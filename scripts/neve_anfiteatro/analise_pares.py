# -*- coding: utf-8 -*-
"""
Mudanca de neve/gelo por pares de datas, so nos pixels observados nas duas datas, no anfiteatro e nos controles;
erro por componente. Le mascaras_<fonte>.npz e serie_<fonte>.json (serie_multifonte.py) e cubos_s1.npz.

Pares do evento (colapso 26/08 02:52 UTC; tempestade do Himawari na noite 25->26/08):
  A  12/08 -> 24/08   acumulacao antes do evento ("gelo novo")
  B  24/08 -> 27/08   o evento (colapso + noite da tempestade)
  C  12/08 -> 27/08   o par da MEDICAO_SENTINEL2_2026
Pares de referencia (sem evento conhecido): todos os pares de cenas da moncao (01/07 a 21/09) com intervalo de
3 a 20 dias que nao contem 26/08: dao a variabilidade natural + ruido de mascara, no anfiteatro e nos controles.

Componentes de erro da mudanca liquida no anfiteatro:
  processamento  |s2es - s2pc|           (mesmo dado, duas cadeias de distribuicao/offset)
  atmosfera      |s2es - s2l1c|          (Sen2Cor x topo da atmosfera)
  limiar         meia amplitude NDSI 0,30-0,50
  natural        desvio-padrao da mudanca liquida (fracao da area comum) nos pares de referencia
  nao observado  intervalo: 0 (nada mudou fora da vista) a extrapolacao proporcional
Uso: python analise_pares.py <dir_dados>
"""
import json
import os
import sys
from datetime import datetime, timedelta

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

COLAPSO_T = datetime(2026, 8, 26, 2, 52)
LIM = (0.30, 0.42, 0.50)


def carrega(d, fonte):
    z = np.load(os.path.join(d, "mascaras_%s.npz" % fonte))
    reg = {k.split("__", 1)[1]: z[k] for k in z.files if k.startswith("regiao__")}
    cenas = {}
    suf = "__ndsiE" if os.environ.get("MASCARA") == "estrita" else "__ndsi"
    for k in z.files:
        if k.endswith(suf):
            i = k[:-len(suf)]
            cenas[i] = (z[k].astype(np.float32), z[i + "__T"])
    # cada aquisicao e uma chave (data + satelite); recortes do mesmo datatake (mesmo satelite e dia) sao juntados
    serie = {r["id"]: r for r in json.load(open(os.path.join(d, "serie_%s.json" % fonte))) if "erro" not in r}
    dias = {}
    for i, (a, T) in sorted(cenas.items()):
        t = datetime.strptime(serie[i]["datetime"][:19], "%Y-%m-%dT%H:%M:%S")
        dk = "%s_%s" % (t.date(), i[:3])
        if dk in dias:
            b = dias[dk][0]
            dias[dk] = (np.where(np.isfinite(b), b, a), T, min(dias[dk][2], t))
        else:
            dias[dk] = (a, T, t)
    return reg, dias


def compara(a, b, reg, A, lim):
    """a, b: NDSI (nan = nao observado). devolve por regiao: area comum, perda, ganho, liquido (ha)"""
    ok = np.isfinite(a) & np.isfinite(b)
    na, nb = a > lim, b > lim
    r = {}
    for nome, m in reg.items():
        c = m & ok; tot = m.sum() * A
        perda = (c & na & ~nb).sum() * A; ganho = (c & ~na & nb).sum() * A
        r[nome] = {"area_ha": round(tot / 1e4, 2), "comum_ha": round(c.sum() * A / 1e4, 2),
                   "frac_comum": round(float(c.sum() / m.sum()), 4),
                   "neve_a_ha": round((c & na).sum() * A / 1e4, 2), "neve_b_ha": round((c & nb).sum() * A / 1e4, 2),
                   "perda_ha": round(perda / 1e4, 2), "ganho_ha": round(ganho / 1e4, 2), "liquido_ha": round((ganho - perda) / 1e4, 2),
                   "liquido_frac_comum": round(float((ganho - perda) / (c.sum() * A)), 4) if c.any() else None}
    return r


def aglomerado(a, b, m, A, lim=0.42):
    from scipy import ndimage
    ok = np.isfinite(a) & np.isfinite(b) & m
    p = ok & (a > lim) & ~(b > lim)
    lab, n = ndimage.label(p, structure=np.ones((3, 3)))
    if n == 0:
        return None
    tam = ndimage.sum(p, lab, range(1, n + 1))
    k = int(np.argmax(tam)) + 1
    jj, ii = np.where(lab == k)
    return {"n_aglomerados": int(n), "maior_ha": round(float(tam.max() * A / 1e4), 2), "j": (int(jj.min()), int(jj.max())), "i": (int(ii.min()), int(ii.max())),
            "dim_m": (int((jj.max() - jj.min() + 1) * 20), int((ii.max() - ii.min() + 1) * 20)), "lab": lab == k}


def main(d):
    out = {"fontes": {}, "pares_evento": {}, "referencia": {}, "erro": {}}
    PARES = {"A_12ago_24ago": ("2026-08-12", "2026-08-24"), "B_24ago_27ago": ("2026-08-24", "2026-08-27"), "C_12ago_27ago": ("2026-08-12", "2026-08-27"), "D_12ago_18out": ("2026-08-12", "2026-10-18")}
    dados = {}
    for f in ("s2es", "s2pc", "s2l1c"):
        if not os.path.exists(os.path.join(d, "mascaras_%s.npz" % f)):
            continue
        reg, dias = carrega(d, f)
        if not dias:
            continue
        T = dias[next(iter(dias))][1]; A = abs(T[0] * T[4])
        dados[f] = (reg, dias, A)
        out["fontes"][f] = sorted(str(k) for k in dias)
    # pares do evento: todas as combinacoes de aquisicoes das duas datas; mais o par do mesmo dia 24/08 (S2B x S2A, 15 min)
    PARES["Z_24ago_S2B_S2A_15min"] = ("2026-08-24_S2B", "2026-08-24_S2A")
    for nome, (da, db) in PARES.items():
        out["pares_evento"][nome] = {}
        for f, (reg, dias, A) in dados.items():
            kas = [k for k in dias if k.startswith(da)]; kbs = [k for k in dias if k.startswith(db)]
            for ka in kas:
                for kb in kbs:
                    if ka == kb:
                        continue
                    a, b = dias[ka][0], dias[kb][0]
                    chave = "%s|%s>%s" % (f, ka[11:], kb[11:])
                    v = {"%02d" % int(l * 100): compara(a, b, reg, A, l) for l in LIM}
                    ag = aglomerado(a, b, reg["anfiteatro"], A)
                    if ag:
                        T = dias[ka][1]
                        jc = (ag["j"][0] + ag["j"][1]) / 2 + 0.5; ic = (ag["i"][0] + ag["i"][1]) / 2 + 0.5
                        x, y = T[2] + T[0] * ic, T[5] + T[4] * jc
                        from pyproj import Transformer
                        lon, lat = Transformer.from_crs(32645, 4326, always_xy=True).transform(x, y)
                        dist = np.hypot((lon - comum.COLAPSO[0]) * 111320 * np.cos(np.radians(lat)), (lat - comum.COLAPSO[1]) * 111320)
                        v["maior_aglomerado_perda"] = {k: w for k, w in ag.items() if k != "lab"} | {
                            "centro_lon": round(lon, 4), "centro_lat": round(lat, 4), "dist_colapso_m": int(dist)}
                        if f == "s2es":
                            np.save(os.path.join(d, "aglomerado_%s%s_%s_%s.npy" % ("E_" if os.environ.get("MASCARA") == "estrita" else "", nome, ka[11:], kb[11:])), ag["lab"])
                    out["pares_evento"][nome][chave] = v
    # pares de referencia (s2es), 01/07 a 21/09, 3-20 dias, sem 26/08
    ref = []
    reg, dias, A = dados["s2es"]
    ks = sorted(dias, key=lambda k: dias[k][2])
    for i, ka in enumerate(ks):
        for kb in ks[i + 1:]:
            dt = (dias[kb][2].date() - dias[ka][2].date()).days
            ta, tb = dias[ka][2], dias[kb][2]
            if not (3 <= dt <= 20) or tb > datetime(2026, 9, 22) or (ta < COLAPSO_T < tb):
                continue
            r = compara(dias[ka][0], dias[kb][0], reg, A, 0.42)
            if r["anfiteatro"]["frac_comum"] < 0.3:
                continue
            ref.append({"a": ka, "b": kb, "dias": dt, **{k: {kk: r[k][kk] for kk in ("frac_comum", "liquido_ha", "perda_ha", "ganho_ha", "liquido_frac_comum")} for k in r}})
    out["referencia"] = ref
    # orcamento de erro por par e por combinacao de aquisicoes, limiar 0,42
    fr_anf = [x["anfiteatro"]["liquido_frac_comum"] for x in ref if x["anfiteatro"]["liquido_frac_comum"] is not None]
    fr_ctl = [x["alto_fora"]["liquido_frac_comum"] for x in ref if x["alto_fora"]["frac_comum"] >= 0.3 and x["alto_fora"]["liquido_frac_comum"] is not None]
    fr_anf_curto = [x["anfiteatro"]["liquido_frac_comum"] for x in ref if x["dias"] <= 5 and x["anfiteatro"]["liquido_frac_comum"] is not None]
    out["ruido_referencia"] = {"anf_dp": float(np.std(fr_anf)), "anf_n": len(fr_anf), "ctl_dp": float(np.std(fr_ctl)) if fr_ctl else None, "ctl_n": len(fr_ctl),
                               "anf_curto_dp": float(np.std(fr_anf_curto)) if fr_anf_curto else None, "anf_curto_n": len(fr_anf_curto)}
    for nome, pe in out["pares_evento"].items():
        for chave, v in pe.items():
            if not chave.startswith("s2es|"):
                continue
            b = v["42"]["anfiteatro"]
            e = {k: b[k] for k in ("liquido_ha", "perda_ha", "ganho_ha", "comum_ha", "frac_comum")}
            alt = chave.replace("s2es|", "s2pc|")
            if alt in pe:
                e["proc_ha"] = round(abs(b["liquido_ha"] - pe[alt]["42"]["anfiteatro"]["liquido_ha"]), 2)
            alt = chave.replace("s2es|", "s2l1c|")
            if alt in pe:
                e["atm_ha"] = round(abs(b["liquido_ha"] - pe[alt]["42"]["anfiteatro"]["liquido_ha"]), 2)
            ls = [v[k]["anfiteatro"]["liquido_ha"] for k in ("30", "42", "50")]
            e["limiar_ha"] = round((max(ls) - min(ls)) / 2, 2)
            e["natural_anf_ha"] = round(out["ruido_referencia"]["anf_dp"] * b["comum_ha"], 2)
            if out["ruido_referencia"]["anf_curto_dp"] is not None:
                e["natural_anf_curto_ha"] = round(out["ruido_referencia"]["anf_curto_dp"] * b["comum_ha"], 2)
            if fr_ctl:
                e["natural_ctl_ha"] = round(out["ruido_referencia"]["ctl_dp"] * b["comum_ha"], 2)
            comp = [e.get(k) or 0 for k in ("proc_ha", "atm_ha", "limiar_ha")] + [e.get("natural_anf_curto_ha") or e["natural_anf_ha"]]
            e["sigma_total_ha"] = round(float(np.sqrt(np.sum(np.square(comp)))), 2)
            e["extrapolado_liquido_ha"] = round(b["liquido_ha"] / b["frac_comum"], 2) if b["frac_comum"] else None
            e["controle_alto_fora"] = v["42"]["alto_fora"]; e["controle_cume_fora"] = v["42"]["cume_fora"]
            out["erro"][nome + "|" + chave[5:]] = e
    out["mascara"] = os.environ.get("MASCARA", "espectral")
    json.dump(out, open(os.path.join(d, "analise_pares_%s.json" % out["mascara"]), "w"), indent=1, default=str)
    for nome, e in out["erro"].items():
        print(nome, json.dumps({k: v for k, v in e.items() if not k.startswith("controle")}))
        print("   controle alto_fora:", {k: e["controle_alto_fora"][k] for k in ("frac_comum", "perda_ha", "ganho_ha", "liquido_ha", "liquido_frac_comum")})
    for nome, pe in out["pares_evento"].items():
        for f, v in pe.items():
            if "maior_aglomerado_perda" in v:
                g = v["maior_aglomerado_perda"]
                print(nome, f, "liq %+.1f ha | maior aglomerado de perda %.2f ha %s m em %.4fE %.4fN a %d m do colapso" % (
                    v["42"]["anfiteatro"]["liquido_ha"], g["maior_ha"], g["dim_m"], g["centro_lon"], g["centro_lat"], g["dist_colapso_m"]))
    print("ruido de referencia:", out["ruido_referencia"])
    print("pares de referencia:", len(ref))
    for x in ref:
        print("  %s->%s (%2d d) anf comum %.2f liq %+6.1f ha (%+.3f) | alto_fora comum %.2f liq %+.3f" % (
            x["a"], x["b"], x["dias"], x["anfiteatro"]["frac_comum"], x["anfiteatro"]["liquido_ha"], x["anfiteatro"]["liquido_frac_comum"],
            x["alto_fora"]["frac_comum"], x["alto_fora"]["liquido_frac_comum"] or 0))


if __name__ == "__main__":
    main(sys.argv[1])
