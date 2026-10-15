# -*- coding: utf-8 -*-
"""
GPM IMERG V07 sobre a bacia do Lhende Khola — 25 e 26 de agosto de 2026.

Baixa apenas a JANELA da bacia via OPeNDAP (poucos kB por granulo, nao os ~20 MB
do arquivo global), acumula a precipitacao e compara com o que o balanco hidrico
exige. Nao imprime, nao registra e nao transmite o token para lugar nenhum
alem do cabecalho Authorization da propria NASA.

Credencial:
    - arquivo  %USERPROFILE%\\.earthdata_token   (uma linha, so o token), ou
    - variavel de ambiente EARTHDATA_TOKEN

Uso:
    python scripts/imerg_2026_bacia.py
"""
import os
import sys
import ssl
import json
import urllib.request
import datetime as dt

import numpy as np

# ---------------------------------------------------------------- credencial
def get_token():
    tok = os.environ.get("EARTHDATA_TOKEN", "").strip()
    if tok:
        return tok
    p = os.path.join(os.path.expanduser("~"), ".earthdata_token")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            tok = f.read().strip()
        if tok:
            return tok
    sys.exit(
        "Token nao encontrado.\n"
        "  Gere um em https://urs.earthdata.nasa.gov (Generate Token) e salve em:\n"
        "    %USERPROFILE%\\.earthdata_token\n"
        "  ou defina a variavel de ambiente EARTHDATA_TOKEN."
    )

TOKEN = get_token()
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE          # interceptacao TLS corporativa nesta maquina


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read().decode("utf-8", "replace")


# ------------------------------------------------------------------ dominio
# Caixa cobrindo as bacias reais delineadas no GLO-30 (3,4 / 17,4 / 32,7 km2)
# e folga para a bacia do tronco a montante de Rasuwagadhi.
LON_MIN, LON_MAX = 85.30, 85.80
LAT_MIN, LAT_MAX = 28.15, 28.55

# grade IMERG: 0,1 grau, lon -180..180 (3600), lat -90..90 (1800)
i0 = int((LON_MIN + 180) / 0.1)
i1 = int((LON_MAX + 180) / 0.1)
j0 = int((LAT_MIN + 90) / 0.1)
j1 = int((LAT_MAX + 90) / 0.1)

BASE = "https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGHHL.07"
VAR = "precipitation"          # mm/h


def granules(day):
    """nomes dos 48 granulos meia-horarios de um dia"""
    doy = day.timetuple().tm_yday
    out = []
    for k in range(48):
        s = k * 30
        h0, m0 = divmod(s, 60)
        e = s + 29
        h1, m1 = divmod(e, 60)
        name = ("3B-HHR-L.MS.MRG.3IMERG.%s-S%02d%02d00-E%02d%02d59.%04d.V07C.HDF5"
                % (day.strftime("%Y%m%d"), h0, m0, h1, m1, s))
        out.append(("%s/%d/%03d/%s" % (BASE, day.year, doy, name), name, s))
    return out


def parse_ascii(txt):
    """extrai os numeros do retorno .ascii do OPeNDAP"""
    vals = []
    for line in txt.splitlines():
        if "," not in line:
            continue
        head, _, tail = line.partition(",")
        if any(c.isalpha() for c in head) and "[" not in head:
            continue
        for tk in tail.split(","):
            tk = tk.strip()
            try:
                vals.append(float(tk))
            except ValueError:
                pass
    return np.array(vals)


def main():
    print("=" * 84)
    print("GPM IMERG V07 (Late) — Lhende Khola — 25 e 26 de agosto de 2026")
    print("=" * 84)
    print("janela: %.2f-%.2f E / %.2f-%.2f N  (indices lon %d:%d, lat %d:%d)"
          % (LON_MIN, LON_MAX, LAT_MIN, LAT_MAX, i0, i1, j0, j1))
    print("subsetting via OPeNDAP: so a janela, ~1 kB por granulo\n")

    total = {}
    serie = []
    for day in (dt.date(2026, 8, 25), dt.date(2026, 8, 26)):
        acc = 0.0
        for url, name, sec in granules(day):
            q = "%s.ascii?/Grid/%s[0][%d:%d][%d:%d]" % (url, VAR, i0, i1, j0, j1)
            try:
                v = parse_ascii(fetch(q))
            except Exception as ex:
                print("  %s  FALHA: %s" % (name[38:53], str(ex)[:60]))
                continue
            v = v[np.isfinite(v)]
            v = v[(v >= 0) & (v < 1000)]
            if v.size == 0:
                continue
            mm = float(np.mean(v)) * 0.5          # mm/h durante meia hora
            mx = float(np.max(v)) * 0.5
            acc += mm
            hh, mm_ = divmod(sec, 60)
            serie.append((day, hh, mm_, mm, mx, acc))
        total[day] = acc
        print("  %s : acumulado do dia = %.2f mm (media na janela)" % (day, acc))

    print("\n" + "=" * 84)
    print("MEIAS-HORAS COM CHUVA (media na janela > 0,05 mm)")
    print("=" * 84)
    print("%-12s %6s %10s %10s %10s" % ("dia", "UTC", "media mm", "max mm", "acum mm"))
    for day, hh, mm_, m, mx, acc in serie:
        if m > 0.05:
            print("%-12s %02d:%02d %10.3f %10.3f %10.2f" % (day, hh, mm_, m, mx, acc))

    grand = sum(total.values())
    print("\n" + "=" * 84)
    print("CONFRONTO COM O BALANCO HIDRICO")
    print("=" * 84)
    print("  acumulado IMERG em 25+26/08 (media na janela): %.2f mm" % grand)
    print("\n  lamina requerida pela reconstrucao hidraulica, por area de bacia:")
    for A, rot in ((3.39, "chegada ao vale, 4.010 m"),
                   (17.39, "garganta 3.615 m"),
                   (32.71, "garganta 3.103 m"),
                   (934.0, "secao onde o nivel foi lido")):
        for V, tag in ((14.2e6, "V=14,2 Mm3"), (17.2e6, "V=17,2 Mm3")):
            p = V / (A * 1e6 * 0.85) * 1000
            razao = (p / grand) if grand > 0 else float("inf")
            print("    A=%7.2f km2 (%-28s) %s -> %8.1f mm  | deficit %6.1fx"
                  % (A, rot, tag, p, razao))
    print("\n  Nota: o IMERG subestima extremos orograficos no Himalaia (viés seco")
    print("  documentado; ver Jul 2026 NW-Himalaya ~400 vs ~650 mm/dia do IMD).")
    print("  Trate o valor acima como PISO, nao como medida fechada.")


if __name__ == "__main__":
    main()
