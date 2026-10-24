# -*- coding: utf-8 -*-
"""
Relevo do Copernicus GLO-30 no formato binario do geogrid do WPS (dataset "continuous", regular_ll), para o d04 de
333 m sobre o macico do Langtang Lirung / Tsangbu Ri (teste de estabilidade, 24/10/2026).
Resolucao 3" (0,000833333 graus, ~90 m) por media de area; caixa 28,08-28,48 N, 85,30-85,75 E (o d04 vai de
28,141/85,374 a 28,416/85,676). Um unico tile, inteiro de 2 bytes big-endian, linhas de sul para norte.
Saida: <dir>/index e <dir>/00001-NNNNN.00001-MMMMM
Uso: python glo30_geogrid.py <dir_saida>
"""
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "neve_anfiteatro"))
from comum import stac_busca, pc_assina, ler_janela, PC

S, N, W, E = 28.08, 28.48, 85.30, 85.75
RES = 3.0 / 3600.0


def main(saida):
    from shapely.geometry import box
    from rasterio.warp import reproject, Resampling
    from affine import Affine
    os.makedirs(saida, exist_ok=True)
    nx = int(round((E - W) / RES)); ny = int(round((N - S) / RES))
    tr = Affine(RES, 0, W, 0, -RES, N)                  # linha 0 = norte
    z = np.full((ny, nx), np.nan, np.float32)
    g = box(W - 0.02, S - 0.02, E + 0.02, N + 0.02)
    for f in stac_busca(PC, ["cop-dem-glo-30"], list(g.bounds), "2000-01-01/2030-01-01"):
        a, ta, ca, nd = ler_janela(pc_assina(f["assets"]["data"]["href"], "cop-dem-glo-30"), g, folga_m=0)
        out = np.full((ny, nx), np.nan, np.float32)
        reproject(a.astype(np.float32), out, src_transform=ta, src_crs=ca, dst_transform=tr, dst_crs="EPSG:4326",
                  resampling=Resampling.average, src_nodata=nd, dst_nodata=np.nan)
        z = np.where(np.isfinite(out), out, z)
    assert np.isfinite(z).all(), "GLO-30 nao cobriu a caixa"
    z = np.rint(z[::-1, :]).astype(">i2")               # linhas de sul para norte (row_order = bottom_top)
    nome = "%05d-%05d.%05d-%05d" % (1, nx, 1, ny)
    z.tofile(os.path.join(saida, nome))
    open(os.path.join(saida, "index"), "w", newline="\n").write(
        "type = continuous\nsigned = yes\nprojection = regular_ll\n"
        "dx = %.9f\ndy = %.9f\nknown_x = 1.0\nknown_y = 1.0\nknown_lat = %.9f\nknown_lon = %.9f\n"
        "wordsize = 2\nendian = big\nrow_order = bottom_top\ntile_x = %d\ntile_y = %d\ntile_z = 1\n"
        "missing_value = -32768\nunits = \"meters MSL\"\ndescription = \"Copernicus GLO-30 media de area a 3 s\"\n"
        % (RES, RES, S + RES / 2, W + RES / 2, nx, ny))
    print("tile", nome, "max %.0f m, min %.0f m" % (z.max(), z.min()))


if __name__ == "__main__":
    main(sys.argv[1])
