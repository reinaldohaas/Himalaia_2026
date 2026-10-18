# -*- coding: utf-8 -*-
"""
Delineia, no Copernicus GLO-30, o anfiteatro do Lhende Khola: a bacia a montante do ponto em que o talvegue,
descendo do ponto de colapso (85,515 E; 28,271 N), chega ao fundo do vale a 4.010 m (~1,45 km; 3,39 km2 em
ANALISE_DEM_GLO30_E_AUSENCIA_DE_LAGO.md). Preenchimento de depressoes por priority-flood (epsilon), direcoes D8,
bacia por varredura de montante. Tambem grava os dois controles: o cume do Langtang Lirung (1 km2 em torno do
ponto mais alto a menos de 3 km) e o terreno acima de 5.800 m a menos de 6 km que nao drena para o anfiteatro.

Uso: python anfiteatro_glo30.py <dir_saida>   -> anfiteatro.geojson, controles.geojson, anfiteatro_meta.json
"""
import heapq
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

COTA_EXUTORIO = 4010.0


def main(saida):
    import rasterio
    from rasterio.features import shapes
    from shapely.geometry import box, shape, mapping, Point
    from shapely.ops import unary_union
    os.makedirs(saida, exist_ok=True)
    it = comum.stac_busca(comum.PC, ["cop-dem-glo-30"], [85.40, 28.18, 85.65, 28.38], "2000-01-01/2030-01-01")[0]
    href = comum.pc_assina(it["assets"]["data"]["href"], "cop-dem-glo-30")
    z, T, crs, nd = comum.ler_janela(href, box(85.30, 28.20, 85.62, 28.40), folga_m=0)
    z = z.astype(np.float64); ny, nx = z.shape
    lat = T.f + T.e * (np.arange(ny) + 0.5); lon = T.c + T.a * (np.arange(nx) + 0.5)
    dy = abs(T.e) * 111320.0; dxs = T.a * 111320.0 * np.cos(np.radians(lat))
    area = (dy * dxs)[:, None] * np.ones((1, nx))
    # priority-flood (Barnes et al. 2014) com epsilon
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
    # D8
    jd =np.full(z.shape, -1, int); id_ = np.full(z.shape, -1, int)
    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            melhor, bj, bi = 0.0, -1, -1
            for dj, di in viz:
                d = np.hypot(dj * dy, di * dxs[j])
                s = (fil[j, i] - fil[j + dj, i + di]) / d
                if s > melhor:
                    melhor, bj, bi = s, j + dj, i + di
            jd[j, i], id_[j, i] = bj, bi
    # desce do colapso ate 4.010 m
    j = int(np.argmin(abs(lat - comum.COLAPSO[1]))); i = int(np.argmin(abs(lon - comum.COLAPSO[0])))
    caminho = [(j, i)]; comp = 0.0
    while z[j, i] > COTA_EXUTORIO and jd[j, i] >= 0:
        nj, ni = jd[j, i], id_[j, i]; comp += np.hypot((nj - j) * dy, (ni - i) * dxs[j]); j, i = nj, ni; caminho.append((j, i))
    exu = (j, i)
    # percurso a jusante do exutorio ate a borda da janela (ou 25 km): o corredor do fluxo de detritos
    jus = [exu]; cj = 0.0; jj_, ii_ = exu
    while jd[jj_, ii_] >= 0 and cj < 25000:
        nj, ni = jd[jj_, ii_], id_[jj_, ii_]; cj += np.hypot((nj - jj_) * dy, (ni - ii_) * dxs[jj_]); jj_, ii_ = nj, ni; jus.append((jj_, ii_))
    # bacia: varredura de montante a partir do exutorio
    rev = {}
    for jj in range(1, ny - 1):
        for ii in range(1, nx - 1):
            if jd[jj, ii] >= 0:
                rev.setdefault((jd[jj, ii], id_[jj, ii]), []).append((jj, ii))
    bac = np.zeros(z.shape, bool); pilha = [exu]; bac[exu] = True
    while pilha:
        c = pilha.pop()
        for p in rev.get(c, []):
            if not bac[p]:
                bac[p] = True; pilha.append(p)
    a_km2 = float(area[bac].sum() / 1e6)
    pol = unary_union([shape(g) for g, v in shapes(bac.astype(np.uint8), mask=bac, transform=T) if v == 1])
    # controles
    jc, ic = int(np.argmin(abs(lat - comum.COLAPSO[1]))), int(np.argmin(abs(lon - comum.COLAPSO[0])))
    R = np.hypot((np.arange(ny)[:, None] - jc) * dy, (np.arange(nx)[None, :] - ic) * dxs[:, None])
    k = np.argmax(np.where(R < 3000, z, -1)); jt, it_ = np.unravel_index(k, z.shape)
    cume = box(lon[it_] - 0.0051, lat[jt] - 0.0045, lon[it_] + 0.0051, lat[jt] + 0.0045)   # ~1 km x 1 km
    alto = (z > 5800) & (R < 6000) & ~bac
    pol_alto = unary_union([shape(g) for g, v in shapes(alto.astype(np.uint8), mask=alto, transform=T) if v == 1]).difference(pol.buffer(0.002))
    json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {
        "nome": "anfiteatro", "area_km2": round(a_km2, 3), "exutorio_lon": float(lon[exu[1]]), "exutorio_lat": float(lat[exu[0]]),
        "exutorio_cota_m": float(z[exu]), "comprimento_talvegue_km": round(comp / 1000, 2),
        "cota_min_m": float(z[bac].min()), "cota_max_m": float(z[bac].max()), "cota_mediana_m": float(np.median(z[bac])),
        "frac_acima_5000m": round(float(area[bac & (z > 5000)].sum() / area[bac].sum()), 3)}, "geometry": mapping(pol)}]},
        open(os.path.join(saida, "anfiteatro.geojson"), "w"))
    json.dump({"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"nome": "cume_langtang_lirung", "cota_max_m": float(z[jt, it_]), "lon": float(lon[it_]), "lat": float(lat[jt])}, "geometry": mapping(cume)},
        {"type": "Feature", "properties": {"nome": "alto_fora_anfiteatro", "criterio": "z > 5.800 m, a menos de 6 km do colapso, fora do anfiteatro",
                                            "area_km2": round(float(area[alto].sum() / 1e6), 2)}, "geometry": mapping(pol_alto)}]},
        open(os.path.join(saida, "controles.geojson"), "w"))
    from shapely.geometry import LineString
    from shapely.ops import substring
    lin = LineString([(float(lon[b]), float(lat[a])) for a, b in jus])
    dist_acum = np.concatenate([[0], np.cumsum([np.hypot((jus[k + 1][0] - jus[k][0]) * dy, (jus[k + 1][1] - jus[k][1]) * dxs[jus[k][0]]) for k in range(len(jus) - 1)])])
    feats = []
    for a0, a1 in ((0, 5000), (5000, 10000), (10000, 15000), (15000, 25000)):
        sel = [k for k in range(len(jus)) if a0 <= dist_acum[k] <= a1]
        if len(sel) < 2:
            continue
        seg = LineString([lin.coords[k] for k in sel])
        feats.append({"type": "Feature", "properties": {"nome": "corredor_%02d_%02dkm" % (a0 // 1000, a1 // 1000), "km_ini": a0 / 1000, "km_fim": round(min(a1, dist_acum[-1]) / 1000, 2),
                      "cota_ini_m": float(z[jus[sel[0]]]), "cota_fim_m": float(z[jus[sel[-1]]])}, "geometry": mapping(seg.buffer(0.0025))})   # ~250 m de cada lado
    comp_ = caminho + jus[1:]     # do ponto de colapso ao fim do corredor
    dc = np.concatenate([[0], np.cumsum([np.hypot((comp_[k + 1][0] - comp_[k][0]) * dy, (comp_[k + 1][1] - comp_[k][1]) * dxs[comp_[k][0]]) for k in range(len(comp_) - 1)])])
    feats.append({"type": "Feature", "properties": {"nome": "talvegue_completo", "origem": "ponto de colapso", "km_exutorio": round(comp / 1000, 3),
                  "dist_m": [round(float(x), 1) for x in dc], "cota_m": [float(z[c]) for c in comp_]},
                  "geometry": mapping(LineString([(float(lon[b]), float(lat[a])) for a, b in comp_]))})
    feats.append({"type": "Feature", "properties": {"nome": "talvegue_jusante", "comprimento_km": round(dist_acum[-1] / 1000, 2)}, "geometry": mapping(lin)})
    json.dump({"type": "FeatureCollection", "features": feats}, open(os.path.join(saida, "corredor.geojson"), "w"))
    print("talvegue a jusante: %.1f km, de %.0f m a %.0f m, termina em %.4fE %.4fN" % (dist_acum[-1] / 1000, z[exu], z[jus[-1]], lon[jus[-1][1]], lat[jus[-1][0]]))
    print("anfiteatro: %.3f km2 (referencia 3,39); exutorio %.4fE %.4fN a %.0f m, %.2f km de talvegue; cotas %.0f-%.0f m, mediana %.0f, %.0f%% acima de 5.000 m" % (
        a_km2, lon[exu[1]], lat[exu[0]], z[exu], comp / 1000, z[bac].min(), z[bac].max(), np.median(z[bac]), 100 * area[bac & (z > 5000)].sum() / area[bac].sum()))
    print("cume: %.0f m em %.4fE %.4fN; alto fora do anfiteatro: %.1f km2" % (z[jt, it_], lon[it_], lat[jt], area[alto].sum() / 1e6))


if __name__ == "__main__":
    main(sys.argv[1])
