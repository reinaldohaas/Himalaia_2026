# -*- coding: utf-8 -*-
"""
Checagens da janela 18 UTC -> 03 UTC (colapso as 02:52 UTC de 26/08) nas rodadas rad_06utc e rad_12utc.
Roda NO VLAB, sobre os campos 3D, e imprime so texto (nao precisa trazer os brutos).

Para cada saida (30 min):
  A) artefato numerico: pontos com w > 10 m/s; fracao a menos de 1 km do solo; w max, altura acima
     do solo, posicao e declividade do terreno ali.
  B) comparacao com o Himawari-9 B13 (10,4 um):
     temperatura de topo "equivalente IR" em cada coluna = temperatura do nivel em que a agua
     condensada acumulada de cima para baixo atinge 15 g/m2 (gelo ~ tau_IR 1); se nunca atinge,
     usa a temperatura da superficie (tsk). E uma aproximacao (sem transferencia radiativa).
     Reporta: Tb_eq no sitio (celula central), Tb_eq minima e area com Tb_eq < 213 K e < 240 K.
     Observado (Himawari, caixa de 150 km): 18 UTC 8.413 km2 < 213 K; 21 UTC 4.892; 00 UTC 810;
     02:50 UTC 0 km2 < 213 K, e 272,7 K sobre o sitio.  O dominio do modelo tem 40 x 40 km = 1.600 km2.
  C) colunas sobre o anfiteatro (3 x 3 km): agua liquida, gelo (kg/m2) e agua liquida com T < 0 C.

Uso:  cd pos && python checar_janela.py [rad_06utc rad_12utc]
"""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads

POS = os.path.dirname(os.path.abspath(__file__))
ZBASE, DX, TAP = 3000.0, 500.0, 1800.0
H0 = {"rad_06utc": 6.0, "rad_12utc": 12.0}
LIMIAR_GM2 = 15.0          # g/m2 de condensado (de cima para baixo) que define o "topo IR"


def um(run):
    d = os.path.join(POS, run)
    if not os.path.isdir(d):
        d = os.path.join(POS, "..", "execucoes", run)
    s, dd = grads.ler(os.path.join(d, "cm1out_s.ctl"),
                      ["zs", "zhval", "th", "prs", "rho", "qc", "qr", "qi", "qs", "qg", "winterp", "tsk"])
    x = dd["xdef"]; X, Y = np.meshgrid(x, x)
    anf = (abs(X) <= 1.5) & (abs(Y) <= 1.5)
    ic = np.argmin(abs(x))                                  # celula central (ponto do colapso)
    zs = s["zs"][0, 0] + ZBASE
    gy, gx = np.gradient(zs, DX); inc = np.degrees(np.arctan(np.hypot(gx, gy)))
    nt = s["th"].shape[0]
    print("\n================ %s  (%d saidas)" % (run, nt))
    print(" UTC  | n(w>10) %<1kmAGL  wmax  zAGL  x,y(km) incl | Tb_sitio Tb_min A<213 A<240 (km2) | anf: liq gelo SLW (kg/m2)")
    for t in range(nt):
        hh = (H0[run] + t * TAP / 3600.0)
        if hh < 18:
            continue
        zh = s["zhval"][t] + ZBASE
        agl = zh - zs[None]
        w = s["winterp"][t]
        forte = w > 10
        n = int(forte.sum())
        frac = 100.0 * (agl[forte] < 1000).mean() if n else 0.0
        k, j, i = np.unravel_index(np.nanargmax(w), w.shape)
        T = s["th"][t] * (s["prs"][t] / 1e5) ** 0.2857
        rho = s["rho"][t]
        dz = np.clip(np.gradient(zh, axis=0), 1, None)
        liq = (s["qc"][t] + s["qr"][t]) * rho * dz            # kg/m2 por camada
        gel = (s["qi"][t] + s["qs"][t] + s["qg"][t]) * rho * dz
        cond = (liq + gel)[::-1] * 1000.0                      # g/m2, de cima para baixo
        acum = np.cumsum(cond, axis=0)
        atinge = acum >= LIMIAR_GM2
        kk = np.argmax(atinge, axis=0)                         # primeiro nivel (de cima) que atinge
        Ttop = np.take_along_axis(T[::-1], kk[None], axis=0)[0]
        tb = np.where(atinge.any(axis=0), Ttop, s["tsk"][t, 0])
        a213 = (tb < 213).sum() * DX * DX / 1e6
        a240 = (tb < 240).sum() * DX * DX / 1e6
        L = liq.sum(axis=0); G = gel.sum(axis=0); SLW = np.where(T < 273.15, liq, 0).sum(axis=0)
        print(" %5.2f | %6d %7.0f%% %5.1f %5.0f %5.1f,%5.1f %4.0f | %7.1f %6.1f %5.0f %5.0f       | %5.2f %5.2f %5.3f"
              % (hh % 24, n, frac, w[k, j, i], agl[k, j, i], x[i], x[j], inc[j, i],
                 tb[ic, ic], np.nanmin(tb), a213, a240,
                 L[anf].mean(), G[anf].mean(), SLW[anf].mean()))


if __name__ == "__main__":
    for r in (sys.argv[1:] or ["rad_06utc", "rad_12utc"]):
        try:
            um(r)
        except Exception as e:
            print(r, "ERRO", e)
