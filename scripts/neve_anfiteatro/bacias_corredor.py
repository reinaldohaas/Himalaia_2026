# -*- coding: utf-8 -*-
"""
Area de contribuicao (GLO-30, priority-flood + D8 vetorizado) em pontos do talvegue do Lhende Khola
(corredor.geojson: talvegue_completo), para converter o volume de agua do repositorio (14,2 x 10^6 m3, Manning,
premissa) em lamina equivalente sobre cada bacia. Avisa se a bacia toca a borda da janela do DEM (area truncada).
Uso: python bacias_corredor.py <dir_dados>
"""
import heapq
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

KM = (1.68, 5.0, 10.0, 15.0, 20.0, 25.0)
VOL = 14.2e6


def main(d):
    from shapely.geometry import box
    it = comum.stac_busca(comum.PC, ["cop-dem-glo-30"], [85.40, 28.18, 85.65, 28.38], "2000-01-01/2030-01-01")[0]
    href = comum.pc_assina(it["assets"]["data"]["href"])
    z, T, crs, nd = comum.ler_janela(href, box(85.22, 28.12, 85.75, 28.62), folga_m=0)
    z = z.astype(np.float64); ny, nx = z.shape
    lat = T.f + T.e * (np.arange(ny) + 0.5); lon = T.c + T.a * (np.arange(nx) + 0.5)
    dy = abs(T.e) * 111320.0; dxs = T.a * 111320.0 * np.cos(np.radians(lat))
    area = (dy * dxs)[:, None] * np.ones((1, nx))
    fil = z.copy(); vis = np.zeros(z.shape, bool); h = []
    for j in range(ny):
        for i in (0, nx - 1):
            heapq.heappush(h, (fil[j, i], j, i)); vis[j, i] = True
    for i in range(1, nx - 1):
        for j in (0, ny - 1):
            heapq.heappush(h, (fil[j, i], j, i)); vis[j, i] = True
    viz = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while h:
        e, j, i = heapq.heappop(h)
        for dj, di in viz:
            jj, ii = j + dj, i + di
            if 0 <= jj < ny and 0 <= ii < nx and not vis[jj, ii]:
                vis[jj, ii] = True
                if fil[jj, ii] <= e:
                    fil[jj, ii] = e + 1e-3
                heapq.heappush(h, (fil[jj, ii], jj, ii))
    # D8 vetorizado
    best = np.zeros(z.shape); bj = np.full(z.shape, -1); bi = np.full(z.shape, -1)
    J, I = np.mgrid[0:ny, 0:nx]
    for dj, di in viz:
        sj = np.clip(J + dj, 0, ny - 1); si = np.clip(I + di, 0, nx - 1)
        dist = np.hypot(dj * dy, di * dxs[:, None] * np.ones((1, nx)))
        s = (fil - fil[sj, si]) / dist
        m = s > best
        best[m] = s[m]; bj[m] = sj[m]; bi[m] = si[m]
    for a in (0, ny - 1):
        bj[a, :] = -1
    for a in (0, nx - 1):
        bj[:, a] = -1
    # acumulacao por ordem de cota decrescente
    ordem = np.argsort(-fil, axis=None)
    acc = area.ravel().copy(); alvo = np.where(bj.ravel() >= 0, bj.ravel() * nx + bi.ravel(), -1)
    for k in ordem:
        t = alvo[k]
        if t >= 0:
            acc[t] += acc[k]
    acc = acc.reshape(z.shape)
    tal = [f for f in json.load(open(os.path.join(d, "corredor.geojson")))["features"] if f["properties"]["nome"] == "talvegue_completo"][0]
    xy = np.array(tal["geometry"]["coordinates"]); dist = np.array(tal["properties"]["dist_m"])
    res = []
    for km in KM:
        k = int(np.argmin(abs(dist - km * 1000)))
        j = int(np.argmin(abs(lat - xy[k, 1]))); i = int(np.argmin(abs(lon - xy[k, 0])))
        # o maior acumulado num raio de 2 pixels (o talvegue do DEM menor pode estar deslocado de 1 pixel)
        jj, ii = np.unravel_index(np.argmax(acc[max(j - 2, 0):j + 3, max(i - 2, 0):i + 3]), (min(j + 3, ny) - max(j - 2, 0), min(i + 3, nx) - max(i - 2, 0)))
        j += jj - min(j, 2); i += ii - min(i, 2)
        # bacia: varredura de montante para checar se toca a borda
        rev_alvo = alvo.reshape(z.shape)
        bac = np.zeros(z.shape, bool); bac[j, i] = True
        mud = True
        flat = j * nx + i
        sel = np.zeros(ny * nx, bool); sel[flat] = True
        for _ in range(4000):
            novo = (~sel) & (alvo >= 0) & sel[np.clip(alvo, 0, None)]
            if not novo.any():
                break
            sel |= novo
        bac = sel.reshape(z.shape)
        borda = bool(bac[0, :].any() or bac[-1, :].any() or bac[:, 0].any() or bac[:, -1].any())
        a = float(area[bac].sum())
        r = {"km": km, "lon": round(float(lon[i]), 4), "lat": round(float(lat[j]), 4), "cota_m": float(z[j, i]), "area_km2": round(a / 1e6, 2),
             "toca_borda": borda, "lamina_mm_para_14_2Mm3": round(VOL / a * 1000, 1), "frac_acima_5000m": round(float(area[bac & (z > 5000)].sum() / a), 3)}
        res.append(r); print(r)
    json.dump(res, open(os.path.join(d, "bacias_corredor.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
