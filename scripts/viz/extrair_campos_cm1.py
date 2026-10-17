# -*- coding: utf-8 -*-
"""
Extrai, de uma rodada do CM1 (saida GrADS), os campos 2D do visualizador, a cada saida (30 min):
  rain  chuva acumulada na superficie (mm)
  slw   agua liquida (nuvem + chuva) com T < 0 C, integrada na coluna (g/m2)
  gelo  gelo + neve + graupel integrados na coluna (g/m2)
  tb    temperatura de topo "equivalente IR" (K): T do nivel em que o condensado acumulado de cima
        para baixo atinge 15 g/m2; sem esse nivel, a temperatura da superficie (aproximacao, sem
        transferencia radiativa; a mesma de pos/checar_janela.py)
Grava JSON compacto: cada campo quantizado em uint8 (raiz quadrada para rain/slw/gelo; linear para tb)
e codificado em base64.

Uso: python3 extrair_campos_cm1.py <dir_rodada> <hora_inicial_UTC> <saida.json> <rotulo>
"""
import base64
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads  # copia de scripts/toro_cm1/grads.py

ZBASE, LIMIAR = 3000.0, 15.0
ESCALA = {"rain": ("sqrt", 0.0, 60.0), "slw": ("sqrt", 0.0, 5000.0),
          "gelo": ("sqrt", 0.0, 20000.0), "tb": ("lin", 185.0, 330.0)}


def quantiza(a, nome):
    tipo, lo, hi = ESCALA[nome]
    x = np.clip((a - lo) / (hi - lo), 0, 1)
    if tipo == "sqrt":
        x = np.sqrt(x)
    return base64.b64encode(np.round(x * 255).astype(np.uint8).tobytes()).decode()


def main(d, h0, saida, rotulo):
    s, dd = grads.ler(os.path.join(d, "cm1out_s.ctl"),
                      ["rain", "zs", "zhval", "th", "prs", "rho", "qc", "qr", "qi", "qs", "qg", "tsk"])
    nt = s["th"].shape[0]
    zs = s["zs"][0, 0] + ZBASE
    campos = {k: [] for k in ESCALA}
    extremos = {k: [np.inf, -np.inf] for k in ESCALA}
    for t in range(nt):
        zh = s["zhval"][t] + ZBASE
        T = s["th"][t] * (s["prs"][t] / 1e5) ** 0.2857
        rho = s["rho"][t]
        dz = np.clip(np.gradient(zh, axis=0), 1, None)
        liq = (s["qc"][t] + s["qr"][t]) * rho * dz * 1000.0           # g/m2 por camada
        gel = (s["qi"][t] + s["qs"][t] + s["qg"][t]) * rho * dz * 1000.0
        slw = np.where(T < 273.15, liq, 0.0).sum(axis=0)
        acum = np.cumsum((liq + gel)[::-1], axis=0)
        atinge = acum >= LIMIAR
        kk = np.argmax(atinge, axis=0)
        ttop = np.take_along_axis(T[::-1], kk[None], axis=0)[0]
        tb = np.where(atinge.any(axis=0), ttop, s["tsk"][t, 0])
        f = {"rain": s["rain"][t, 0] * 10.0, "slw": slw, "gelo": gel.sum(axis=0), "tb": tb}
        for k, a in f.items():
            campos[k].append(quantiza(a, k))
            extremos[k] = [min(extremos[k][0], float(np.nanmin(a))), max(extremos[k][1], float(np.nanmax(a)))]
    x = dd["xdef"]
    out = {"rotulo": rotulo, "nx": len(x), "ny": len(dd["ydef"]), "x0_km": float(x[0]), "dx_km": float(x[1] - x[0]),
           "horas_utc": [h0 + 0.5 * t for t in range(nt)], "escala": ESCALA, "extremos": extremos,
           "zs_m": base64.b64encode(np.round(zs).astype("<u2").tobytes()).decode(), "campos": campos}
    json.dump(out, open(saida, "w"), separators=(",", ":"))
    print("%s: %d saidas, %.1f MB, extremos %s" % (rotulo, nt, os.path.getsize(saida) / 1e6,
          {k: [round(v[0], 1), round(v[1], 1)] for k, v in extremos.items()}))


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4])
