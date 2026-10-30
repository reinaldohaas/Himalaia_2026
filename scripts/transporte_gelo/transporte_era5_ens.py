# -*- coding: utf-8 -*-
"""
Como o gelo da nuvem chegaria a frente de gelo do quadro do Xinhua (28,2918 N / 85,5284 E, 4,8-5,15 km),
com o erro do ERA5 medido pelo ensemble (EDA, 10 membros + spread, 0,5 grau, 3 h) em vez de chutado.

Tres perguntas, por membro:
1. Deriva na queda. Graupel e granizo soltos a 6,4-9 km caem ate 5,0 km com o vento do membro; onde pousam?
   Para cada fonte candidata (o proprio alvo, a mancha de agua super-resfriada do B03/B05, o cume do
   Langtang Lirung), que vento seria preciso, e quantos desvios do ensemble ele fica do ERA5?
2. Fusao. A bacia inteira fica abaixo do 0 C. Quanto da massa sobrevive ate 5,6 / 5,0 / 4,64 km
   (Mason 1956, com ventilacao e evaporacao)? Quanto gelo derretido torna a camada isotermica a 0 C?
3. Massa. Quanta precipitacao os membros poem na bacia de 1,19 km2, e que convergencia/ascensao seria
   preciso para 1e6-1e8 kg em 2,5 h?

Alturas: z(600 hPa) do ERA5 deterministico horario (era5_wrf_pl_*.grib, com geopotencial), e daí para cima
hipsometria com o Tv de cada membro.

Uso: python transporte_era5_ens.py <dir_era5_ens> <dir_era5_wrf>
Saidas: data/processed/transporte_gelo/transporte_era5_ens.{json,txt,png}
"""
import json
import os
import sys

import numpy as np
import xarray as xr

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
SAIDA = os.path.join(RAIZ, "data", "processed", "transporte_gelo")
TILE = os.path.join(RAIZ, "cluster", "wrf_lhende", "d04", "glo30_3s", "00001-00540.00001-00480")
S0, W0, RES, NX, NY = 28.08, 85.30, 3.0 / 3600.0, 540, 480

ALVO = (28.2918, 85.5284)          # centro da perda de gelo do S2 (frente do quadro do Xinhua)
P = (28.293985, 85.523964)         # ponto do drone
Z_ALVO, Z_PONTO, Z_TOPO_BACIA = 5000.0, 4638.0, 5634.0
FONTES = {"sobre o alvo": ALVO,
          "mancha SR leste (B03/B05)": (28.2597, 85.4975),   # 6,3-6,9 km, encosta alta do Langtang Lirung
          "mancha SR oeste (B03/B05)": (28.2700, 85.4590),   # 5,0-5,5 km
          "cume do Langtang Lirung": (28.2561, 85.5189)}
Z_SOLTA = [6400.0, 7000.0, 7600.0, 9000.0]                  # -3 C, ~-5 C, -8 C e nucleo alto
HORAS = ["2026-08-25T22:00", "2026-08-25T23:00", "2026-08-26T00:00", "2026-08-26T00:30", "2026-08-26T01:00"]
AREA_BACIA = 1.19e6                # m2
G, RD, RV, CP, LF, LV, KA = 9.80665, 287.04, 461.5, 1005.0, 3.34e5, 2.5e6, 2.4e-2
KM_LAT, KM_LON = 111.32, 111.32 * np.cos(np.radians(ALVO[0]))

# classes de particula: (nome, diametro m, densidade kg/m3, velocidade terminal(D, rho_ar))
def vt_graupel(D, ra):              # Locatelli & Hobbs (1974), graupel tipo "lump", D em mm, corrigido pela densidade
    return 1.3 * (D * 1e3) ** 0.66 * (1.2 / ra) ** 0.4
def vt_granizo(D, ra):              # lei de arrasto, Cd = 0,6
    return np.sqrt(4 * G * D * 850.0 / (3 * 0.6 * ra))
def vt_neve(D, ra):
    return 1.0 * (1.2 / ra) ** 0.4
CLASSES = [("neve (agregado 5 mm)", 5e-3, 50.0, vt_neve),
           ("graupel 2 mm", 2e-3, 400.0, vt_graupel),
           ("graupel 5 mm", 5e-3, 400.0, vt_graupel),
           ("granizo 10 mm", 10e-3, 850.0, vt_granizo),
           ("granizo 20 mm", 20e-3, 850.0, vt_granizo)]
CORES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]


def es(Tc):
    return 611.2 * np.exp(17.67 * Tc / (Tc + 243.5))


def perfis(ens, det, hora):
    """perfis de cada membro no alvo, interpolados no tempo, com z hipsometrico a partir do z600 deterministico"""
    m = ens.interp(latitude=ALVO[0], longitude=ALVO[1]).interp(valid_time=np.datetime64(hora))
    z600 = float(det.z.sel(isobaricInhPa=600).interp(latitude=ALVO[0], longitude=ALVO[1]).interp(time=np.datetime64(hora))) / G
    p = m.pressure_level.values * 100.0                   # 600 ... 300 hPa
    out = []
    for k in m.number.values:
        a = m.sel(number=k)
        T, q, u, v, w = (a[x].values.astype(float) for x in ("t", "q", "u", "v", "w"))
        Tv = T * (1 + 0.608 * q)
        z = np.empty_like(p); z[0] = z600
        for i in range(1, len(p)):
            z[i] = z[i - 1] + RD * 0.5 * (Tv[i] + Tv[i - 1]) / G * np.log(p[i - 1] / p[i])
        out.append(dict(p=p, z=z, T=T, q=q, u=u, v=v, w=w))
    return out


def fino(pf, zz):
    """perfil numa grade de 10 m"""
    f = {c: np.interp(zz, pf["z"], pf[c]) for c in ("T", "q", "u", "v")}
    f["p"] = np.exp(np.interp(zz, pf["z"], np.log(pf["p"])))
    f["rho"] = f["p"] / (RD * f["T"] * (1 + 0.608 * f["q"]))
    return f


def queda(f, zz, zr, classe, z_fim=Z_PONTO):
    """integra a queda de zr ate z_fim: deriva (m), tempo (s) e fracao de massa de gelo restante em cada cota"""
    nome, D0, rp, vt = classe
    m0 = np.pi / 6 * rp * D0 ** 3
    m, x, y, t = m0, 0.0, 0.0, 0.0
    marcas = {Z_TOPO_BACIA: None, Z_ALVO: None, Z_PONTO: None}
    perfil = np.full(zz.shape, np.nan)
    i0 = int(np.searchsorted(zz, zr))
    dz = zz[1] - zz[0]
    for i in range(i0, -1, -1):
        z = zz[i]
        perfil[i] = m / m0
        for zm in marcas:
            if marcas[zm] is None and z <= zm:
                marcas[zm] = (m / m0, x, y, t)
        if z < z_fim:
            break
        D = (6 * m / (np.pi * rp)) ** (1 / 3) if m > 0 else 0.0
        ra, T, q, p = f["rho"][i], f["T"][i], f["q"][i], f["p"][i]
        V = vt(max(D, 1e-4), ra)
        dt = dz / V
        if m > 0:
            x += f["u"][i] * dt; y += f["v"][i] * dt; t += dt
            Tc = T - 273.15
            mu = 1.72e-5 * (T / 273.15) ** 0.7
            Dv = 2.11e-5 * (T / 273.15) ** 1.94 * (101325.0 / p)
            Re = V * D * ra / mu
            fh = 0.78 + 0.308 * 0.71 ** (1 / 3) * np.sqrt(Re)
            fv = 0.78 + 0.308 * (mu / ra / Dv) ** (1 / 3) * np.sqrt(Re)
            calor = KA * fh * Tc + LV * Dv * fv * (q * ra - es(0.0) / (RV * 273.15))
            if calor > 0:
                m = max(m - 2 * np.pi * D * calor / LF * dt, 0.0)
    marcas["perfil"] = perfil
    return marcas


def fl(zz, f):
    """altura do 0 C e do 0 C de bulbo umido"""
    import metpy.calc as mc
    from metpy.units import units
    Tc = f["T"] - 273.15
    z0 = float(np.interp(0.0, Tc[::-1], zz[::-1]))
    sel = slice(None, None, 10)
    Td = mc.dewpoint_from_specific_humidity(f["p"][sel] * units.Pa, f["q"][sel] * units("kg/kg")).to("degC").m
    Tw = mc.wet_bulb_temperature(f["p"][sel] * units.Pa, f["T"][sel] * units.K, Td * units.degC).to("degC").m
    zw = float(np.interp(0.0, Tw[::-1], zz[sel][::-1]))
    return z0, zw


def isotermica(zz, f, z0, z_chao):
    """gelo derretido (kg/m2 = mm) que resfria ate 0 C a camada entre z_chao e o 0 C"""
    s = (zz >= z_chao) & (zz <= z0)
    return float(np.sum(f["rho"][s] * CP * (f["T"][s] - 273.15)) * (zz[1] - zz[0]) / LF)


def divergencia(ens, hora):
    """divergencia media 600-450 hPa no alvo (diferencas centradas na grade de 0,5 grau), por membro"""
    m = ens.interp(valid_time=np.datetime64(hora)).sel(pressure_level=[600, 550, 500, 450])
    lat, lon = m.latitude.values, m.longitude.values
    dy = np.gradient(lat) * KM_LAT * 1e3
    dx = np.gradient(lon) * 111.32e3 * np.cos(np.radians(lat))[:, None]
    du = np.gradient(m.u.values, axis=-1) / dx
    dv = np.gradient(m.v.values, axis=-2) / dy[:, None]
    d = xr.DataArray((du + dv).mean(axis=1), dims=("number", "latitude", "longitude"),
                     coords=dict(number=m.number, latitude=lat, longitude=lon))
    return d.interp(latitude=ALVO[0], longitude=ALVO[1]).values


def cape_elevado(det, hora):
    """CAPE de parcelas de 600, 550 e 500 hPa no ERA5 deterministico (perfil completo ate 100 hPa)"""
    import metpy.calc as mc
    from metpy.units import units
    a = det.interp(latitude=ALVO[0], longitude=ALVO[1]).interp(time=np.datetime64(hora))
    a = a.where(a.isobaricInhPa <= 600, drop=True).sortby("isobaricInhPa", ascending=False)
    p = a.isobaricInhPa.values * units.hPa
    T = a.t.values * units.K
    Td = mc.dewpoint_from_specific_humidity(p, a.q.values * units("kg/kg"))
    r = {}
    for p0 in (600, 550, 500):
        i = int(np.argmin(abs(a.isobaricInhPa.values - p0)))
        prof = mc.parcel_profile(p[i:], T[i], Td[i])
        c, ci = mc.cape_cin(p[i:], T[i:], Td[i:], prof)
        r["%d hPa" % p0] = round(float(c.m), 1)
    return r


def perturbacao_cape(det, hora):
    """aquecimento (UR mantida) e umedecimento da parcela de 600 hPa necessarios para CAPE >= 50 e >= 250 J/kg"""
    import metpy.calc as mc
    from metpy.units import units
    a = det.interp(latitude=ALVO[0], longitude=ALVO[1]).interp(time=np.datetime64(hora))
    a = a.where(a.isobaricInhPa <= 600, drop=True).sortby("isobaricInhPa", ascending=False)
    p = a.isobaricInhPa.values * units.hPa
    T = a.t.values * units.K
    q = a.q.values
    Td = mc.dewpoint_from_specific_humidity(p, q * units("kg/kg"))
    ur0 = float(mc.relative_humidity_from_dewpoint(T[0], Td[0]).m)
    r = {"UR_600hPa": round(ur0, 2)}
    def cape(T0, Td0):
        c, _ = mc.cape_cin(p, T, Td, mc.parcel_profile(p, T0, Td0))
        return float(c.m)
    for nome, passos in (("aquecimento_K", np.arange(0, 6.01, 0.25)),):
        for alvo in (50, 250):
            r["%s_para_%d" % (nome, alvo)] = None
            for d in passos:
                T0 = T[0] + d * units.K
                if cape(T0, mc.dewpoint_from_relative_humidity(T0, ur0)) >= alvo:
                    r["%s_para_%d" % (nome, alvo)] = float(d); break
    for alvo in (50, 250):
        r["umedecimento_g_kg_para_%d" % alvo] = None
        for dq in np.arange(0, 6.01, 0.25):
            Td0 = mc.dewpoint_from_specific_humidity(p[0], (q[0] + dq / 1e3) * units("kg/kg"))
            if Td0 > T[0]:
                break
            if cape(T[0], Td0) >= alvo:
                r["umedecimento_g_kg_para_%d" % alvo] = float(dq); break
    r["cape_parcela_saturada_J_kg"] = round(cape(T[0], T[0]), 1)
    return r


def relevo():
    z = np.fromfile(TILE, ">i2").reshape(NY, NX).astype(float)
    lat = S0 + (np.arange(NY) + 0.5) * RES; lon = W0 + (np.arange(NX) + 0.5) * RES
    return lat, lon, z


def main():
    dens, dwrf = sys.argv[1], sys.argv[2]
    os.makedirs(SAIDA, exist_ok=True)
    ens = xr.open_dataset(os.path.join(dens, "era5ens_pl_members.nc"))
    spr = xr.open_dataset(os.path.join(dens, "era5ens_pl_spread.nc"))
    sl_i = xr.open_dataset(os.path.join(dens, "era5ens_sl_members", "data_stream-enda_stepType-instant.nc"))
    sl_a = xr.open_dataset(os.path.join(dens, "era5ens_sl_members", "data_stream-enda_stepType-accum.nc"))
    kw = dict(engine="cfgrib", backend_kwargs={"indexpath": ""})
    det = xr.concat([xr.open_dataset(os.path.join(dwrf, "era5_wrf_pl_%d.grib" % i), **kw) for i in (1, 2)], "time")
    det = det.sel(latitude=slice(29.5, 27.0), longitude=slice(84.0, 87.0))
    zz = np.arange(4400.0, 9790.0, 10.0)
    bac = np.load(os.path.join(RAIZ, "data", "processed", "ponto_drone", "bacia_ponto.npz"))

    def na_bacia(lat, lon):
        r = bac["lat"][1] - bac["lat"][0]
        i = int(round((lat - bac["lat"][0]) / r)); j = int(round((lon - bac["lon"][0]) / r))
        return bool(0 <= i < bac["mascara"].shape[0] and 0 <= j < bac["mascara"].shape[1] and bac["mascara"][i, j])

    R = {"alvo": {"lat": ALVO[0], "lon": ALVO[1], "z_m": Z_ALVO}, "fontes": {k: list(v) for k, v in FONTES.items()},
         "horas": HORAS, "z_solta_m": Z_SOLTA, "por_hora": {}}
    pousos = {c[0]: [] for c in CLASSES}       # para a figura: solta a 7,0 km sobre o alvo
    sobrevive = {c[0]: [] for c in CLASSES}    # fracao de massa a 5,6 / 5,0 / 4,64 km (solta a 7,0 km)
    perfis_massa = {c[0]: [] for c in CLASSES}
    req = {}                                   # (fonte, classe, zr) -> lista de (|dV|, sigma)
    for hora in HORAS:
        pfs = perfis(ens, det, hora)
        H = {"membros": []}
        for k, pf in enumerate(pfs):
            f = fino(pf, zz)
            z0, zw = fl(zz, f)
            camada = (zz >= Z_ALVO) & (zz <= z0)
            vcam = float(np.hypot(f["u"][camada].mean(), f["v"][camada].mean()))
            M = {"z_0C_m": round(z0), "z_0C_bulbo_umido_m": round(zw),
                 "vento_medio_abaixo_0C_ms": round(vcam, 2),
                 "gelo_para_isotermica_mm": {"ate_5000m": round(isotermica(zz, f, z0, Z_ALVO), 2),
                                             "ate_4638m": round(isotermica(zz, f, z0, Z_PONTO), 2)},
                 "agua_precipitavel_acima_5000m_mm": round(float(np.sum((f["rho"] * f["q"])[zz >= Z_ALVO]) * 10.0), 2),
                 "queda": {}}
            for c in CLASSES:
                M["queda"][c[0]] = {}
                for zr in Z_SOLTA:
                    mk = queda(f, zz, zr, c)
                    fa, x, y, t = mk[Z_ALVO]
                    M["queda"][c[0]]["%d" % zr] = {
                        "deriva_ate_5000m_km": [round(x / 1e3, 2), round(y / 1e3, 2)],
                        "tempo_de_queda_min": round(t / 60, 1),
                        "massa_restante": {"5634m": round(mk[Z_TOPO_BACIA][0], 3), "5000m": round(fa, 3), "4638m": round(mk[Z_PONTO][0], 3)}}
                    if zr == 7000.0:
                        la = ALVO[0] + y / 1e3 / KM_LAT; lo = ALVO[1] + x / 1e3 / KM_LON
                        pousos[c[0]].append((x / 1e3, y / 1e3, na_bacia(la, lo)))
                        sobrevive[c[0]].append([mk[Z_TOPO_BACIA][0], fa, mk[Z_PONTO][0]])
                        perfis_massa[c[0]].append(mk["perfil"])
            H["membros"].append(M)
        # vento necessario de cada fonte, contra o vento efetivo (deriva / tempo) de cada membro
        H["vento_necessario"] = {}
        for nf, (fla, flo) in FONTES.items():
            dxy = np.array([(ALVO[1] - flo) * KM_LON, (ALVO[0] - fla) * KM_LAT]) * 1e3
            H["vento_necessario"][nf] = {"distancia_km": round(float(np.hypot(*dxy)) / 1e3, 2),
                                         "rumo_para_graus": round(float(np.degrees(np.arctan2(dxy[0], dxy[1]))) % 360)}
            for c in CLASSES:
                for zr in Z_SOLTA:
                    ef, tq = [], []
                    for M in H["membros"]:
                        qd = M["queda"][c[0]]["%d" % zr]
                        t = qd["tempo_de_queda_min"] * 60
                        ef.append(np.array(qd["deriva_ate_5000m_km"]) * 1e3 / t); tq.append(t)
                    ef = np.array(ef); vreq = dxy / np.mean(tq)
                    dv = vreq - ef.mean(axis=0)
                    un = dv / max(np.hypot(*dv), 1e-9)
                    sig = float(np.std(ef @ un, ddof=1))
                    H["vento_necessario"][nf]["%s @ %d m" % (c[0], zr)] = {
                        "vento_necessario_ms": [round(float(vreq[0]), 2), round(float(vreq[1]), 2)],
                        "vento_efetivo_era5_ms": [round(float(ef.mean(axis=0)[0]), 2), round(float(ef.mean(axis=0)[1]), 2)],
                        "diferenca_ms": round(float(np.hypot(*dv)), 2), "desvio_ensemble_ms": round(sig, 3),
                        "em_desvios": round(float(np.hypot(*dv)) / max(sig, 1e-3), 1)}
                    req.setdefault((nf, c[0], zr), []).append((float(np.hypot(*dv)), sig))
        dv = divergencia(ens, hora)
        H["divergencia_600_450hPa_por_s"] = {"media": float("%.3g" % dv.mean()), "desvio": float("%.3g" % dv.std(ddof=1))}
        om = ens.w.interp(latitude=ALVO[0], longitude=ALVO[1]).interp(valid_time=np.datetime64(hora)).sel(pressure_level=500).values
        H["omega_500hPa_Pa_s"] = {"media": round(float(om.mean()), 3), "desvio": round(float(om.std(ddof=1)), 3)}
        H["spread_produto_500hPa"] = {x: round(float(spr[x].interp(latitude=ALVO[0], longitude=ALVO[1]).interp(
            valid_time=np.datetime64(hora)).sel(pressure_level=500)), 2) for x in ("u", "v", "t")}
        H["cape_elevado_deterministico_J_kg"] = cape_elevado(det, hora)
        H["perturbacao_para_conveccao_600hPa"] = perturbacao_cape(det, hora)
        H["spread_produto_600hPa"] = {x: float("%.3g" % float(spr[x].interp(latitude=ALVO[0], longitude=ALVO[1]).interp(
            valid_time=np.datetime64(hora)).sel(pressure_level=600))) for x in ("t", "q")}
        R["por_hora"][hora] = H

    # resumo
    def est(vals):
        a = np.array(vals); return {"media": round(float(a.mean()), 3), "min": round(float(a.min()), 3), "max": round(float(a.max()), 3)}
    todos = [M for h in R["por_hora"].values() for M in h["membros"]]
    S = {"z_0C_m": est([M["z_0C_m"] for M in todos]), "z_0C_bulbo_umido_m": est([M["z_0C_bulbo_umido_m"] for M in todos]),
         "vento_medio_abaixo_0C_ms": est([M["vento_medio_abaixo_0C_ms"] for M in todos]),
         "gelo_para_isotermica_ate_5000m_mm": est([M["gelo_para_isotermica_mm"]["ate_5000m"] for M in todos]),
         "gelo_para_isotermica_ate_4638m_mm": est([M["gelo_para_isotermica_mm"]["ate_4638m"] for M in todos]),
         "agua_precipitavel_acima_5000m_mm": est([M["agua_precipitavel_acima_5000m_mm"] for M in todos])}
    S["pouso_solta_7000m_sobre_alvo"] = {
        c: {"distancia_km": est([np.hypot(x, y) for x, y, _ in v]), "fracao_na_bacia_do_ponto": round(float(np.mean([b for *_, b in v])), 2),
            "fracao_ate_1km": round(float(np.mean([np.hypot(x, y) <= 1.0 for x, y, _ in v])), 2)}
        for c, v in pousos.items()}
    S["massa_restante_solta_7000m"] = {c: dict(zip(["5634m", "5000m", "4638m"], [est(list(col)) for col in np.array(v).T]))
                                       for c, v in sobrevive.items()}
    S["vento_necessario_diferenca_ms"] = {"%s | %s @ %d m" % k: {"diferenca_ms": est([a for a, _ in v]),
                                                                 "em_desvios": est([a / max(s, 1e-3) for a, s in v])}
                                          for k, v in req.items() if k[2] in (6400.0, 7600.0)}
    # precipitacao dos membros sobre a bacia, 21-03 UTC (acumulados de 3 h que terminam as 00 e as 03)
    tp = sl_a.tp.interp(latitude=ALVO[0], longitude=ALVO[1]).sel(valid_time=["2026-08-26T00", "2026-08-26T03"]).sum("valid_time").values * 1e3
    tp4 = sl_a.tp.sel(latitude=[28.5, 28.0], longitude=[85.5, 86.0], valid_time=["2026-08-26T00", "2026-08-26T03"]).sum("valid_time").max(("latitude", "longitude")).values * 1e3
    cape = sl_i.cape.interp(latitude=ALVO[0], longitude=ALVO[1]).sel(valid_time="2026-08-26T00").values
    S["cape_regional_media_membros"] = {}
    for t in ("2026-08-25T18", "2026-08-25T21", "2026-08-26T00"):
        c = sl_i.cape.sel(valid_time=t).mean("number")
        i, j = np.unravel_index(int(c.values.argmax()), c.shape)
        d = np.hypot((c.latitude.values[i] - ALVO[0]) * KM_LAT, (c.longitude.values[j] - ALVO[1]) * KM_LON)
        S["cape_regional_media_membros"][t] = {"max_J_kg": round(float(c.values.max())), "lat": float(c.latitude.values[i]),
                                               "lon": float(c.longitude.values[j]), "dist_km": round(float(d)),
                                               "no_no_28N_85E_J_kg": round(float(c.sel(latitude=28.0, longitude=85.0)))}
    S["precipitacao_membros_21_03UTC"] = {"no_alvo_mm": [round(float(x), 3) for x in tp],
                                          "maximo_4_nos_vizinhos_mm": [round(float(x), 3) for x in tp4],
                                          "massa_na_bacia_kg": [float("%.2g" % (x * AREA_BACIA)) for x in tp],
                                          "cape_superficie_00UTC_J_kg": [round(float(x), 1) for x in cape]}
    # entrada de ar para pôr M kg na bacia em 2,5 h: celula de raio Rc chovendo por igual, eficiencia 0,3
    pf = perfis(ens, det, "2026-08-26T00:00")
    f = fino(pf[0], zz)
    Win = float(np.mean([np.sum((fino(p_, zz)["rho"] * fino(p_, zz)["q"])[(zz >= 4400) & (zz <= 6700)]) * 10.0 for p_ in pf]))
    rho_q550 = float(np.mean([np.interp(5100.0, zz, fino(p_, zz)["rho"] * fino(p_, zz)["q"]) for p_ in pf]))
    E = {"vapor_600_450hPa_kg_m2": round(Win, 2), "eficiencia": 0.3, "duracao_h": 2.5, "casos": []}
    for Mk in (1e6, 1e7, 1e8):
        for Rc in (2e3, 5e3):
            Ac = np.pi * Rc ** 2
            Mc = Mk * Ac / AREA_BACIA / 0.3
            uin = Mc / (2.5 * 3600 * 2 * np.pi * Rc * Win)
            E["casos"].append({"massa_na_bacia_kg": Mk, "raio_celula_km": Rc / 1e3,
                               "precip_na_celula_mm": round(Mk / AREA_BACIA, 2),
                               "entrada_radial_ms": round(float(uin), 3), "convergencia_por_s": float("%.2g" % (2 * uin / Rc)),
                               "ascensao_na_base_ms": round(float(Mc / (2.5 * 3600 * Ac * rho_q550)), 3)})
    S["entrada_necessaria"] = E
    R["resumo"] = S
    json.dump(R, open(os.path.join(SAIDA, "transporte_era5_ens.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    texto(R)
    figura(R, pousos, perfis_massa, zz, req)


def texto(R):
    S = R["resumo"]
    L = ["Transporte do gelo ate a frente de gelo (28,2918 N / 85,5284 E, 5,0 km) com o ERA5 em ensemble (EDA, 10 membros)",
         "horas: " + ", ".join(R["horas"]), ""]
    for k in ("z_0C_m", "z_0C_bulbo_umido_m", "vento_medio_abaixo_0C_ms", "gelo_para_isotermica_ate_5000m_mm",
              "gelo_para_isotermica_ate_4638m_mm", "agua_precipitavel_acima_5000m_mm"):
        L.append("%-38s media %8.2f  min %8.2f  max %8.2f" % (k, S[k]["media"], S[k]["min"], S[k]["max"]))
    L += ["", "Solta a 7,0 km sobre o alvo: distancia do pouso a 5,0 km, fracao na bacia do ponto, massa restante (5,63 / 5,0 / 4,64 km)"]
    for c, v in S["pouso_solta_7000m_sobre_alvo"].items():
        mr = S["massa_restante_solta_7000m"][c]
        L.append("  %-22s %5.2f km (%.2f-%.2f)  ate 1 km %.2f  bacia %.2f   massa %.2f / %.2f / %.2f" % (
            c, v["distancia_km"]["media"], v["distancia_km"]["min"], v["distancia_km"]["max"], v["fracao_ate_1km"], v["fracao_na_bacia_do_ponto"],
            mr["5634m"]["media"], mr["5000m"]["media"], mr["4638m"]["media"]))
    L += ["", "Vento necessario menos vento efetivo do ERA5 (m/s) e em desvios do ensemble, solta a 6,4 e 7,6 km"]
    for k, v in S["vento_necessario_diferenca_ms"].items():
        L.append("  %-62s %6.2f m/s (%.2f-%.2f)  %7.1f desvios" % (k, v["diferenca_ms"]["media"], v["diferenca_ms"]["min"],
                                                                  v["diferenca_ms"]["max"], v["em_desvios"]["media"]))
    P_ = S["precipitacao_membros_21_03UTC"]
    L += ["", "Precipitacao dos membros 21-03 UTC no alvo (mm): " + " ".join("%.3f" % x for x in P_["no_alvo_mm"]),
          "  maximo nos 4 nos vizinhos (mm): " + " ".join("%.2f" % x for x in P_["maximo_4_nos_vizinhos_mm"]),
          "  massa na bacia (kg): " + " ".join("%.2g" % x for x in P_["massa_na_bacia_kg"]),
          "  CAPE de superficie 00 UTC (J/kg): " + " ".join("%.1f" % x for x in P_["cape_superficie_00UTC_J_kg"]),
          "  CAPE regional (media dos membros): " + "; ".join("%s max %d J/kg em %.1f/%.1f (%d km), no no 28/85 %d" % (
              t, v["max_J_kg"], v["lat"], v["lon"], v["dist_km"], v["no_no_28N_85E_J_kg"]) for t, v in S["cape_regional_media_membros"].items()), ""]
    for h, H in R["por_hora"].items():
        L.append("%s  div 600-450 %.2g +- %.2g /s  omega500 %.3f +- %.3f Pa/s  spread500 %s  CAPE elevado (det.) %s" % (
            h, H["divergencia_600_450hPa_por_s"]["media"], H["divergencia_600_450hPa_por_s"]["desvio"],
            H["omega_500hPa_Pa_s"]["media"], H["omega_500hPa_Pa_s"]["desvio"], H["spread_produto_500hPa"],
            H["cape_elevado_deterministico_J_kg"]))
        L.append("    para conveccao (parcela de 600 hPa, det.): %s  spread600 %s" % (H["perturbacao_para_conveccao_600hPa"], H["spread_produto_600hPa"]))
    E = S["entrada_necessaria"]
    L += ["", "Entrada necessaria (eficiencia %.1f, %.1f h, vapor 600-450 hPa %.1f kg/m2)" % (E["eficiencia"], E["duracao_h"], E["vapor_600_450hPa_kg_m2"])]
    for c in E["casos"]:
        L.append("  M %.0e kg  Rc %.0f km  chuva %6.1f mm  entrada %.3f m/s  convergencia %.2g /s  ascensao na base %.3f m/s" % (
            c["massa_na_bacia_kg"], c["raio_celula_km"], c["precip_na_celula_mm"], c["entrada_radial_ms"],
            c["convergencia_por_s"], c["ascensao_na_base_ms"]))
    open(os.path.join(SAIDA, "transporte_era5_ens.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


def figura(R, pousos, perfis_massa, zz, req):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    tx, tx2, grade = "#0b0b0b", "#52514e", "#d9d8d4"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": tx2, "axes.labelcolor": tx, "xtick.color": tx2, "ytick.color": tx2})
    fig, axs = plt.subplots(1, 3, figsize=(17, 5.6))
    # (a) mapa: pousos, bacia, fontes e relevo
    ax = axs[0]
    lat, lon, z = relevo()
    X = (lon - ALVO[1]) * KM_LON; Y = (lat - ALVO[0]) * KM_LAT
    sx = (X > -7) & (X < 4); sy = (Y > -5) & (Y < 3)
    ax.contour(X[sx], Y[sy], z[np.ix_(sy, sx)], levels=np.arange(3500, 7500, 250), colors=grade, linewidths=0.5)
    cs = ax.contour(X[sx], Y[sy], z[np.ix_(sy, sx)], levels=[5000, 6000, 7000], colors=tx2, linewidths=0.8)
    ax.clabel(cs, fmt="%d m", fontsize=7)
    bac = np.load(os.path.join(RAIZ, "data", "processed", "ponto_drone", "bacia_ponto.npz"))
    bx = (bac["lon"] - ALVO[1]) * KM_LON; by = (bac["lat"] - ALVO[0]) * KM_LAT
    ax.contour(bx, by, bac["mascara"].astype(float), levels=[0.5], colors=tx, linewidths=1.4)
    for (c, v), cor in zip(pousos.items(), CORES):
        a = np.array([(x, y) for x, y, _ in v])
        ax.scatter(a[:, 0], a[:, 1], s=14, color=cor, edgecolor="white", linewidth=0.5, label=c, zorder=3)
    for nf, (fla, flo) in FONTES.items():
        if nf == "sobre o alvo":
            continue
        fx, fy = (flo - ALVO[1]) * KM_LON, (fla - ALVO[0]) * KM_LAT
        ax.annotate("", xy=(0, 0), xytext=(fx, fy), arrowprops=dict(arrowstyle="->", color=tx2, lw=1, ls="--"))
        ax.plot(fx, fy, "s", color=tx2, ms=6); ax.text(fx, fy - 0.35, nf, fontsize=7, color=tx, ha="center", va="top")
    ax.plot(0, 0, "*", color=tx, ms=12); ax.text(0.15, 0.2, "frente de gelo", fontsize=8, color=tx)
    ax.plot((P[1] - ALVO[1]) * KM_LON, (P[0] - ALVO[0]) * KM_LAT, "o", mfc="none", mec=tx, ms=7)
    ax.set_xlim(-7, 4); ax.set_ylim(-5, 3); ax.set_aspect(1)
    ax.set_xlabel("km a leste da frente de gelo"); ax.set_ylabel("km ao norte")
    ax.set_title("a) Pouso a 5,0 km, soltando a 7,0 km sobre a frente\n(10 membros x 5 horas; contorno preto = bacia do ponto)", fontsize=9, color=tx)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    # (b) massa restante com a altura (solta a 7,0 km), media dos membros
    ax = axs[1]
    S = R["resumo"]
    ax.axhspan(S["z_0C_m"]["min"] / 1e3, S["z_0C_m"]["max"] / 1e3, color=grade, alpha=0.6, lw=0)
    ax.text(1.01, S["z_0C_m"]["max"] / 1e3 - 0.02, "0 °C", fontsize=7, color=tx2, va="top")
    ax.axhspan(S["z_0C_bulbo_umido_m"]["min"] / 1e3, S["z_0C_bulbo_umido_m"]["max"] / 1e3, color=grade, alpha=0.35, lw=0)
    ax.text(1.01, S["z_0C_bulbo_umido_m"]["max"] / 1e3 - 0.02, "0 °C de\nbulbo úmido", fontsize=7, color=tx2, va="top")
    ax.axhline(Z_TOPO_BACIA / 1e3, color=tx2, lw=0.6, ls=":"); ax.text(1.01, Z_TOPO_BACIA / 1e3 + 0.01, "topo da bacia", fontsize=7, color=tx2)
    ax.axhspan(4.8, 5.15, xmax=0.06, color=tx2, alpha=0.5, lw=0); ax.text(0.07, 4.81, "frente de gelo", fontsize=7, color=tx2)
    ax.axhline(Z_PONTO / 1e3, color=tx2, lw=0.6, ls=":"); ax.text(1.01, Z_PONTO / 1e3 + 0.01, "ponto do drone", fontsize=7, color=tx2)
    for (c, v), cor in zip(perfis_massa.items(), CORES):
        a = np.array(v); ok = np.isfinite(a).all(axis=0)
        ax.fill_betweenx(zz[ok] / 1e3, a[:, ok].min(axis=0), a[:, ok].max(axis=0), color=cor, alpha=0.15, lw=0)
        ax.plot(a[:, ok].mean(axis=0), zz[ok] / 1e3, color=cor, lw=2, label=c)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.set_xlim(0, 1.18); ax.set_ylim(4.55, 6.0)
    ax.set_xlabel("fração da massa de gelo que resta"); ax.set_ylabel("altitude (km)")
    ax.set_title("b) Fusão na queda (Mason 1956, com ventilação)\nsolta a 7,0 km; faixa = mín-máx dos membros", fontsize=9, color=tx)
    ax.grid(axis="x", color=grade, lw=0.5)
    # (c) vento necessario menos o do ERA5, por fonte (solta a 7,0 km), contra o desvio do ensemble
    ax = axs[2]
    fontes = [f for f in FONTES if f != "sobre o alvo"]
    for j, (c, cor) in enumerate(zip([c[0] for c in CLASSES], CORES)):
        for i, nf in enumerate(fontes):
            v = req[(nf, c, 7000.0)]
            ax.plot([a for a, _ in v], [i + (j - 2) * 0.12] * len(v), "o", color=cor, ms=5, mec="white", mew=0.5,
                    label=c if i == 0 else None)
    sig = np.mean([s for v in req.values() for _, s in v])
    ax.axvspan(0.1, 3 * sig, color=grade, lw=0)
    ax.text(0.12, len(fontes) - 0.55, "até 3 desvios\ndo ensemble\n(%.1f m/s)" % (3 * sig), fontsize=7, color=tx2, va="top")
    ax.set_yticks(range(len(fontes))); ax.set_yticklabels(fontes, fontsize=8)
    ax.set_xscale("log"); ax.set_xlim(0.1, 200); ax.set_ylim(-0.5, len(fontes) - 0.4)
    ax.set_xlabel("vento necessário − vento efetivo do ERA5 (m/s)")
    ax.set_title("c) Quanto o vento teria de errar para levar o gelo\nda fonte à frente (solta a 7,0 km; 5 horas)", fontsize=9, color=tx)
    ax.grid(axis="x", color=grade, lw=0.5, which="both")
    ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3)
    for a in axs:
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(SAIDA, "transporte_era5_ens.png"), dpi=130, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
