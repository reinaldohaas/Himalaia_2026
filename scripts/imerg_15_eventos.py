# -*- coding: utf-8 -*-
"""
GPM IMERG V07 para os 15 desastres himalaios (1981-2026).

Duas fases:
  --catalogo : descobre granulos no CMR da NASA (aberto, SEM credencial) e
               reporta a cobertura de cada evento. Roda agora.
  --baixar   : subsets via OPeNDAP usando o token Earthdata, acumula a chuva
               na janela de cada evento e confronta com a lamina exigida pela
               reconstrucao hidraulica.

Credencial (so na fase --baixar):
    arquivo  %USERPROFILE%\\.earthdata_token   (uma linha), ou
    variavel EARTHDATA_TOKEN
O token nunca e impresso, gravado em log ou enviado a outro destino que nao
o cabecalho Authorization do proprio servidor da NASA.

Uso:
    python scripts/imerg_15_eventos.py --catalogo
    python scripts/imerg_15_eventos.py --baixar
"""
import os
import sys
import ssl
import json
import urllib.request
import urllib.parse
import datetime as dt
from concurrent.futures import ThreadPoolExecutor

import numpy as np

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE          # interceptacao TLS nesta maquina

# ------------------------------------------------------------------ eventos
# lamina requerida: do balanco inverso; area: bacia efetiva adotada
EVENTOS = [
    # id, nome, data do evento (UTC), lon, lat, area_km2, V_agua_Mm3
    ("kedarnath_2013",   "Kedarnath",          dt.date(2013, 6, 17), 79.067, 30.745,  42.0,  4.68),
    ("chamoli_2021",     "Chamoli",            dt.date(2021, 2,  7), 79.732, 30.378,  58.0, 10.73),
    ("himalaia_2026",    "Lhende / Trishuli",  dt.date(2026, 8, 26), 85.515, 28.271,  32.7, 14.20),
    ("aru_2016",         "Aru (Tibete)",       dt.date(2016, 7, 17), 82.285, 34.045,  95.0, 54.40),
    ("seti_2012",        "Seti",               dt.date(2012, 5,  5), 84.152, 28.542,  72.0, 17.60),
    ("south_lhonak_2023","South Lhonak",       dt.date(2023,10,  4), 88.205, 27.905,  88.0, 19.60),
    ("leh_2010",         "Leh Ladakh",         dt.date(2010, 8,  6), 77.577, 34.152,  35.0,  2.36),
    ("melamchi_2021",    "Melamchi",           dt.date(2021, 6, 15), 85.612, 28.095,  62.0,  8.00),
    ("parechu_2000",     "Parechu 2000",       dt.date(2000, 8,  1), 78.536, 32.028, 210.0, 32.40),
    ("zhangzangbo_1981", "Zhangzangbo",        dt.date(1981, 7, 11), 86.045, 28.175,  55.0, 12.92),
    ("dig_tsho_1985",    "Dig Tsho",           dt.date(1985, 8,  4), 86.600, 27.870,  32.0,  3.42),
    ("luggye_tsho_1994", "Luggye Tsho",        dt.date(1994,10,  7), 90.300, 28.080, 110.0, 15.54),
    ("bhotekoshi_2016",  "Bhotekoshi",         dt.date(2016, 7,  5), 85.965, 28.026,  48.0,  6.80),
    ("himachal_2023",    "Himachal Pradesh",   dt.date(2023, 7, 10), 77.150, 31.985, 180.0, 26.25),
    ("parechu_2005",     "Parechu 2005",       dt.date(2005, 6, 26), 78.558, 31.956, 210.0, 27.36),
]

BOX = 0.25          # meia-largura da janela, em graus
DIAS_ANTES = 2      # acumula o dia do evento e os N anteriores
CMR = "https://cmr.earthdata.nasa.gov/search/granules.json"
# Final Run (HH) e calibrado por pluviometro e e a referencia, mas tem latencia
# de ~3,5 meses. Para eventos recentes cai-se no Late Run (HHL), latencia ~14 h,
# sem calibracao por pluviometro. A funcao tenta na ordem e reporta qual usou.
SHORTS = ["GPM_3IMERGHH", "GPM_3IMERGHHL"]
IMERG_INICIO = dt.date(2000, 6, 1)


def build_opener():
    """
    Autentica no Earthdata. Aceita, nesta ordem:
      1. ~/.earthdata_token  ou variavel EARTHDATA_TOKEN  (bearer) -- PREFERIDO,
         porque nao usa senha e portanto nao pode travar a conta no URS
      2. ~/.netrc  com  machine urs.earthdata.nasa.gov  (usa senha; se estiver
         incorreta, tentativas repetidas TRAVAM o perfil por 10 minutos)
    Em nenhum caso a credencial e impressa ou registrada.
    Devolve (opener, header_extra).
    """
    import netrc as _netrc
    import http.cookiejar

    # --- 1. bearer token (preferido: nao usa senha, nao pode travar a conta)
    tok = os.environ.get("EARTHDATA_TOKEN", "").strip()
    if not tok:
        home = os.path.expanduser("~")
        # o Notepad acrescenta .txt silenciosamente; aceita as variantes e
        # IGNORA arquivos vazios (senao cairia no netrc e travaria a conta)
        for nome in (".earthdata_token", ".earthdata_token.txt",
                     "earthdata_token.txt", "earthdata_token"):
            f = os.path.join(home, nome)
            if os.path.exists(f):
                cand = open(f, "r", encoding="utf-8").read().strip()
                if cand:
                    tok = cand
                    break
    if tok:
        op = urllib.request.build_opener(urllib.request.HTTPSHandler(context=CTX))
        print("  autenticacao: bearer token")
        return op, {"Authorization": "Bearer " + tok}

    # --- 2. netrc (usa SENHA: tentativas repetidas TRAVAM a conta no URS)
    auth = None
    home = os.path.expanduser("~")
    for cand in (os.path.join(home, ".netrc"), os.path.join(home, "_netrc"), None):
        try:
            n = _netrc.netrc(cand) if cand else _netrc.netrc()
            auth = n.authenticators("urs.earthdata.nasa.gov")
            if auth:
                break
        except Exception:
            continue
    if auth:
        user, _, pwd = auth
        pm = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        pm.add_password(None, "https://urs.earthdata.nasa.gov", user, pwd)
        op = urllib.request.build_opener(
            urllib.request.HTTPBasicAuthHandler(pm),
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
            urllib.request.HTTPSHandler(context=CTX))
        print("  autenticacao: ~/.netrc (urs.earthdata.nasa.gov)")
        return op, {}

    sys.exit("Credencial nao encontrada. Use ~/.netrc com machine "
             "urs.earthdata.nasa.gov, ou salve um token em ~/.earthdata_token.")


def cmr_granulos(lon, lat, d0, d1):
    """tenta Final Run; se vazio, cai para Late Run. devolve (lista, colecao)"""
    for sn in SHORTS:
        g = _cmr(lon, lat, d0, d1, sn)
        if g:
            return g, sn
    return [], SHORTS[0]


def _cmr(lon, lat, d0, d1, short):
    q = {
        "short_name": short,
        "bounding_box": "%.3f,%.3f,%.3f,%.3f" % (lon - BOX, lat - BOX, lon + BOX, lat + BOX),
        "temporal": "%sT00:00:00Z,%sT23:59:59Z" % (d0.isoformat(), d1.isoformat()),
        "page_size": 300,
    }
    url = CMR + "?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=120, context=CTX) as r:
        d = json.load(r)
    out = []
    for e in d.get("feed", {}).get("entry", []):
        href = None
        for L in e.get("links", []):
            h = L.get("href", "")
            if h.endswith(".HDF5") and "opendap" not in h.lower():
                href = h
                break
        if href:
            out.append((e.get("title", ""), href, e.get("time_start", "")))
    return out


def opendap(href, lon, lat):
    """converte URL de arquivo em consulta OPeNDAP .ascii da janela"""
    u = href.replace("https://data.gesdisc.earthdata.nasa.gov/data/",
                     "https://gpm1.gesdisc.eosdis.nasa.gov/opendap/")
    i0 = int((lon - BOX + 180) / 0.1); i1 = int((lon + BOX + 180) / 0.1)
    j0 = int((lat - BOX + 90) / 0.1);  j1 = int((lat + BOX + 90) / 0.1)
    return "%s.ascii?precipitation[0][%d:1:%d][%d:1:%d]" % (u, i0, i1, j0, j1)


def parse_ascii(txt):
    vals = []
    for line in txt.splitlines():
        if "," not in line:
            continue
        _, _, tail = line.partition(",")
        for tk in tail.split(","):
            try:
                vals.append(float(tk.strip()))
            except ValueError:
                pass
    return np.array(vals)


def fase_catalogo():
    print("=" * 96)
    print("COBERTURA GPM IMERG V07 PARA OS 15 EVENTOS  (Final Run; Late Run como reserva)")
    print("=" * 96)
    print("%-20s %-12s %9s %11s %s" % ("evento", "data", "granulos", "situacao", "colecao"))
    for eid, nome, d, lon, lat, A, V in EVENTOS:
        d0 = d - dt.timedelta(days=DIAS_ANTES)
        if d < IMERG_INICIO:
            print("%-20s %-12s %10s %12s %s"
                  % (nome, d.isoformat(), "-", "SEM COBERTURA",
                     "anterior a 2000-06-01; exige reanalise (ERA5) ou pluviometro"))
            continue
        try:
            g, sn = cmr_granulos(lon, lat, d0, d)
            sit = "OK" if len(g) >= 48 else ("PARCIAL" if g else "VAZIO")
            print("%-20s %-12s %9d %11s %s"
                  % (nome, d.isoformat(), len(g), sit, sn if g else "-"))
        except Exception as ex:
            print("%-20s %-12s %9s %11s %s" % (nome, d.isoformat(), "-", "ERRO", str(ex)[:40]))


def fase_baixar(apenas=None):
    opener, hdr = build_opener()

    def fetch(url):
        req = urllib.request.Request(url, headers=hdr)
        with opener.open(req, timeout=180) as r:
            return r.read().decode("utf-8", "replace")

    print("=" * 108)
    print("PRECIPITACAO IMERG ACUMULADA (evento + %d dias anteriores) x LAMINA EXIGIDA" % DIAS_ANTES)
    print("=" * 108)
    print("%-20s %9s %9s %11s %10s %6s %-14s" %
          ("evento", "media mm", "max mm", "requerida", "deficit x", "n", "colecao"))
    linhas = []
    for eid, nome, d, lon, lat, A, V in EVENTOS:
        if apenas and eid not in apenas:
            continue
        if d < IMERG_INICIO:
            print("%-20s %9s %9s %11s %10s %6s %-14s" % (nome, "-", "-", "-", "-", "-", "sem cobertura"))
            continue
        d0 = d - dt.timedelta(days=DIAS_ANTES)
        try:
            gs, sn = cmr_granulos(lon, lat, d0, d)
        except Exception as ex:
            print("%-20s  CMR falhou: %s" % (nome, str(ex)[:50])); continue
        def um(g):
            try:
                v = parse_ascii(fetch(opendap(g[1], lon, lat)))
            except Exception as ex:
                msg = str(ex)
                if "401" in msg or "403" in msg or "locked" in msg.lower():
                    raise SystemExit(
                        "\nABORTADO: o servidor recusou a autenticacao (%s).\n"
                        "  Nao insisto: tentativas repetidas TRAVAM a conta no URS.\n"
                        "  Verifique a credencial e rode de novo mais tarde." % msg[:80])
                return None
            v = v[np.isfinite(v)]
            v = v[(v >= 0) & (v < 1000)]
            return None if v.size == 0 else (float(np.mean(v)) * 0.5, float(np.max(v)) * 0.5)

        # sonda unica, em serie: so paraleliza depois que UMA requisicao funcionar
        sonda = um(gs[0])
        if sonda is None:
            print("%-20s  sonda inicial falhou; evento ignorado" % nome)
            continue
        with ThreadPoolExecutor(max_workers=4) as ex:
            res = [r for r in ex.map(um, gs[1:]) if r]
        res.insert(0, sonda)
        acc = sum(r[0] for r in res)
        mx = max((r[1] for r in res), default=0.0)
        n = len(res)
        preq = V * 1e6 / (A * 1e6 * 0.85) * 1000
        if n == 0:
            print("%-20s %9s %9s %11.1f %10s %6d %-14s"
                  % (nome, "FALHA", "FALHA", preq, "SEM DADO", 0, sn))
            continue
        if n < len(gs) * 0.8:
            print("     [aviso] %s: so %d de %d granulos lidos" % (nome, n, len(gs)))
        raz = preq / acc if acc > 0 else float("inf")
        linhas.append((nome, acc, mx, preq, raz, n, sn))
        print("%-20s %9.2f %9.2f %11.1f %10.1f %6d %-14s"
              % (nome, acc, mx, preq, raz, n, sn))

    print("\n" + "=" * 108)
    print("LEITURA")
    print("=" * 108)
    print("  deficit x = lamina requerida / chuva IMERG acumulada.")
    print("  Valores proximos de 1 ou abaixo: a chuva observada explica a cheia.")
    print("  O IMERG tem vies seco documentado em extremos orograficos no Himalaia")
    print("  (NW-Himalaya, jul/2026: ~400 mm/dia IMERG contra ~650 mm/dia IMD).")
    print("  Portanto o 'deficit x' aqui e um TETO, nao uma medida fechada.")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "data", "processed", "imerg_15_eventos.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("evento,imerg_acum_mm,imerg_max_mm,lamina_requerida_mm,deficit_x,n_granulos\n")
        for r in linhas:
            f.write("%s,%.3f,%.3f,%.2f,%.3f,%d,%s\n" % r)
    print("\n  salvo: %s" % out)


if __name__ == "__main__":
    if "--baixar" in sys.argv:
        sel = [a for a in sys.argv[1:] if not a.startswith("--")]
        fase_baixar(apenas=sel or None)
    else:
        fase_catalogo()
