# -*- coding: utf-8 -*-
"""
Diagnostico de vortices de sotavento numa rodada do CM1 com terreno (saida GrADS, cm1out_s).

Para cada saida (30 min):
  * interpola uinterp, vinterp, winterp a alturas constantes ASL (Z_NIVEIS) e mascara o que esta
    abaixo do relevo + 100 m;
  * calcula vorticidade vertical zeta = dv/dx - du/dy, divergencia delta = du/dx + dv/dy e o parametro
    de Okubo-Weiss OW = sn^2 + ss^2 - zeta^2 (OW < 0: rotacao domina o cisalhamento/deformacao);
  * vortice = regiao conexa com |zeta| >= ZETA_MIN e OW < 0, area >= 2 celulas (0,5 km^2);
    "orografico" se o |w| maximo na regiao < W_CONV (senao: ligado a conveccao);
    persistencia: mesmo sinal a menos de 2,5 km de um vortice da saida anterior;
  * janela do anfiteatro (|x|,|y| <= 1,5 km): zeta, delta e w medios por nivel;
  * regime: vento medio do dominio em 5-6 km, N em 4-7 km (perfil medio de theta), Fr = U / (N H), H = 2 km.

Uso: python3 vortices_sotavento.py <dir_rodada> <hora_inicial_UTC> <saida_prefixo> [rotulo]
Grava <prefixo>.json, <prefixo>.txt (tabela) e <prefixo>.png (mapas a 5,5 km).
So le a rodada; nao altera nada.
"""
import json
import os
import sys

import numpy as np
try:
    from scipy import ndimage
    rotular = ndimage.label
except ImportError:                                  # sem scipy: rotulacao 4-conexa simples
    def rotular(m):
        lab = np.zeros(m.shape, int); n = 0
        for j0, i0 in zip(*np.nonzero(m)):
            if lab[j0, i0]:
                continue
            n += 1; pilha = [(j0, i0)]; lab[j0, i0] = n
            while pilha:
                j, i = pilha.pop()
                for jj, ii in ((j + 1, i), (j - 1, i), (j, i + 1), (j, i - 1)):
                    if 0 <= jj < m.shape[0] and 0 <= ii < m.shape[1] and m[jj, ii] and not lab[jj, ii]:
                        lab[jj, ii] = n; pilha.append((jj, ii))
        return lab, n

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads  # noqa: E402

ZBASE = 3000.0                      # base do modelo (m ASL)
Z_NIVEIS = [4500.0, 5000.0, 5500.0, 6000.0, 7000.0]
ZETA_MIN = 1.0e-3                   # s^-1 (~15 f)
W_CONV = 2.0                        # m/s
F_COR = 2 * 7.292e-5 * np.sin(np.radians(28.271))
DX = 500.0
H_OBST = 2000.0


def abrir(ctl_path):
    d = grads.ctl(ctl_path)
    nx, ny = len(d["xdef"]), len(d["ydef"])
    por_t = sum(nl * ny * nx for _, nl in d["vars"])
    mm = np.memmap(os.path.join(os.path.dirname(ctl_path), d["dset"]), dtype="<f4", mode="r")
    nt = mm.size // por_t
    off, idx = 0, {}
    for nome, nl in d["vars"]:
        idx[nome] = (off, nl)
        off += nl * ny * nx

    def campo(nome, t):
        o, nl = idx[nome]
        a = np.asarray(mm[t * por_t + o: t * por_t + o + nl * ny * nx], dtype=np.float64)
        return a.reshape(nl, ny, nx) if nl > 1 else a.reshape(ny, nx)
    return d, nt, campo


def interp_z(f3, zh3, z0):
    """interpola f3 (nz,ny,nx) para a altura z0 (m ASL); NaN fora da coluna"""
    acima = zh3 >= z0
    k = np.argmax(acima, axis=0)                       # primeiro nivel >= z0
    ok = acima.any(axis=0) & (k > 0)
    k1 = np.clip(k, 1, zh3.shape[0] - 1); k0 = k1 - 1
    z0a = np.take_along_axis(zh3, k0[None], 0)[0]; z1a = np.take_along_axis(zh3, k1[None], 0)[0]
    f0 = np.take_along_axis(f3, k0[None], 0)[0]; f1 = np.take_along_axis(f3, k1[None], 0)[0]
    w = (z0 - z0a) / np.where(z1a > z0a, z1a - z0a, 1.0)
    out = f0 + w * (f1 - f0)
    out[~ok] = np.nan
    return out


def cinematica(u, v):
    dudy, dudx = np.gradient(u, DX)
    dvdy, dvdx = np.gradient(v, DX)
    zeta = dvdx - dudy
    delta = dudx + dvdy
    sn = dudx - dvdy; ss = dvdx + dudy
    ow = sn ** 2 + ss ** 2 - zeta ** 2
    return zeta, delta, ow


def main(d_run, h0, prefixo, rotulo=""):
    d, nt, campo = abrir(os.path.join(d_run, "cm1out_s.ctl"))
    x = d["xdef"]; y = d["ydef"]
    X, Y = np.meshgrid(x, y)
    zs = campo("zs", 0) + ZBASE
    anf = (np.abs(X) <= 1.5) & (np.abs(Y) <= 1.5)
    horas, linhas, regs = [], [], []
    mapas = {}
    ant = []                                            # vortices da saida anterior (5,5 km)
    persist = {}
    for t in range(nt):
        h = h0 + 0.5 * t
        zh = campo("zhval", t) + ZBASE
        u3, v3, w3, th3 = (campo(n, t) for n in ("uinterp", "vinterp", "winterp", "th"))
        reg = {"hora_utc": h, "niveis": {}}
        # regime
        cam = (zh >= 5000) & (zh <= 6000)
        U = float(np.nanmean(np.where(cam, u3, np.nan))); V = float(np.nanmean(np.where(cam, v3, np.nan)))
        th_lo = np.nanmean(np.where((zh >= 3900) & (zh <= 4100), th3, np.nan))
        th_hi = np.nanmean(np.where((zh >= 6900) & (zh <= 7100), th3, np.nan))
        N = float(np.sqrt(max(9.81 / (0.5 * (th_lo + th_hi)) * (th_hi - th_lo) / 3000.0, 0.0)))
        spd = float(np.hypot(U, V))
        reg.update({"U": U, "V": V, "vel": spd, "dir_de": float((np.degrees(np.arctan2(-U, -V)) + 360) % 360),
                    "N": N, "Fr": spd / (N * H_OBST) if N > 0 else None})
        for z0 in Z_NIVEIS:
            u = interp_z(u3, zh, z0); v = interp_z(v3, zh, z0); w = interp_z(w3, zh, z0)
            abaixo = zs + 100.0 > z0
            for a in (u, v, w):
                a[abaixo] = np.nan
            zeta, delta, ow = cinematica(u, v)
            ok = np.isfinite(zeta)
            mask = ok & (np.abs(np.nan_to_num(zeta)) >= ZETA_MIN) & (np.nan_to_num(ow) < 0)
            lab, nlab = rotular(mask)
            vort = []
            for i in range(1, nlab + 1):
                m = lab == i
                if m.sum() < 2:
                    continue
                zz = zeta[m]; k = np.argmax(np.abs(zz))
                xc = float(np.average(X[m], weights=np.abs(zz))); yc = float(np.average(Y[m], weights=np.abs(zz)))
                wmax = float(np.nanmax(np.abs(w[m]))) if np.isfinite(w[m]).any() else float("nan")
                vort.append({"x": round(xc, 2), "y": round(yc, 2), "area_km2": float(m.sum() * 0.25),
                             "zeta_f": round(float(zz[k]) / F_COR, 1), "sinal": "ciclonico" if zz[k] > 0 else "anticiclonico",
                             "dist_anf_km": round(float(np.hypot(xc, yc)), 2), "w_max": round(wmax, 2),
                             "tipo": "orografico" if wmax < W_CONV else "convectivo"})
            vort.sort(key=lambda r: -abs(r["zeta_f"]))
            na = int(anf.sum())
            janela = {"cobertura": float(np.isfinite(zeta[anf]).sum() / na),
                      "zeta_f": float(np.nanmean(zeta[anf]) / F_COR) if np.isfinite(zeta[anf]).any() else None,
                      "delta_1e4": float(np.nanmean(delta[anf]) * 1e4) if np.isfinite(delta[anf]).any() else None,
                      "w": float(np.nanmean(w[anf])) if np.isfinite(w[anf]).any() else None}
            if z0 == 5500.0:
                for r in vort:
                    r["persist"] = 1 + max([p["persist"] for p in ant
                                            if p["sinal"] == r["sinal"] and np.hypot(p["x"] - r["x"], p["y"] - r["y"]) < 2.5] or [0])
                ant = vort
                if t % 2 == 0:
                    mapas[t] = (zeta / F_COR, u, v)
            reg["niveis"][str(int(z0))] = {"vortices": vort, "anfiteatro": janela,
                                           "n_orog": sum(r["tipo"] == "orografico" for r in vort),
                                           "n_conv": sum(r["tipo"] == "convectivo" for r in vort),
                                           "zeta_f_p99": float(np.nanpercentile(np.abs(zeta), 99) / F_COR) if ok.any() else None}
        regs.append(reg)
        n55 = reg["niveis"]["5500"]; a55 = n55["anfiteatro"]
        orog = [r for r in n55["vortices"] if r["tipo"] == "orografico"]
        top = orog[0] if orog else None
        linhas.append("%5.1f  %4.1f %3.0f  %.4f %5.2f | %2d orog %2d conv | %s | anf: zeta/f %s  conv %s  w %s" % (
            h % 24, spd, reg["dir_de"], N, reg["Fr"] or 0, n55["n_orog"], n55["n_conv"],
            ("mais forte orog: %+6.1f f, %4.2f km2, a %4.1f km, w %4.1f, persist %d" % (
                top["zeta_f"], top["area_km2"], top["dist_anf_km"], top["w_max"], top["persist"])) if top else "nenhum vortice orografico".ljust(66),
            "%+5.1f" % a55["zeta_f"] if a55["zeta_f"] is not None else "  -  ",
            "%+5.1f" % (-a55["delta_1e4"]) if a55["delta_1e4"] is not None else "  -  ",
            "%+4.2f" % a55["w"] if a55["w"] is not None else " -  "))
        print(linhas[-1], flush=True)
    cab = ("UTC   vel  dir  N      Fr    | vortices a 5,5 km (|zeta|>=%.0e, OW<0)    | " % ZETA_MIN +
           "vortice orografico mais forte (zeta/f, area, dist. ao anfiteatro, |w| max, saidas seguidas)        | " +
           "janela 3x3 km a 5,5 km: zeta/f, convergencia (1e-4 s-1), w (m/s)")
    txt = "Vortices de sotavento -- %s (%s)\nf = %.2e s-1; vento medio 5-6 km; N 4-7 km; Fr = U/(N*%.0f m)\n\n%s\n%s\n" % (
        rotulo, d_run, F_COR, H_OBST, cab, "\n".join(linhas))
    open(prefixo + ".txt", "w", encoding="utf-8").write(txt)
    json.dump({"rotulo": rotulo, "dir": d_run, "f": F_COR, "zeta_min": ZETA_MIN, "w_conv": W_CONV,
               "niveis_m": Z_NIVEIS, "saidas": regs}, open(prefixo + ".json", "w"), indent=1)
    figura(prefixo + ".png", mapas, x, y, zs, h0, rotulo)
    print("gravado:", prefixo + ".{txt,json,png}")


def figura(arq, mapas, x, y, zs, h0, rotulo):
    os.environ["MPLBACKEND"] = "Agg"        # o Jupyter exporta um backend inline que o matplotlib fora dele recusa
    try:
        import matplotlib
        matplotlib.use("Agg")
    except Exception as e:                 # sem matplotlib (ou backend invalido): tabelas ficam, figura nao
        print("figura nao gerada:", e); return
    import matplotlib.pyplot as plt
    alvo = [h for h in (8.0, 14.0, 18.0, 21.0, 24.0, 26.5) if int(round((h - h0) * 2)) in mapas]
    if not alvo:
        return
    fig, axs = plt.subplots(2, 3, figsize=(15, 9.6), constrained_layout=True)
    for ax, h in zip(axs.flat, alvo):
        t = int(round((h - h0) * 2)); z, u, v = mapas[t]
        pc = ax.pcolormesh(x, y, z, cmap="RdBu_r", vmin=-60, vmax=60, shading="auto")
        ax.contour(x, y, zs, levels=np.arange(3500, 7001, 500), colors="k", linewidths=0.4, alpha=0.6)
        ax.contour(x, y, zs, levels=[5500], colors="k", linewidths=1.2)
        s = 4
        ax.quiver(x[::s], y[::s], u[::s, ::s], v[::s, ::s], scale=120, width=0.0025, color="0.15")
        ax.add_patch(plt.Rectangle((-1.5, -1.5), 3, 3, fill=False, ec="lime", lw=1.6))
        ax.plot(0, 0, "o", ms=4, color="lime")
        ax.set_title("%02d:%02d UTC  (5,5 km ASL)" % (int(h % 24), int(round((h % 1) * 60))), fontsize=11)
        ax.set_aspect("equal"); ax.set_xlim(-20, 20); ax.set_ylim(-20, 20)
    for ax in list(axs.flat)[len(alvo):]:
        ax.axis("off")
    fig.colorbar(pc, ax=axs, shrink=0.6, label="vorticidade vertical / f   (f = %.1e s$^{-1}$)" % F_COR)
    fig.suptitle("%s: vorticidade vertical a 5,5 km ASL, vento (setas), relevo (contornos de 500 m; grosso = 5,5 km), "
                 "anfiteatro (quadrado verde)" % rotulo, fontsize=11)
    fig.savefig(arq, dpi=110)


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
