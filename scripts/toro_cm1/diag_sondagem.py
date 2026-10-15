# -*- coding: utf-8 -*-
"""CAPE/CIN/PWAT/LCL/LFC/EL, vento e cisalhamento de um input_sounding do CM1 (parcela de superficie, pseudoadiabatica)."""
import sys
import numpy as np

Rd, cp, g, Lv, eps = 287.04, 1004.5, 9.81, 2.501e6, 0.622


def ler(p):
    L = open(p).read().split("\n")
    ps, th0, q0 = [float(x) for x in L[0].split()]
    a = np.array([[float(x) for x in l.split()] for l in L[1:] if l.strip()])
    z = np.r_[0.0, a[:, 0]]; th = np.r_[th0, a[:, 1]]; qv = np.r_[q0, a[:, 2]] / 1000.
    u = np.r_[a[0, 3], a[:, 3]]; v = np.r_[a[0, 4], a[:, 4]]
    if a[0, 0] == 0.0:
        z, th, qv, u, v = z[1:], th[1:], qv[1:], u[1:], v[1:]
    # hidrostatica em pi (Exner) com theta_v
    thv = th * (1 + 0.61 * qv)
    pi = np.empty_like(z); pi[0] = (ps / 1000.) ** (Rd / cp)
    for k in range(1, len(z)):
        pi[k] = pi[k - 1] - g / cp * (z[k] - z[k - 1]) / (0.5 * (thv[k] + thv[k - 1]))
    p = 1000. * pi ** (cp / Rd); T = th * pi
    return z, p, T, qv, u, v


def es(T):
    return 6.112 * np.exp(17.67 * (T - 273.15) / (T - 29.65))


def qs(T, p):
    e = es(T); return eps * e / (p - e)


def parcela(z, p, T, qv):
    Tp = np.empty_like(T); Tp[0] = T[0]; q = qv[0]; sat = False; zlcl = np.nan
    for k in range(1, len(z)):
        dz = z[k] - z[k - 1]
        if not sat:
            Tt = Tp[k - 1] - g / cp * dz
            if q >= qs(Tt, p[k]):
                sat = True; zlcl = z[k - 1]
        if sat:
            # pseudoadiabatica: passo em subpassos
            t = Tp[k - 1]; n = 10
            for j in range(n):
                pj = p[k - 1] + (p[k] - p[k - 1]) * (j + .5) / n
                rs = qs(t, pj)
                gm = g * (1 + Lv * rs / (Rd * t)) / (cp + Lv * Lv * rs * eps / (Rd * t * t))
                t -= gm * dz / n
            Tp[k] = t; q = qs(t, p[k])
        else:
            Tp[k] = Tt
    qp = np.minimum(qv[0], qs(Tp, p))
    Tvp = Tp * (1 + 0.61 * qp); Tve = T * (1 + 0.61 * qv)
    b = g * (Tvp - Tve) / Tve
    return b, zlcl, Tp


def diag(path):
    z, p, T, qv, u, v = ler(path)
    b, zlcl, Tp = parcela(z, p, T, qv)
    dz = np.gradient(z)
    pos = b > 0
    # LFC = primeiro nivel positivo acima do LCL; EL = ultimo positivo
    idx = np.where(pos & (z >= np.nan_to_num(zlcl)))[0]
    if len(idx):
        lfc, el = z[idx[0]], z[idx[-1]]
        cape = np.sum((b * dz)[(z >= lfc) & (z <= el) & pos])
        cin = np.sum((b * dz)[(z < lfc) & (b < 0)])
    else:
        lfc = el = np.nan; cape = 0.0; cin = np.nan   # sem LFC: CIN indefinida
    rho = p * 100 / (Rd * T * (1 + 0.61 * qv))
    pw = np.sum(rho * qv * dz)
    def ui(zz): return np.interp(zz, z, u), np.interp(zz, z, v)
    u0, v0 = ui(0); u6, v6 = ui(6000)
    sh06 = np.hypot(u6 - u0, v6 - v0)
    # nivel de 0 C e camada super-resfriada (0 a -38 C) do ambiente
    z0 = np.interp(273.15, T[::-1], z[::-1]); z38 = np.interp(235.15, T[::-1], z[::-1])
    return dict(ps=p[0], Ts=T[0] - 273.15, qv=qv[0] * 1e3, CAPE=cape, CIN=cin, LCL=zlcl, LFC=lfc, EL=el,
                PWAT=pw, SH06=sh06, U500=np.hypot(*ui(np.interp(-np.log(500), -np.log(p), z))),
                z0C=z0, zm38=z38)


if __name__ == "__main__":
    print("%-16s %6s %6s %5s %7s %7s %6s %6s %6s %5s %5s %5s %6s %6s" % (
        "sondagem", "ps", "Ts", "qv", "CAPE", "CIN", "LCL", "LFC", "EL", "PWAT", "SH06", "U500", "z0C", "z-38"))
    for a in sys.argv[1:]:
        nome, path = a.split("=", 1)
        d = diag(path)
        print("%-16s %6.1f %6.1f %5.1f %7.0f %7.0f %6.0f %6.0f %6.0f %5.1f %5.1f %5.1f %6.0f %6.0f" % (
            nome, d["ps"], d["Ts"], d["qv"], d["CAPE"], d["CIN"], d["LCL"], d["LFC"], d["EL"], d["PWAT"],
            d["SH06"], d["U500"], d["z0C"], d["zm38"]))
