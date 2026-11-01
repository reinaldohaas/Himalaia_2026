# -*- coding: utf-8 -*-
"""
Recorte e criterios C1-C5 do ensemble no d03 (scripts/toro_wrf/LEIA-ME_toro_wrf.md, secao "Ensemble no d03").

O recorte guarda, de cada rodada, o que os criterios e as figuras precisam, para que os wrfout possam sair do disco:
  * 3D numa caixa de 31 x 31 pontos do d03 (+-15 km) centrada na frente de gelo, de 25/08 20:00 a 26/08 03:00 (15 min);
  * 2D do d03 inteiro na mesma janela (OLR e precipitacao acumulada por especie);
  * sha1 de T, QCLOUD e W (d03) e de T e QCLOUD (d02) em todos os instantes, para conferir as identidades bit a bit
    (A = S antes de 17:00, S = E2 antes de 22:00, S = R antes de 23:30) sem guardar os campos inteiros.

  python3 criterios_ens_d03.py recorte <pasta_da_rodada> <saida.npz>        uma rodada (serve tambem para toro_A..D)
  python3 criterios_ens_d03.py tudo <ens_d03> <pasta_saida>                 recorta as rodadas com SUCCESS que ainda nao
                                                                            tem .npz e escreve os criterios de todas
  python3 criterios_ens_d03.py criterios <pasta_com_os_npz> <pasta_saida>   so os criterios (A_m1.npz, S_m1.npz, ...)

Le com netCDF4, h5py ou scipy (o que houver); nao instala nada.
Interpretacoes fixadas aqui (o texto dos criterios nao as decide):
  * C2: fracao congelada em 30 min = max(0, min(-dSLW, dGELO)) / SLW(t), em janelas moveis de 30 min a partir de 00:00
    (E2: nucleacao no nucleo, t_vn_ini = 24) e de 23:30 (R: t_rel); S e A na mesma janela, como referencia.
  * C4: 02:35 nao e instante de saida; o acumulado e interpolado linearmente entre 02:30 e 02:45.
  * C5: OLR medio ate 5 km do ponto do drone em cada instante; a) o menor de 22:00 a 00:30 <= 175 W/m2;
    b) o menor de 02:00 a 02:45 (ultimo instante <= 02:50) >= 280 W/m2.
"""
import glob
import hashlib
import json
import math
import os
import re
import sys

import numpy as np

FRENTE = (28.2918, 85.5284)       # frente de gelo do quadro do Xinhua (data/processed/gelo_xinhua/gelo_xinhua.json)
DRONE = (28.293985, 85.523964)    # ponto do drone
A_BACIA = 1.19e6                  # m2, bacia do Lhende Khola acima do ponto de ruptura
MEIA = 15                         # meia-largura da caixa 3D, em pontos do d03 (1 km)
INI, FIM = "2026-08-25_20:00:00", "2026-08-26_03:00:00"
V3D = ["QVAPOR", "QCLOUD", "QNDROP", "QRAIN", "QNRAIN", "QICE", "QNICE", "QSNOW", "QNSNOW", "QGRAUP", "QNGRAUPEL",
       "QVGRAUPEL", "QHAIL", "QNHAIL", "QVHAIL", "T", "P", "PB", "PH", "PHB", "W", "U", "V"]
V2D = ["OLR", "GRAUPELNC", "HAILNC", "SNOWNC", "RAINNC"]
HASH_D03 = ["T", "QCLOUD", "W"]
HASH_D02 = ["T", "QCLOUD"]
RD, CP, G = 287.04, 1004.5, 9.81
CORTES = {("A", "S"): "2026-08-25_17:00:00", ("S", "E2"): "2026-08-25_22:00:00", ("S", "R"): "2026-08-25_23:30:00"}
T0_C2 = {"E2": "2026-08-26_00:00:00", "R": "2026-08-25_23:30:00"}


class Nc:
    """Leitura minima de netCDF: netCDF4, h5py (netCDF4/HDF5) ou scipy (netCDF classico)."""

    def __init__(self, arq):
        try:
            import netCDF4
            self.d = netCDF4.Dataset(arq); self.d.set_auto_mask(False); self.tipo = "netCDF4"; return
        except ImportError:
            pass
        try:
            import h5py
            self.d = h5py.File(arq, "r"); self.tipo = "h5py"; return
        except (ImportError, OSError):
            pass
        from scipy.io import netcdf_file
        self.d = netcdf_file(arq, "r", mmap=True); self.tipo = "scipy"

    def tem(self, n):
        return n in (self.d if self.tipo == "h5py" else self.d.variables)

    def var(self, n):
        return self.d[n] if self.tipo == "h5py" else self.d.variables[n]

    def attr(self, n):
        if self.tipo == "netCDF4":
            return self.d.getncattr(n)
        if self.tipo == "h5py":
            return self.d.attrs[n]
        return getattr(self.d, n)

    def tempos(self):
        return [np.asarray(t).astype("S1").tobytes().decode() for t in self.var("Times")[:]]

    def close(self):
        self.d.close()


def instantes(pasta, dom):
    """[(arquivo, indice, tempo)] de todos os wrfout_<dom> da pasta, em ordem."""
    out = []
    for arq in sorted(glob.glob(os.path.join(pasta, "wrfout_%s_*" % dom))):
        nc = Nc(arq); out += [(arq, k, t) for k, t in enumerate(nc.tempos())]; nc.close()
    return out


def sha(a):
    return hashlib.sha1(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def km(lat, lon, p):
    dy = (lat - p[0]) * 111.195; dx = (lon - p[1]) * 111.195 * np.cos(np.radians(p[0]))
    return np.hypot(dx, dy), (np.degrees(np.arctan2(dx, dy)) + 360) % 360


def recorte(pasta, saida):
    it3 = instantes(pasta, "d03")
    if not it3:
        raise SystemExit("sem wrfout_d03 em %s" % pasta)
    nc = Nc(it3[0][0]); leitor = nc.tipo
    lat, lon = np.array(nc.var("XLAT")[0]), np.array(nc.var("XLONG")[0])
    dx = float(np.ravel(nc.attr("DX"))[0]); nc.close()   # no wrf_run o scipy devolve o atributo como vetor de 1 elemento
    jc, ic = np.unravel_index(np.argmin(km(lat, lon, FRENTE)[0]), lat.shape)
    j0, j1, i0, i1 = jc - MEIA, jc + MEIA + 1, ic - MEIA, ic + MEIA + 1
    if j0 < 0 or i0 < 0 or j1 > lat.shape[0] or i1 > lat.shape[1]:
        raise SystemExit("a caixa sai do d03")
    hashes, cub, sup, tj, faltam = {"d03": {}, "d02": {}}, {}, {}, [], set()
    abertos = {}
    for arq, k, t in it3:
        nc = abertos.setdefault(arq, Nc(arq))
        hashes["d03"][t] = {n: sha(nc.var(n)[k]) for n in HASH_D03 if nc.tem(n)}
        if not (INI <= t <= FIM):
            continue
        tj.append(t)
        for n in V3D:
            if not nc.tem(n):
                faltam.add(n); continue
            v = nc.var(n)
            if len(v.shape) != 4:
                continue
            cub.setdefault(n, []).append(np.array(v[k, :, j0:j1 + (n == "V"), i0:i1 + (n == "U")], dtype=np.float32))
        for n in V2D:
            if nc.tem(n):
                sup.setdefault(n, []).append(np.array(nc.var(n)[k], dtype=np.float32))
            else:
                faltam.add(n)
        hgt = np.array(nc.var("HGT")[k, j0:j1, i0:i1], dtype=np.float32)
    for nc in abertos.values():
        nc.close()
    abertos = {}
    for arq, k, t in instantes(pasta, "d02"):
        nc = abertos.setdefault(arq, Nc(arq))
        hashes["d02"][t] = {n: sha(nc.var(n)[k]) for n in HASH_D02 if nc.tem(n)}
    for nc in abertos.values():
        nc.close()
    if not tj:
        raise SystemExit("nenhum instante do d03 entre %s e %s" % (INI, FIM))
    meta = {"pasta": os.path.abspath(pasta), "leitor": leitor, "dx": dx, "jc": int(jc), "ic": int(ic), "meia": MEIA,
            "faltam": sorted(faltam), "janela": [INI, FIM]}
    np.savez_compressed(saida, tempos=np.array(tj), lat=lat[j0:j1, i0:i1], lon=lon[j0:j1, i0:i1], hgt=hgt,
                        lat_d03=lat, lon_d03=lon, hashes=json.dumps(hashes), meta=json.dumps(meta),
                        **{"c_" + n: np.stack(v) for n, v in cub.items()}, **{"s_" + n: np.stack(v) for n, v in sup.items()})
    return meta


def carrega(arq):
    z = np.load(arq)
    r = {k: z[k] for k in z.files}
    r["tempos"] = [str(t) for t in r["tempos"]]
    r["hashes"] = json.loads(str(r["hashes"])); r["meta"] = json.loads(str(r["meta"]))
    return r


def idx(tempos, a, b):
    return [k for k, t in enumerate(tempos) if a <= t <= b]


def diag(r):
    """Numeros de C1-C5 de uma rodada recortada."""
    c, s, tt, dx = (lambda n: r.get("c_" + n)), (lambda n: r.get("s_" + n)), r["tempos"], r["meta"]["dx"]
    zero = np.zeros_like(c("QCLOUD"))
    q = lambda n: c(n) if c(n) is not None else zero
    p = c("P") + c("PB")
    tk = (c("T") + 300.0) * (p / 1e5) ** (RD / CP)
    rho = p / (RD * tk * (1 + 0.608 * q("QVAPOR")))
    dz = np.diff((c("PH") + c("PHB")) / G, axis=1)
    mar = rho * dz * dx * dx                                        # kg de ar por celula
    d5, _ = km(r["lat"], r["lon"], FRENTE); d3 = d5 <= 3.0; d5 = d5 <= 5.0
    frio = tk < 273.15
    slw = (q("QCLOUD") + q("QRAIN")) * frio
    gelo = q("QICE") + q("QSNOW") + q("QGRAUP") + q("QHAIL")
    m_slw = (mar * slw)[:, :, d5].sum(axis=(1, 2))
    m_gel = (mar * gelo)[:, :, d5].sum(axis=(1, 2))
    out = {}
    # C1: reservatorio
    k1 = idx(tt, "2026-08-25_22:00:00", "2026-08-26_01:30:00")
    km1 = max(k1, key=lambda k: m_slw[k])
    w = (mar * slw)[km1][:, d5]
    tc = tk[km1][:, d5] - 273.15
    c1 = {"slw_max_kg": float(m_slw[km1]), "quando": tt[km1],
          "t_media_c": float((w * tc).sum() / w.sum()) if w.sum() > 0 else None}
    qc, nd = q("QCLOUD")[k1][:, :, d5], q("QNDROP")[k1][:, :, d5]
    tcj = tk[k1][:, :, d5] - 273.15
    dgot = np.where((qc > 1e-7) & (nd > 1e3), (6 * qc / (math.pi * 1000.0 * np.maximum(nd, 1.0))) ** (1 / 3.0), 0.0)
    for nome, a, b in (("-8_-3", -8.0, -3.0), ("-38_-30", -38.0, -30.0)):
        m = (tcj >= a) & (tcj <= b) & (dgot > 0)
        ww = (qc * mar[k1][:, :, d5])[m]
        c1["d_got_um_" + nome] = float((dgot[m] * ww).sum() / ww.sum() * 1e6) if ww.sum() > 0 else None
        c1["slw_kg_" + nome] = float(((mar * slw)[k1][:, :, d5] * ((tcj >= a) & (tcj <= b))).sum() / len(k1))
    c1["sem_qndrop"] = c("QNDROP") is None
    out["C1"] = c1
    # C2: surto (janelas moveis de 30 min = 2 instantes)
    out["C2"] = {}
    for braco, t0 in T0_C2.items():
        ks = idx(tt, t0, "2026-08-26_02:35:00")
        best = (0.0, None)
        for k in ks:
            if k + 2 < len(tt) and tt[k + 2] <= "2026-08-26_02:35:00" and m_slw[k] > 0:
                f = max(0.0, min(m_slw[k] - m_slw[k + 2], m_gel[k + 2] - m_gel[k])) / m_slw[k]
                if f > best[0]:
                    best = (f, tt[k])
        out["C2"]["janela_" + braco] = {"fracao_max": best[0], "inicio": best[1]}
    # C3: tamanho no nivel mais baixo, ate 3 km
    k3 = idx(tt, "2026-08-25_22:00:00", "2026-08-26_02:35:00")
    c3 = {}
    for nome, qn, nn, vn, rh in (("graupel", "QGRAUP", "QNGRAUPEL", "QVGRAUPEL", 400.0), ("granizo", "QHAIL", "QNHAIL", "QVHAIL", 900.0)):
        qq, nx = q(qn)[k3, 0][:, d3], q(nn)[k3, 0][:, d3]
        vol = c(vn)[k3, 0][:, d3] if c(vn) is not None else qq / rh
        ok = (qq > 1e-6) & (nx > 0)
        dd = np.where(ok, (6 * vol / (math.pi * np.maximum(nx, 1e-12))) ** (1 / 3.0), 0.0)
        c3[nome] = {"d_max_mm": float(dd.max() * 1e3) if ok.any() else 0.0,
                    "d_medio_mm": float((dd[ok] * qq[ok]).sum() / qq[ok].sum() * 1e3) if ok.any() else 0.0,
                    "volume_previsto": c(vn) is not None}
    out["C3"] = c3
    # C4: gelo no chao, 22:00 -> 02:35, media ate 3 km na grade inteira do d03
    D, _ = km(r["lat_d03"], r["lon_d03"], FRENTE); m3 = D <= 3.0

    def acum(n, t):
        if s(n) is None:
            return None
        if t in tt:
            return float(s(n)[tt.index(t)][m3].mean())
        a, b = tt.index("2026-08-26_02:30:00"), tt.index("2026-08-26_02:45:00")
        return float(s(n)[a][m3].mean() + (s(n)[b][m3].mean() - s(n)[a][m3].mean()) / 3.0)
    c4 = {}
    for n in ("GRAUPELNC", "HAILNC", "SNOWNC", "RAINNC"):
        a, b = acum(n, "2026-08-25_22:00:00"), acum(n, "2026-08-26_02:35:00")
        c4[n + "_mm"] = None if a is None else b - a
    gel = sum(c4[n + "_mm"] or 0.0 for n in ("GRAUPELNC", "HAILNC", "SNOWNC"))
    c4["gelo_mm"] = gel; c4["gelo_kg_bacia"] = gel * A_BACIA; c4["pontos_3km"] = int(m3.sum())
    out["C4"] = c4
    # C5: OLR ate 5 km do ponto do drone; nuvem super-resfriada 3-8 km a SSW da frente as 01:00-01:15
    Dd, _ = km(r["lat_d03"], r["lon_d03"], DRONE); m5 = Dd <= 5.0
    olr = np.array([s("OLR")[k][m5].mean() for k in range(len(tt))])
    ka, kb = idx(tt, "2026-08-25_22:00:00", "2026-08-26_00:30:00"), idx(tt, "2026-08-26_02:00:00", "2026-08-26_02:50:00")
    dist, rumo = km(r["lat"], r["lon"], FRENTE)
    sec = (dist >= 3) & (dist <= 8) & (rumo >= 180) & (rumo <= 225)
    col = (mar * slw).sum(axis=1) / (dx * dx)                      # kg/m2 de agua super-resfriada na coluna
    kc = idx(tt, "2026-08-26_00:50:00", "2026-08-26_01:20:00")
    out["C5"] = {"olr_min_22_0030": float(olr[ka].min()), "quando_min": tt[ka[int(np.argmin(olr[ka]))]],
                 "olr_min_02_0250": float(olr[kb].min()), "olr_pixel_min_22_0030": float(min(s("OLR")[k][m5].min() for k in ka)),
                 "a": bool(olr[ka].min() <= 175.0), "b": bool(olr[kb].min() >= 280.0),
                 "slw_ssw_kg_m2_max": float(col[kc][:, sec].max()) if kc else None,
                 "slw_ssw_kg_m2_media": float(col[kc][:, sec].mean()) if kc else None}
    out["C5"]["passa"] = out["C5"]["a"] and out["C5"]["b"]
    out["serie"] = {"tempos": tt, "slw_kg": m_slw.tolist(), "gelo_kg": m_gel.tolist(), "olr_drone": olr.tolist()}
    return out


def identidade(h1, h2, corte):
    """Primeiro instante com hash diferente (d02 e d03) e se todos os anteriores ao corte sao iguais."""
    dif = []
    for dom in ("d02", "d03"):
        for t in sorted(set(h1[dom]) & set(h2[dom])):
            if h1[dom][t] != h2[dom][t]:
                dif.append(t); break
    pr = min(dif) if dif else None
    return {"primeiro_diferente": pr, "ok": pr is None or pr >= corte}


def criterios(pasta_npz, saida):
    os.makedirs(saida, exist_ok=True)
    R = {}
    for arq in sorted(glob.glob(os.path.join(pasta_npz, "*_m*.npz"))):
        m = re.match(r"^(A|S|E2|R)_m(\d+)\.npz$", os.path.basename(arq))
        if m:
            R[(m.group(1), int(m.group(2)))] = carrega(arq)
    if not R:
        raise SystemExit("nenhum <braco>_m<n>.npz em %s" % pasta_npz)
    D = {k: diag(v) for k, v in R.items()}
    membros = sorted({m for _, m in R})
    L = ["Criterios C1-C5 do ensemble no d03 (criterios_ens_d03.py); rodadas: " + ", ".join("%s_m%d" % k for k in sorted(R)), ""]
    faltam = sorted({n for v in R.values() for n in v["meta"]["faltam"]})
    if faltam:
        L.append("campos ausentes nos wrfout (tratados como zero ou pela alternativa): " + ", ".join(faltam))
    L.append("leitor: " + ", ".join(sorted({v["meta"]["leitor"] for v in R.values()})))
    L += ["", "Validacao 3 (bit a bit antes do corte):"]
    ident = {}
    for m in membros:
        for (a, b), corte in CORTES.items():
            if (a, m) in R and (b, m) in R:
                x = identidade(R[(a, m)]["hashes"], R[(b, m)]["hashes"], corte); ident["%s=%s_m%d" % (a, b, m)] = x
                L.append("  m%d %s = %s antes de %s: %s (primeiro instante diferente: %s)"
                         % (m, a, b, corte[11:16], "ok" if x["ok"] else "FALHOU", x["primeiro_diferente"]))
    fmt = lambda x, f="%.3g": "-" if x is None else f % x
    L += ["", "%-6s %-10s %-6s %-9s %-9s %-9s %-8s %-8s %-10s %-9s %-9s %-6s"
          % ("rodada", "C1 SLW kg", "quando", "T med C", "Dgot-8-3", "Dgot-38-30", "C2 E2", "C2 R", "C3 Dmax mm", "C4 kg", "C5 OLR", "C5")]
    for k in sorted(R, key=lambda k: (k[1], ["A", "S", "E2", "R"].index(k[0]))):
        d = D[k]
        L.append("%-6s %-10s %-6s %-9s %-9s %-9s %-8s %-8s %-10s %-9s %-9s %-6s" % (
            "%s_m%d" % k, fmt(d["C1"]["slw_max_kg"]), d["C1"]["quando"][11:16], fmt(d["C1"]["t_media_c"], "%.1f"),
            fmt(d["C1"]["d_got_um_-8_-3"], "%.1f"), fmt(d["C1"]["d_got_um_-38_-30"], "%.1f"),
            fmt(d["C2"]["janela_E2"]["fracao_max"], "%.2f"), fmt(d["C2"]["janela_R"]["fracao_max"], "%.2f"),
            fmt(max(d["C3"]["graupel"]["d_max_mm"], d["C3"]["granizo"]["d_max_mm"]), "%.1f"),
            fmt(d["C4"]["gelo_kg_bacia"]), "%.0f/%.0f" % (d["C5"]["olr_min_22_0030"], d["C5"]["olr_min_02_0250"]),
            "sim" if d["C5"]["passa"] else "nao"))
    L += ["  (C2: fracao do SLW ate 5 km congelada em 30 min, na janela de E2 a partir de 00:00 e na de R a partir de 23:30;",
          "   C3: maior diametro medio-massa de graupel ou granizo no nivel 1 ate 3 km; C4: GRAUPELNC+HAILNC+SNOWNC",
          "   de 22:00 a 02:35, media ate 3 km x 1,19e6 m2; C5: OLR medio ate 5 km do drone, menor de 22:00-00:30 / de 02:00-02:45)", ""]
    L.append("Regra de decisao (C4 >= 1e6 kg e acima de A no mesmo membro; C5; candidato com os dois em >= 80 % dos membros):")
    decisao = {}
    for b in ("S", "E2", "R"):
        ms = [m for m in membros if (b, m) in R and ("A", m) in R]
        if not ms:
            continue
        c4 = [m for m in ms if D[(b, m)]["C4"]["gelo_kg_bacia"] >= 1e6 and D[(b, m)]["C4"]["gelo_kg_bacia"] > D[("A", m)]["C4"]["gelo_kg_bacia"]]
        c5 = [m for m in ms if D[(b, m)]["C5"]["passa"]]
        sinais = {int(np.sign(D[(b, m)]["C4"]["gelo_kg_bacia"] - D[("A", m)]["C4"]["gelo_kg_bacia"])) for m in ms}
        cand = len(c4) >= math.ceil(0.8 * len(ms)) and len(c5) >= math.ceil(0.8 * len(ms))
        decisao[b] = {"membros": ms, "c4": c4, "c5": c5, "sinal_c4_vs_A": sorted(sinais), "candidato": cand}
        L.append("  %-3s membros %s: C4 em %d, C5 em %d; sinal de C4 - A nos pares: %s -> %s%s" % (
            b, ms, len(c4), len(c5), sorted(sinais), "CANDIDATO" if cand else "nao candidato",
            "" if len(ms) == 5 else " (provisorio: %d de 5 membros)" % len(ms)))
    txt = "\n".join(L) + "\n"
    open(os.path.join(saida, "criterios_ens_d03.txt"), "w").write(txt)
    json.dump({"rodadas": {"%s_m%d" % k: v for k, v in D.items()}, "identidade": ident, "decisao": decisao},
              open(os.path.join(saida, "criterios_ens_d03.json"), "w"), indent=1)
    print(txt)


def tudo(ens, saida):
    rec = os.path.join(saida, "recortes"); os.makedirs(rec, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(ens, "*_m*"))):
        nome = os.path.basename(p)
        if not re.match(r"^(A|S|E2|R)_m\d+$", nome) or os.path.exists(os.path.join(rec, nome + ".npz")):
            continue
        try:
            ok = "SUCCESS COMPLETE WRF" in open(os.path.join(p, "rsl.error.0000"), errors="replace").read()
        except OSError:
            ok = False
        if ok:
            print("recortando", nome, flush=True)
            print("  ", recorte(p, os.path.join(rec, nome + ".npz")), flush=True)
    criterios(rec, saida)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "recorte":
        print(recorte(a[1], a[2]))
    elif len(a) == 3 and a[0] == "tudo":
        tudo(a[1], a[2])
    elif len(a) == 3 and a[0] == "criterios":
        criterios(a[1], a[2])
    else:
        sys.exit(__doc__)
