# -*- coding: utf-8 -*-
"""
Jz CONSTRUIDO A PARTIR DE DADO MEDIDO — raios cosmicos galacticos.

Cadeia fisica, sem nenhum valor arbitrado:
    GCR  ->  taxa de ionizacao q
    equilibrio ion-ion:  n = sqrt(q/alpha)  ->  sigma = n e mu  ->  sigma ~ q^0.5
    Rc = integral dz/sigma  ->  Rc ~ q^-0.5
    Jz = VI / Rc           ->  Jz ~ VI * sqrt(GCR)
    a VI constante:        dJz/Jz = 0.5 * dGCR/GCR

Esta e a via que Tinsley de fato propoe (modulacao de GCR -> ionizacao
troposferica -> condutividade -> Jz), e a unica que continua aberta depois
que o crochet medido limitou a via de raios X do flare a ~1e-5 %.

Dado: NMDB (nmdb.eu), monitores de neutrons, contagem horaria. Aberto, sem
credencial. Estacoes de rigidez de corte diferente sao usadas de proposito:
a COMPARACAO entre elas E o teste de rigidez de corte, sem assumir expoente.

    OULU  0,81 GV  (polar; serie desde 1964, alcanca os 15 eventos)
    ATHN  8,53 GV  (Atenas)
    MXCO  8,20 GV  (Cidade do Mexico)

O Himalaia esta a ~13-14 GV. Se um sinal aparece em OULU e some em ATHN/MXCO,
ele nao alcanca a rigidez do sitio.

Uso:  python scripts/jz_de_raios_cosmicos.py
"""
import ssl
import sys
import urllib.request
import datetime as dt
from math import comb

import numpy as np

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

ESTACOES = [("OULU", 0.81), ("ATHN", 8.53), ("MXCO", 8.20)]

EVENTOS = [
    ("Kedarnath",         dt.datetime(2013, 6, 17, 1, 45)),
    ("Chamoli",           dt.datetime(2021, 2,  7, 4, 51)),
    ("Lhende / Trishuli", dt.datetime(2026, 8, 26, 2, 52)),
    ("Aru (Tibete)",      dt.datetime(2016, 7, 17, 4,  0)),
    ("Seti",              dt.datetime(2012, 5,  5, 3, 30)),
    ("South Lhonak",      dt.datetime(2023,10,  3,18, 30)),
    ("Leh Ladakh",        dt.datetime(2010, 8,  5,20,  0)),
    ("Melamchi",          dt.datetime(2021, 6, 15,12,  0)),
    ("Parechu 2000",      dt.datetime(2000, 8,  1,12,  0)),
    ("Zhangzangbo",       dt.datetime(1981, 7, 11,12,  0)),
    ("Dig Tsho",          dt.datetime(1985, 8,  4,12,  0)),
    ("Luggye Tsho",       dt.datetime(1994,10,  7,12,  0)),
    ("Bhotekoshi",        dt.datetime(2016, 7,  5,12,  0)),
    ("Himachal Pradesh",  dt.datetime(2023, 7,  9,12,  0)),
    ("Parechu 2005",      dt.datetime(2005, 6, 26,12,  0)),
]

BASE_DIAS = 27       # linha de base: rotacao solar de Carrington
JANELA_H = 72        # janela anterior ao evento


def nmdb(st, t0, t1):
    """contagem horaria corrigida por eficiencia, entre t0 e t1"""
    u = ("https://www.nmdb.eu/nest/draw_graph.php?formchk=1&stations[]=%s"
         "&tabchoice=revori&dtype=corr_for_efficiency&tresolution=60&force=1"
         "&yunits=0&date_choice=bydate"
         "&start_day=%d&start_month=%d&start_year=%d&start_hour=0&start_min=0"
         "&end_day=%d&end_month=%d&end_year=%d&end_hour=23&end_min=59"
         "&output=ascii") % (st, t0.day, t0.month, t0.year, t1.day, t1.month, t1.year)
    with urllib.request.urlopen(u, timeout=180, context=CTX) as r:
        txt = r.read().decode("utf-8", "replace")
    T, V = [], []
    for ln in txt.splitlines():
        ln = ln.strip()
        if not ln or not ln[:4].isdigit() or ";" not in ln:
            continue
        a, _, b = ln.partition(";")
        try:
            T.append(dt.datetime.strptime(a.strip(), "%Y-%m-%d %H:%M:%S"))
            V.append(float(b.strip()))
        except ValueError:
            continue
    return np.array(T), np.array(V, dtype=float)


def anomalia(T, V, t_ev):
    """
    anomalia de GCR na janela anterior ao evento, em % da linha de base.
    linha de base: mediana dos BASE_DIAS anteriores, excluindo a janela.
    """
    if T.size == 0:
        return None
    dt_h = np.array([(t - t_ev).total_seconds() / 3600.0 for t in T])
    base = (dt_h < -JANELA_H) & (dt_h > -BASE_DIAS * 24.0)
    jan = (dt_h >= -JANELA_H) & (dt_h <= 0)
    if base.sum() < 100 or jan.sum() < 24:
        return None
    b = np.median(V[base])
    if not np.isfinite(b) or b <= 0:
        return None
    return {
        "base": b,
        "media_pct": 100.0 * (np.mean(V[jan]) - b) / b,
        "min_pct": 100.0 * (np.min(V[jan]) - b) / b,   # profundidade do decrescimo
        "n_base": int(base.sum()), "n_jan": int(jan.sum()),
    }


def main():
    print("=" * 104)
    print("Jz CONSTRUIDO A PARTIR DE RAIOS COSMICOS MEDIDOS (NMDB) — 15 EVENTOS")
    print("=" * 104)
    print("dJz/Jz = 0,5 x dGCR/GCR   (sigma ~ sqrt(q), Rc ~ q^-0,5, Jz = VI/Rc)")
    print("Janela: %d h anteriores ao evento. Linha de base: mediana dos %d dias precedentes.\n"
          % (JANELA_H, BASE_DIAS))

    tab = {}
    for st, R in ESTACOES:
        print("-" * 104)
        print("ESTACAO %s  (rigidez de corte %.2f GV)" % (st, R))
        print("%-20s %12s %12s %12s %12s" %
              ("evento", "GCR med %", "GCR min %", "dJz med %", "dJz min %"))
        vals = []
        for nome, t_ev in EVENTOS:
            t0 = (t_ev - dt.timedelta(days=BASE_DIAS + 1)).date()
            t1 = t_ev.date()
            try:
                T, V = nmdb(st, t0, t1)
                a = anomalia(T, V, t_ev)
            except Exception as ex:
                print("%-20s  falha: %s" % (nome, str(ex)[:50]))
                continue
            if a is None:
                print("%-20s %12s %12s %12s %12s" % (nome, "sem dado", "-", "-", "-"))
                continue
            print("%-20s %+12.2f %+12.2f %+12.3f %+12.3f" %
                  (nome, a["media_pct"], a["min_pct"],
                   0.5 * a["media_pct"], 0.5 * a["min_pct"]))
            vals.append(a["media_pct"])
        tab[st] = vals
        if vals:
            v = np.array(vals)
            print("  -> n=%d | media %+.2f %% | mediana %+.2f %% | dp %.2f"
                  % (len(v), v.mean(), np.median(v), v.std(ddof=1) if len(v) > 1 else 0))

    print("\n" + "=" * 104)
    print("TESTE DE RIGIDEZ: o sinal sobrevive ao subir a rigidez de corte?")
    print("=" * 104)
    for st, R in ESTACOES:
        v = np.array(tab.get(st, []))
        if v.size:
            print("  %-6s (%5.2f GV): media das anomalias = %+6.2f %%  ->  dJz medio = %+6.3f %%"
                  % (st, R, v.mean(), 0.5 * v.mean()))
    print("\n  O sitio esta a ~13-14 GV, acima de todas estas estacoes.")
    print("  Se a anomalia ja e pequena a 8,2-8,5 GV, a 13-14 GV e menor ainda.")


if __name__ == "__main__":
    main()
