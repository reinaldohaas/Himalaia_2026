# -*- coding: utf-8 -*-
"""
Serie meia-horaria de precipitacao IMERG sobre a bacia do Lhende Khola,
25 e 26 de agosto de 2026 — preservando o TEMPO, nao so o acumulado.

Salva a serie para combinar com a area de nuvem fria do Himawari-9 e com Jz.
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
CTX.verify_mode = ssl.CERT_NONE

LON, LAT = 85.515, 28.271
BOX = 0.25
CMR = "https://cmr.earthdata.nasa.gov/search/granules.json"
SHORT = "GPM_3IMERGHHL"          # Late Run: o Final ainda nao cobre ago/2026


def token():
    t = os.environ.get("EARTHDATA_TOKEN", "").strip()
    if t:
        return t
    home = os.path.expanduser("~")
    for n in (".earthdata_token", ".earthdata_token.txt", "earthdata_token.txt"):
        p = os.path.join(home, n)
        if os.path.exists(p):
            c = open(p, encoding="utf-8").read().strip()
            if c:
                return c
    sys.exit("token Earthdata nao encontrado")


TOK = token()


def fetch(u):
    r = urllib.request.Request(u, headers={"Authorization": "Bearer " + TOK})
    with urllib.request.urlopen(r, timeout=180, context=CTX) as x:
        return x.read().decode("utf-8", "replace")


def granulos(d0, d1):
    q = {"short_name": SHORT,
         "bounding_box": "%.3f,%.3f,%.3f,%.3f" % (LON - BOX, LAT - BOX, LON + BOX, LAT + BOX),
         "temporal": "%sT00:00:00Z,%sT23:59:59Z" % (d0.isoformat(), d1.isoformat()),
         "page_size": 300}
    with urllib.request.urlopen(CMR + "?" + urllib.parse.urlencode(q), timeout=120, context=CTX) as r:
        d = json.load(r)
    out = []
    for e in d.get("feed", {}).get("entry", []):
        for L in e.get("links", []):
            h = L.get("href", "")
            if h.endswith(".HDF5") and "opendap" not in h.lower():
                out.append((e.get("time_start", ""), h))
                break
    return sorted(out)


def opendap(href):
    u = href.replace("https://data.gesdisc.earthdata.nasa.gov/data/",
                     "https://gpm1.gesdisc.eosdis.nasa.gov/opendap/")
    i0 = int((LON - BOX + 180) / 0.1); i1 = int((LON + BOX + 180) / 0.1)
    j0 = int((LAT - BOX + 90) / 0.1);  j1 = int((LAT + BOX + 90) / 0.1)
    return "%s.ascii?precipitation[0][%d:1:%d][%d:1:%d]" % (u, i0, i1, j0, j1)


def parse(t):
    v = []
    for ln in t.splitlines():
        if "," not in ln:
            continue
        _, _, tail = ln.partition(",")
        for tk in tail.split(","):
            try:
                v.append(float(tk.strip()))
            except ValueError:
                pass
    return np.array(v)


def main():
    gs = granulos(dt.date(2026, 8, 25), dt.date(2026, 8, 26))
    print("granulos: %d" % len(gs))
    if not gs:
        sys.exit("nenhum granulo")

    def um(g):
        try:
            v = parse(fetch(opendap(g[1])))
        except Exception as ex:
            if "401" in str(ex) or "403" in str(ex):
                raise SystemExit("ABORTADO: autenticacao recusada")
            return None
        v = v[np.isfinite(v)]
        v = v[(v >= 0) & (v < 1000)]
        return None if v.size == 0 else (g[0], float(np.mean(v)), float(np.max(v)))

    sonda = um(gs[0])
    if sonda is None:
        sys.exit("sonda inicial falhou")
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = [r for r in ex.map(um, gs[1:]) if r]
    res.insert(0, sonda)
    res.sort()
    print("lidos: %d de %d" % (len(res), len(gs)))

    T = [dt.datetime.strptime(r[0][:19], "%Y-%m-%dT%H:%M:%S") for r in res]
    med = np.array([r[1] for r in res])      # mm/h medio na caixa
    mx = np.array([r[2] for r in res])       # mm/h maximo na caixa
    acc = np.cumsum(med * 0.5)

    print("\n%-18s %10s %10s %10s" % ("UTC", "med mm/h", "max mm/h", "acum mm"))
    for t, a, b, c in zip(T, med, mx, acc):
        mk = ""
        if t == dt.datetime(2026, 8, 26, 2, 30):
            mk = "  <-- colapso 02:52"
        if t == dt.datetime(2026, 8, 25, 18, 0):
            mk = "  <-- pico convectivo (Himawari)"
        if a > 0.05 or mk:
            print("%-18s %10.3f %10.3f %10.2f%s" % (t.strftime("%d/%m %H:%M"), a, b, c, mk))

    i_col = int(np.argmin([abs((t - dt.datetime(2026, 8, 26, 2, 52)).total_seconds()) for t in T]))
    print("\n  acumulado ATE o colapso   : %.2f mm" % acc[i_col])
    print("  acumulado total 25+26/08  : %.2f mm" % acc[-1])
    print("  pico de taxa media        : %.3f mm/h em %s UTC"
          % (med.max(), T[int(np.argmax(med))].strftime("%d/%m %H:%M")))
    print("  pico de taxa maxima       : %.3f mm/h em %s UTC"
          % (mx.max(), T[int(np.argmax(mx))].strftime("%d/%m %H:%M")))

    h = np.array([(t - dt.datetime(2026, 8, 25)).total_seconds() / 3600.0 for t in T])
    np.save(r"C:\Users\haas\AppData\Local\Temp\imerg_serie_2026.npy",
            np.array([h, med, mx, acc]))
    print("\n  serie salva")


if __name__ == "__main__":
    main()
