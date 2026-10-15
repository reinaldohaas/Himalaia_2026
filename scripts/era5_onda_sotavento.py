# -*- coding: utf-8 -*-
"""
TESTE DA HIPOTESE DE ONDA DE SOTAVENTO — ERA5, 15 eventos himalaios.

A hipotese em teste NAO e conveccao profunda. E:
    nuvem entrando em sotavento da montanha, em ambiente de cisalhamento,
    com ascendencia sustentada sobre o anfiteatro, acumulando agua liquida
    SUPER-RESFRIADA que nao precipita (goticulas monodispersas), ate colapsar.

As condicoes necessarias sao mensuraveis na reanalise:
  1. escoamento forte cruzando a crista (nivel de cume ~500 hPa)
  2. cisalhamento vertical
  3. estratificacao estavel (N2 > 0) -> onda retida
  4. parametro de Scorer DECRESCENDO com a altura -> onda aprisionada
  5. ascendencia (omega < 0)
  6. AGUA LIQUIDA SUPER-RESFRIADA na coluna entre 0 e -20 C

GRUPO-CONTROLE INTERNO: para cada evento, baixa-se +/-15 dias. A janela de 48 h
anterior ao colapso e comparada com TODAS as outras janelas de 48 h do mesmo
periodo. Isso casa estacao e regime sinotico por construcao, e exige uma unica
requisicao por evento.

LIMITACAO DECLARADA: ERA5 tem 0,25 graus (~28 km). Ele NAO resolve a onda de
sotavento nem o anfiteatro de 3,4 km2. Resolve as CONDICOES NECESSARIAS --
escoamento, cisalhamento, estabilidade e agua super-resfriada na coluna. A
ausencia delas refuta; a presenca nao prova.

Credencial: ~/.cdsapirc (nao e impressa nem transmitida a outro destino).
Uso:  python scripts/era5_onda_sotavento.py --baixar
      python scripts/era5_onda_sotavento.py --analisar
"""
import os
import sys
import datetime as dt

import numpy as np

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "raw", "era5")
os.makedirs(DIR, exist_ok=True)

EVENTOS = [
    ("kedarnath_2013",   dt.datetime(2013, 6, 17, 1, 45), 79.067, 30.745),
    ("chamoli_2021",     dt.datetime(2021, 2,  7, 4, 51), 79.732, 30.378),
    ("himalaia_2026",    dt.datetime(2026, 8, 26, 2, 52), 85.515, 28.271),
    ("aru_2016",         dt.datetime(2016, 7, 17, 4,  0), 82.285, 34.045),
    ("seti_2012",        dt.datetime(2012, 5,  5, 3, 30), 84.152, 28.542),
    ("south_lhonak_2023",dt.datetime(2023,10,  3,18, 30), 88.205, 27.905),
    ("leh_2010",         dt.datetime(2010, 8,  5,20,  0), 77.577, 34.152),
    ("melamchi_2021",    dt.datetime(2021, 6, 15,12,  0), 85.612, 28.095),
    ("parechu_2000",     dt.datetime(2000, 8,  1,12,  0), 78.536, 32.028),
    ("zhangzangbo_1981", dt.datetime(1981, 7, 11,12,  0), 86.045, 28.175),
    ("dig_tsho_1985",    dt.datetime(1985, 8,  4,12,  0), 86.600, 27.870),
    ("luggye_tsho_1994", dt.datetime(1994,10,  7,12,  0), 90.300, 28.080),
    ("bhotekoshi_2016",  dt.datetime(2016, 7,  5,12,  0), 85.965, 28.026),
    ("himachal_2023",    dt.datetime(2023, 7,  9,12,  0), 77.150, 31.985),
    ("parechu_2005",     dt.datetime(2005, 6, 26,12,  0), 78.558, 31.956),
]

# enxugado ao que as metricas usam: o CDS impoe limite de custo por requisicao
# (n_variaveis x n_niveis x n_horarios x n_dias) e recusa com 403 acima dele.
NIVEIS = ["400", "450", "500", "550", "600"]
VARS = ["temperature", "u_component_of_wind", "v_component_of_wind",
        "vertical_velocity", "specific_cloud_liquid_water_content"]
HORAS = ["00:00", "06:00", "12:00", "18:00"]
DIAS = 15          # +/- em torno do evento
JANELA = 48        # horas antes do evento


def baixar():
    """
    Uma requisicao POR MES. O CDS expande year x month x day no produto
    cartesiano: pedir dois meses de uma vez multiplica os dias por dois e
    estoura o limite de custo. Os pedacos sao concatenados na leitura.
    """
    import cdsapi
    c = cdsapi.Client()
    for eid, tev, lon, lat in EVENTOS:
        d0 = (tev - dt.timedelta(days=DIAS)).date()
        d1 = (tev + dt.timedelta(days=DIAS)).date()
        # agrupa os dias por (ano, mes)
        blocos = {}
        d = d0
        while d <= d1:
            blocos.setdefault((d.year, d.month), []).append("%02d" % d.day)
            d += dt.timedelta(days=1)
        for (ano, mes), dias in sorted(blocos.items()):
            alvo = os.path.join(DIR, "%s_%04d%02d.nc" % (eid, ano, mes))
            if os.path.exists(alvo) and os.path.getsize(alvo) > 5000:
                continue
            n = len(VARS) * len(NIVEIS) * len(HORAS) * len(dias)
            print("  %-20s %04d-%02d  %2d dias  (%d campos) ..." % (eid, ano, mes, len(dias), n), flush=True)
            try:
                c.retrieve("reanalysis-era5-pressure-levels", {
                    "product_type": ["reanalysis"],
                    "variable": VARS,
                    "pressure_level": NIVEIS,
                    "year": ["%04d" % ano], "month": ["%02d" % mes], "day": dias,
                    "time": HORAS,
                    "area": [lat + 0.5, lon - 0.5, lat - 0.5, lon + 0.5],
                    "data_format": "netcdf",
                    "download_format": "unarchived",
                }, alvo)
                print("     -> %.2f MB" % (os.path.getsize(alvo) / 1e6), flush=True)
            except Exception as ex:
                print("     FALHOU: %s" % str(ex)[:120], flush=True)


def abrir(eid):
    """concatena os pedacos mensais de um evento"""
    import xarray as xr
    import glob
    fs = sorted(glob.glob(os.path.join(DIR, "%s_*.nc" % eid)))
    if not fs:
        return None
    if len(fs) == 1:
        return xr.open_dataset(fs[0])
    return xr.concat([xr.open_dataset(f) for f in fs], dim="valid_time").sortby("valid_time")


def metricas(ds, lon, lat):
    """devolve dict de series temporais das condicoes necessarias"""
    import xarray as xr
    v = {n: ds[n] for n in ds.data_vars}
    # nomes curtos variam entre entregas do CDS
    def get(*nomes):
        for n in nomes:
            if n in ds:
                return ds[n]
        raise KeyError(nomes[0])
    T = get("t", "temperature")
    U = get("u", "u_component_of_wind")
    V = get("v", "v_component_of_wind")
    W = get("w", "vertical_velocity")
    Q = get("clwc", "specific_cloud_liquid_water_content")
    dims = [d for d in T.dims if d not in ("valid_time", "time", "pressure_level", "level")]
    T = T.mean(dims); U = U.mean(dims); V = V.mean(dims); W = W.mean(dims); Q = Q.mean(dims)
    lev = ds["pressure_level"].values if "pressure_level" in ds else ds["level"].values
    lev = np.asarray(lev, dtype=float)
    i500 = int(np.argmin(np.abs(lev - 500)))
    i400 = int(np.argmin(np.abs(lev - 400)))
    i600 = int(np.argmin(np.abs(lev - 600)))
    Tv, Uv, Vv, Wv, Qv = (np.asarray(x.values, dtype=float) for x in (T, U, V, W, Q))
    if Tv.ndim == 2 and Tv.shape[0] == lev.size:      # (nivel, tempo) -> (tempo, nivel)
        Tv, Uv, Vv, Wv, Qv = (x.T for x in (Tv, Uv, Vv, Wv, Qv))
    spd = np.hypot(Uv, Vv)
    cis = np.hypot(Uv[:, i400] - Uv[:, i600], Vv[:, i400] - Vv[:, i600])
    # estabilidade: N2 ~ (g/T) (dT/dz + g/cp), com dz da hipsometrica
    g, Rd, cp = 9.80665, 287.05, 1004.0
    dz = Rd * Tv[:, i500] / g * np.log(lev[i600] / lev[i400])
    dTdz = (Tv[:, i400] - Tv[:, i600]) / np.maximum(dz, 1.0)
    N2 = g / Tv[:, i500] * (dTdz + g / cp)
    scorer = N2 / np.maximum(spd[:, i500] ** 2, 1.0)
    # agua liquida super-resfriada: clwc onde -20 C < T < 0 C, integrada na coluna
    mask = (Tv < 273.15) & (Tv > 253.15)
    dp = np.gradient(lev) * 100.0
    slwc = np.nansum(np.where(mask, Qv, 0.0) * np.abs(dp)[None, :] / g, axis=1)  # kg/m2
    return {"vento500": spd[:, i500], "cisalhamento": cis, "N2": N2,
            "scorer": scorer, "omega500": Wv[:, i500], "slwc": slwc}


def analisar():
    import xarray as xr
    print("=" * 104)
    print("CONDICOES DE ONDA DE SOTAVENTO NAS 48 h ANTERIORES — percentil no proprio mes")
    print("=" * 104)
    print("%-20s %11s %11s %11s %11s %11s" %
          ("evento", "vento500", "cisalham.", "Scorer", "omega500", "SLWC"))
    print("%-20s %11s %11s %11s %11s %11s" %
          ("", "m/s (pct)", "m/s (pct)", "(pct)", "asc. (pct)", "kg/m2 (pct)"))
    acum = {k: [] for k in ("vento500", "cisalhamento", "scorer", "omega500", "slwc")}
    for eid, tev, lon, lat in EVENTOS:
        try:
            ds = abrir(eid)
            if ds is None:
                print("%-20s  sem arquivo" % eid); continue
            M = metricas(ds, lon, lat)
            tn = ds["valid_time"] if "valid_time" in ds else ds["time"]
            tt = np.array([np.datetime64(x, "s").astype(dt.datetime) for x in tn.values])
        except Exception as ex:
            print("%-20s  erro: %s" % (eid, str(ex)[:52])); continue
        rel = np.array([(x - tev).total_seconds() / 3600.0 for x in tt])
        jan = (rel >= -JANELA) & (rel <= 0)
        ctl = (rel < -JANELA) | (rel > 24)
        if jan.sum() < 8 or ctl.sum() < 50:
            print("%-20s  janela insuficiente" % eid); continue
        saida = []
        for k in ("vento500", "cisalhamento", "scorer", "omega500", "slwc"):
            x = M[k]
            ev = np.nanmean(x[jan])
            base = x[ctl]
            base = base[np.isfinite(base)]
            if k == "omega500":          # ascendencia = omega negativo
                pct = 100.0 * (base > ev).mean()
            else:
                pct = 100.0 * (base < ev).mean()
            acum[k].append(pct)
            saida.append("%7.2f(%2.0f)" % (ev, pct))
        print("%-20s %11s %11s %11s %11s %11s" % (eid, *saida))
    print("\n" + "=" * 104)
    print("MEDIA DOS PERCENTIS (sob a hipotese nula: 50 %, EP = 28,87/sqrt(n))")
    print("=" * 104)
    from math import erf, sqrt
    for k, rot in (("vento500", "vento a 500 hPa"), ("cisalhamento", "cisalhamento 400-600"),
                   ("scorer", "parametro de Scorer"), ("omega500", "ascendencia"),
                   ("slwc", "agua liquida super-resfriada")):
        v = np.array(acum[k])
        v = v[np.isfinite(v)]
        if v.size < 3:
            continue
        ep = 28.87 / np.sqrt(v.size)
        z = (v.mean() - 50.0) / ep
        p = 0.5 * (1 - erf(abs(z) / sqrt(2)))
        print("  %-30s n=%2d  media %5.1f %%  z=%+5.2f  p=%.4f  %s"
              % (rot, v.size, v.mean(), z, p, "SIGNIFICATIVO" if p < 0.05 else ""))


if __name__ == "__main__":
    if "--baixar" in sys.argv:
        baixar()
    elif "--analisar" in sys.argv:
        analisar()
    else:
        print(__doc__)
