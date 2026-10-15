# -*- coding: utf-8 -*-
"""Leitor minimo de saida GrADS do CM1 (dset sequencial, float32 little-endian)."""
import os
import re
import numpy as np


def ctl(path):
    d = {"vars": []}
    with open(path, encoding="utf-8", errors="ignore") as f:
        linhas = f.read().splitlines()
    em_vars = False
    for ln in linhas:
        s = ln.strip()
        if not s:
            continue
        k = s.split()[0].lower()
        if em_vars:
            if k == "endvars":
                em_vars = False
                continue
            p = s.split()
            nlev = int(p[1])
            d["vars"].append((p[0], max(nlev, 1)))
            continue
        if k == "dset":
            d["dset"] = s.split()[1].lstrip("^")
        elif k == "undef":
            d["undef"] = float(s.split()[1])
        elif k in ("xdef", "ydef", "zdef"):
            p = s.split()
            n = int(p[1])
            if p[2].lower() == "linear":
                d[k] = float(p[3]) + float(p[4]) * np.arange(n)
            else:
                d[k] = np.array([float(x) for x in p[3:3 + n]])
        elif k == "tdef":
            d["nt"] = int(s.split()[1])
        elif k == "vars":
            em_vars = True
    return d


def ler(path_ctl, nomes=None):
    """devolve {var: array (nt, nz, ny, nx)} e o descritor"""
    d = ctl(path_ctl)
    nx, ny = len(d["xdef"]), len(d["ydef"])
    base = os.path.join(os.path.dirname(path_ctl), d["dset"])
    raw = np.fromfile(base, dtype="<f4")
    por_t = sum(nl * ny * nx for _, nl in d["vars"])
    nt = raw.size // por_t
    raw = raw[:nt * por_t].reshape(nt, por_t)
    out, off = {}, 0
    for nome, nl in d["vars"]:
        tam = nl * ny * nx
        if nomes is None or nome in nomes:
            a = raw[:, off:off + tam].reshape(nt, nl, ny, nx).astype(np.float64)
            a[a == d.get("undef", -999999.9)] = np.nan
            out[nome] = a
        off += tam
    d["nt_lido"] = nt
    return out, d


def stats(path_ctl):
    """series temporais do cm1out_stats: {var: array(nt)}"""
    o, d = ler(path_ctl)
    return {k: v[:, 0, 0, 0] for k, v in o.items()}, d
