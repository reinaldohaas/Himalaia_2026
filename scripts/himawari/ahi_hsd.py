# -*- coding: utf-8 -*-
"""
Leitor minimo do formato HSD (Himawari Standard Data, JMA) para um segmento de banda infravermelha do
AHI, e geometria geoestacionaria (CGMS) para lat/lon <-> coluna/linha e correcao de paralaxe.

So numpy e biblioteca padrao. Referencia do formato: "Himawari-8/9 Himawari Standard Data User's Guide"
(JMA). Blocos usados: #2 (dimensoes), #3 (projecao), #5 (calibracao), #7 (segmento). Cada bloco comeca
com numero do bloco (uint8) e tamanho do bloco (uint16). Depois dos blocos de cabecalho vem a imagem
em contagens uint16 (linhas x colunas).
"""
import bz2
import struct

import numpy as np

R_EQ, R_POL, H_SAT = 6378.137, 6356.7523, 42164.0     # km (CGMS)


def ler_segmento(caminho):
    """devolve dict com tb (K, float32, linhas x colunas), primeira linha global, cfac, lfac, coff, loff,
    sub_lon, numero de colunas e linhas do disco inteiro na resolucao da banda"""
    raw = open(caminho, "rb").read()
    if caminho.endswith(".bz2"):
        raw = bz2.decompress(raw)
    off, blocos = 0, {}
    # bloco 1: tamanho total do cabecalho em bytes (uint32 no offset 70 do bloco 1)
    b1_len = struct.unpack_from("<H", raw, 1)[0]
    total_hdr = struct.unpack_from("<I", raw, 70)[0]
    while off < total_hdr:
        num = raw[off]; tam = struct.unpack_from("<H", raw, off + 1)[0]
        blocos[num] = raw[off:off + tam]; off += tam
    b2, b3, b5, b7 = blocos[2], blocos[3], blocos[5], blocos[7]
    ncol, nlin = struct.unpack_from("<HH", b2, 5)
    sub_lon = struct.unpack_from("<d", b3, 3)[0]
    cfac, lfac = struct.unpack_from("<II", b3, 11)
    coff, loff = struct.unpack_from("<ff", b3, 19)
    banda = struct.unpack_from("<H", b5, 3)[0]
    lam = struct.unpack_from("<d", b5, 5)[0]                      # um
    err_count, out_count = struct.unpack_from("<HH", b5, 15)
    gain, const = struct.unpack_from("<dd", b5, 19)
    c0, c1, c2, C0, C1, C2, cl, hp, kb = struct.unpack_from("<9d", b5, 35)
    seg_total, seg_num = b7[3], b7[4]
    lin0 = struct.unpack_from("<H", b7, 5)[0]
    cont = np.frombuffer(raw, dtype="<u2", count=ncol * nlin, offset=total_hdr).reshape(nlin, ncol).astype(np.float64)
    ruim = (cont == err_count) | (cont == out_count)
    rad = cont * gain + const                                      # W/(m2 sr um)
    lam_m = lam * 1e-6
    with np.errstate(divide="ignore", invalid="ignore"):
        te = hp * cl / (kb * lam_m) / np.log(2.0 * hp * cl ** 2 / (lam_m ** 5 * rad * 1e6) + 1.0)
        tb = c0 + c1 * te + c2 * te ** 2
    tb[ruim | ~np.isfinite(tb) | (rad <= 0)] = np.nan
    return {"tb": tb.astype(np.float32), "lin0": lin0, "ncol": ncol, "nlin": nlin, "cfac": cfac, "lfac": lfac,
            "coff": coff, "loff": loff, "sub_lon": sub_lon, "banda": banda, "lambda_um": lam,
            "segmento": (seg_num, seg_total)}


def ll2cl(lat, lon, sub_lon, cfac, lfac, coff, loff):
    """lat/lon (graus) -> coluna, linha (1-based, como no HSD) na projecao geoestacionaria normalizada"""
    la = np.radians(lat); lo = np.radians(np.asarray(lon) - sub_lon)
    c_lat = np.arctan((R_POL ** 2 / R_EQ ** 2) * np.tan(la))
    rl = R_POL / np.sqrt(1 - ((R_EQ ** 2 - R_POL ** 2) / R_EQ ** 2) * np.cos(c_lat) ** 2)
    r1 = H_SAT - rl * np.cos(c_lat) * np.cos(lo); r2 = -rl * np.cos(c_lat) * np.sin(lo); r3 = rl * np.sin(c_lat)
    rn = np.sqrt(r1 * r1 + r2 * r2 + r3 * r3)
    x = np.degrees(np.arctan(-r2 / r1)); y = np.degrees(np.arcsin(-r3 / rn))
    return coff + x * 2.0 ** -16 * cfac, loff + y * 2.0 ** -16 * lfac


def _ecef(lat, lon, alt_km=0.0):
    """esfera-elipsoide aproximada: raio geocentrico do elipsoide + altitude"""
    la, lo = np.radians(lat), np.radians(lon)
    c_lat = np.arctan((R_POL ** 2 / R_EQ ** 2) * np.tan(la))
    r = R_POL / np.sqrt(1 - ((R_EQ ** 2 - R_POL ** 2) / R_EQ ** 2) * np.cos(c_lat) ** 2) + alt_km
    return np.array([r * np.cos(c_lat) * np.cos(lo), r * np.cos(c_lat) * np.sin(lo), r * np.sin(c_lat)])


def paralaxe(lat_ap, lon_ap, h_km, sub_lon):
    """posicao verdadeira (lat, lon) de um topo a h_km que o satelite ve projetado em (lat_ap, lon_ap):
    ponto da linha de visada satelite->(lat_ap, lon_ap) na altitude h_km, levado verticalmente ao chao."""
    S = np.array([H_SAT * np.cos(np.radians(sub_lon)), H_SAT * np.sin(np.radians(sub_lon)), 0.0])
    G = _ecef(lat_ap, lon_ap)
    d = G - S
    Rg = np.linalg.norm(G) + h_km
    a = d @ d; b = 2 * S @ d; c = S @ S - Rg ** 2
    t = (-b - np.sqrt(b * b - 4 * a * c)) / (2 * a)               # primeira intersecao (lado do satelite)
    P = S + t * d
    lat_g = np.degrees(np.arcsin(P[2] / np.linalg.norm(P)))
    lat = np.degrees(np.arctan(np.tan(np.radians(lat_g)) * R_EQ ** 2 / R_POL ** 2))
    return float(lat), float(np.degrees(np.arctan2(P[1], P[0])))
