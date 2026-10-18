# -*- coding: utf-8 -*-
"""
Diagnostico dos experimentos do toro (criterios pre-registrados em experimentos_toro/LEIA-ME.md).
Autonomo (leitor GrADS proprio, so numpy). Le cm1out_s de uma rodada e, a cada saida:
  anfiteatro = |x|,|y| <= 1,5 km (9 km2); r10 = ate 10 km do colapso (0,0)
  * slw_t      : agua liquida (qc+qr) com T < 0 C sobre o anfiteatro (t)
  * gelo_t     : gelo + neve + graupel + granizo sobre o anfiteatro (t)
  * ni_hm      : cristais (cci+csw) na faixa -3 a -8 C sobre o anfiteatro (por litro, media)
  * chuva_mm   : chuva acumulada media no anfiteatro (mm); taxa_mmh = taxa media desde a saida anterior
  * prate_max  : maior taxa instantanea de superficie no anfiteatro (mm/h)
  * vol_anf_m3, vol_r10_m3 : volume precipitado acumulado (m3)
  * f1_r10     : proxy de raios de McCaul et al. (2009), F1 = 0,042 * w * qg a -15 C (qg em g/kg),
                 somado no raio de 10 km (raios por 5 min)
  * wdown_min  : menor w (m/s) a menos de 1 km do solo no raio de 10 km (correntes descendentes)
  * tb_sitio   : topo "equivalente IR" sobre o sitio (K): T onde o condensado acumulado de cima atinge 15 g/m2
Uso:  python3 diag_toro.py <dir_rodada> <hora_inicial_UTC> <prefixo> [rotulo]   -> <prefixo>.json e .txt
      python3 diag_toro.py --tabela <prefixo_comum>   (ex.: logs/diag_)          -> tabela dos criterios
"""
import glob
import json
import os
import re
import sys

import numpy as np

ZBASE = 3000.0
AREA = 500.0 * 500.0
CTRL = "rad_06utc_hib16x7"


def abrir(ctl):
    txt = open(ctl, encoding="utf-8", errors="ignore").read()
    nx = int(re.search(r"xdef\s+(\d+)", txt).group(1)); ny = int(re.search(r"ydef\s+(\d+)", txt).group(1))
    x0, dx = map(float, re.search(r"xdef\s+\d+\s+linear\s+(\S+)\s+(\S+)", txt).groups())
    y0, dy = map(float, re.search(r"ydef\s+\d+\s+linear\s+(\S+)\s+(\S+)", txt).groups())
    linhas = re.search(r"\nvars\s+\d+\n(.*?)\nendvars", txt, re.S).group(1).splitlines()
    vs = [(l.split()[0], max(int(l.split()[1]), 1)) for l in linhas]
    dset = re.search(r"dset\s+\^?(\S+)", txt).group(1)
    por_t = sum(k for _, k in vs) * nx * ny
    mm = np.memmap(os.path.join(os.path.dirname(ctl), dset), dtype="<f4", mode="r")
    nt = mm.size // por_t
    idx, off = {}, 0
    for n, k in vs:
        idx[n] = (off, k); off += k * nx * ny

    def campo(n, t):
        o, k = idx[n]
        a = np.asarray(mm[t * por_t + o: t * por_t + o + k * nx * ny], dtype=np.float64)
        return a.reshape(k, ny, nx) if k > 1 else a.reshape(ny, nx)
    x = x0 + dx * np.arange(nx); y = y0 + dy * np.arange(ny)
    return x, y, nt, campo, idx


def interp_T(f3, T3, T0):
    """valor de f3 no primeiro nivel (de baixo para cima) em que T cruza T0"""
    abaixo = T3 >= T0
    cruza = abaixo[:-1] & ~abaixo[1:]
    k = np.argmax(cruza, axis=0); ok = cruza.any(axis=0)
    t0 = np.take_along_axis(T3, k[None], 0)[0]; t1 = np.take_along_axis(T3, (k + 1)[None], 0)[0]
    f0 = np.take_along_axis(f3, k[None], 0)[0]; f1 = np.take_along_axis(f3, (k + 1)[None], 0)[0]
    w = (t0 - T0) / np.where(t0 != t1, t0 - t1, 1.0)
    return np.where(ok, f0 + w * (f1 - f0), 0.0)


def diag(d, h0, prefixo, rotulo):
    x, y, nt, campo, idx = abrir(os.path.join(d, "cm1out_s.ctl"))
    X, Y = np.meshgrid(x, y); R = np.hypot(X, Y)
    anf = (np.abs(X) <= 1.5) & (np.abs(Y) <= 1.5); r10 = R <= 10.0
    ic = np.unravel_index(np.argmin(R), R.shape)
    zs = campo("zs", 0) + ZBASE
    tem = lambda n: n in idx
    S = []
    chuva_ant = None
    for t in range(nt):
        zh = campo("zhval", t) + ZBASE
        T = campo("th", t) * (campo("prs", t) / 1e5) ** 0.2857
        rho = campo("rho", t)
        dz = np.clip(np.gradient(zh, axis=0), 1.0, None)
        qc, qr = campo("qc", t), campo("qr", t)
        qi, qs, qg = campo("qi", t), campo("qs", t), campo("qg", t)
        qhl = campo("qhl", t) if tem("qhl") else 0.0 * qg
        liq = (qc + qr) * rho * dz; gel = (qi + qs + qg + qhl) * rho * dz       # kg/m2 por camada
        slw = np.where(T < 273.15, liq, 0.0).sum(axis=0)
        ni = (campo("cci", t) + campo("csw", t)) * rho / 1000.0 if tem("cci") else 0.0 * T   # por litro
        banda = (T <= 270.15) & (T >= 265.15)
        cols = np.broadcast_to(anf, T.shape) & banda
        ni_hm = float(ni[cols].mean()) if cols.any() else 0.0
        chuva = campo("rain", t) * 10.0                                         # cm -> mm
        prate = campo("prate", t) * 3600.0 if tem("prate") else 0.0 * chuva      # kg/m2/s -> mm/h
        w = campo("winterp", t)
        f1 = 0.042 * interp_T(w * qg * 1000.0, T, 258.15)                         # McCaul F1 (por 5 min por km2)
        f1 = np.clip(f1, 0.0, None)
        agl = zh - zs[None]
        wlow = np.where((agl < 1000.0) & np.broadcast_to(r10, T.shape), w, np.nan)
        acum = np.cumsum((liq + gel)[::-1], axis=0) * 1000.0                     # g/m2 de cima para baixo
        j, i = ic; a = acum[:, j, i]
        k = int(np.argmax(a >= 15.0)) if (a >= 15.0).any() else None
        tb = float(T[::-1][k, j, i]) if k is not None else float(T[0, j, i])
        S.append({"t": t,
                  "slw_t": float(slw[anf].sum() * AREA / 1000.0),
                  "gelo_t": float(gel.sum(axis=0)[anf].sum() * AREA / 1000.0),
                  "ni_hm_L": ni_hm,
                  "chuva_mm": float(chuva[anf].mean()),
                  "prate_max_mmh": float(prate[anf].max()),
                  "vol_anf_m3": float(chuva[anf].sum() / 1000.0 * AREA),
                  "vol_r10_m3": float(chuva[r10].sum() / 1000.0 * AREA),
                  "f1_r10": float(f1[r10].sum() * 0.25),
                  "wdown_min": float(np.nanmin(wlow)) if np.isfinite(wlow).any() else 0.0,
                  "tb_sitio": tb})
    # horas: deduz o intervalo das saidas pelo tamanho (tapfrq) a partir do namelist
    nl = open(os.path.join(d, "namelist.input")).read()
    tap = float(re.search(r"^\s*tapfrq\s*=\s*([0-9.eE+-]+)", nl, re.M).group(1))
    for s in S:
        s["hora_utc"] = h0 + s["t"] * tap / 3600.0
    for a, b in zip(S[:-1], S[1:]):
        b["taxa_mmh"] = (b["chuva_mm"] - a["chuva_mm"]) / (tap / 3600.0)
    S[0]["taxa_mmh"] = 0.0
    lido = "LIGADO" if "TORO: toro_params.txt lido" in open(os.path.join(d, "cm1.print.out"), errors="ignore").read() else "desligado"
    out = {"rotulo": rotulo, "dir": d, "tapfrq": tap, "toro": lido, "saidas": S}
    json.dump(out, open(prefixo + ".json", "w"), indent=1)
    with open(prefixo + ".txt", "w", encoding="utf-8") as f:
        f.write("%s (%s, toro %s, saidas a cada %.0f s)\n" % (rotulo, d, lido, tap))
        f.write(" UTC    SLW(t)  gelo(t)  Ni_HM/L  chuva(mm) taxa(mm/h) prate_max  vol_anf(m3)  vol_r10(m3)  F1_r10  wdown  Tb_sitio\n")
        for s in S:
            f.write("%5.2f %8.0f %8.0f %8.1f %9.2f %9.1f %9.1f %12.0f %12.0f %7.1f %6.1f %8.1f\n" % (
                s["hora_utc"] % 24, s["slw_t"], s["gelo_t"], s["ni_hm_L"], s["chuva_mm"], s["taxa_mmh"],
                s["prate_max_mmh"], s["vol_anf_m3"], s["vol_r10_m3"], s["f1_r10"], s["wdown_min"], s["tb_sitio"]))
    print("diag gravado:", prefixo + ".{json,txt}", "| toro", lido)


def janela(S, a, b):
    return [s for s in S if a <= s["hora_utc"] <= b + 1e-6]


def tabela(pref):
    J = {}
    for f in sorted(glob.glob(pref + "*.json")):
        d = json.load(open(f)); J[d["rotulo"]] = d
    c = J.get(CTRL)
    slw_c = max(s["slw_t"] for s in janela(c["saidas"], 24.0, 26.5)) if c else None
    print("Experimentos do toro -- criterios pre-registrados (experimentos_toro/LEIA-ME.md); anfiteatro 3x3 km\n")
    print("%-18s %-9s | %9s %7s | %9s %9s %4s | %11s %11s | %7s %7s | %7s" % (
        "rodada", "toro", "SLW00-0230", "x ctrl", "taxa_max", "taxa_ant", "C2", "vol_anf00-03", "vol_r10 00-03",
        "F1 00-03", "wdown", "Tb0230-03"))
    for nome, d in J.items():
        S = d["saidas"]
        slw = max(s["slw_t"] for s in janela(S, 24.0, 26.5))
        lib = janela(S, 25.5, 27.0); ant = janela(S, 23.5, 25.5)
        tx = max(s["taxa_mmh"] for s in lib) if lib else float("nan")
        txa = max(s["taxa_mmh"] for s in ant) if ant else float("nan")
        c2 = "SIM" if (tx >= 50.0 and txa < 1.0) else "nao"
        n00 = janela(S, 24.0, 24.0)[0] if janela(S, 24.0, 24.0) else S[0]
        n03 = S[-1]
        f1 = sum(s["f1_r10"] for s in janela(S, 24.0, 27.0)) * (d["tapfrq"] / 300.0)
        wd = min(s["wdown_min"] for s in janela(S, 24.0, 27.0))
        tb = [s["tb_sitio"] for s in janela(S, 26.5, 27.0)]
        print("%-18s %-9s | %9.0f %7s | %9.1f %9.1f %4s | %11.0f %11.0f | %7.0f %7.1f | %s" % (
            nome, d["toro"], slw, ("%.1f" % (slw / slw_c)) if slw_c else "-", tx, txa, c2,
            n03["vol_anf_m3"] - n00["vol_anf_m3"], n03["vol_r10_m3"] - n00["vol_r10_m3"], f1, wd,
            "/".join("%.0f" % v for v in tb)))
    print("\nC1 (reservatorio) = 'x ctrl' >= 10 | C2 (liberacao explosiva) = taxa media no anfiteatro >= 50 mm/h em 01:30-03 UTC"
          " depois de < 1 mm/h em 23:30-01:30 | volumes em m3 (premissa do repositorio: 14,2e6 m3; IMERG: 5 mm ate o colapso)"
          " | F1 = raios estimados no raio de 10 km, 00-03 UTC | Himawari 02:50: 272,7 K")


if __name__ == "__main__":
    if sys.argv[1] == "--tabela":
        tabela(sys.argv[2])
    else:
        diag(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else os.path.basename(sys.argv[1]))
