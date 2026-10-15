# -*- coding: utf-8 -*-
"""
Serie temporal horaria de Jz sobre o Himalaia, 21 a 28 de agosto de 2026.

TRES CAMADAS, declaradas separadamente. Nenhuma e apresentada como a outra:

  [MEDIDO]        variacao de raios cosmicos (NMDB, monitores de neutrons,
                  contagem horaria). Fornece dRc/Rc via sigma ~ sqrt(q).
  [CLIMATOLOGIA]  curva de Carnegie para a variacao diurna do potencial
                  ionosferico VI. E climatologia estabelecida desde 1920,
                  NAO medicao desta data. VI nao e medido rotineiramente.
  [CONSTANTE]     resistencia colunar de referencia Rc0 a ~4.000 m, adotada.
                  Fixa apenas o nivel absoluto; nao afeta as variacoes.

  Jz(t) = VI_carnegie(UT) / Rc0 * sqrt( GCR(t) / GCR_base )

Uso: python scripts/serie_jz_2026.py
"""
import ssl
import urllib.request
import datetime as dt

import numpy as np

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# [CONSTANTE] resistencia colunar a ~4.000 m. Fixa o nivel, nao as variacoes.
RC0 = 0.78e17          # Ohm.m2

# [CLIMATOLOGIA] curva de Carnegie: VI relativo por hora UT (media = 1).
# Minimo ~03 UT, maximo ~19 UT, amplitude pico-a-pico de ~35 %.
CARNEGIE = np.array([
    0.92, 0.89, 0.87, 0.86, 0.86, 0.87, 0.89, 0.91, 0.93, 0.96,
    0.99, 1.02, 1.05, 1.08, 1.11, 1.13, 1.15, 1.16, 1.17, 1.16,
    1.13, 1.08, 1.02, 0.96])
VI_MEDIO = 250.0e3     # V

T0 = dt.datetime(2026, 8, 21)
T1 = dt.datetime(2026, 8, 28, 23)

MARCOS = [
    (dt.datetime(2026, 8, 25, 10, 2), "flare M6.9 (AR 4513)"),
    (dt.datetime(2026, 8, 25, 18, 0), "pico do sistema convectivo (8.413 km2 < -60 C)"),
    (dt.datetime(2026, 8, 26, 2, 52), "COLAPSO  Ms 5,2 landslide"),
    (dt.datetime(2026, 8, 26, 6, 0), "2o deslizamento  Ms 4,2"),
]


def nmdb(st, t0, t1):
    u = ("https://www.nmdb.eu/nest/draw_graph.php?formchk=1&stations[]=%s"
         "&tabchoice=revori&dtype=corr_for_efficiency&tresolution=60&force=1"
         "&yunits=0&date_choice=bydate"
         "&start_day=%d&start_month=%d&start_year=%d&start_hour=0&start_min=0"
         "&end_day=%d&end_month=%d&end_year=%d&end_hour=23&end_min=59"
         "&output=ascii") % (st, t0.day, t0.month, t0.year, t1.day, t1.month, t1.year)
    with urllib.request.urlopen(u, timeout=180, context=CTX) as r:
        txt = r.read().decode("utf-8", "replace")
    T, V = [], []
    for ln in txt.splitlines():
        ln = ln.strip()
        if not ln[:4].isdigit() or ";" not in ln:
            continue
        a, _, b = ln.partition(";")
        try:
            T.append(dt.datetime.strptime(a.strip(), "%Y-%m-%d %H:%M:%S"))
            V.append(float(b.strip()))
        except ValueError:
            pass
    return np.array(T), np.array(V, dtype=float)


def main():
    print("=" * 100)
    print("SERIE HORARIA DE Jz SOBRE O HIMALAIA — 21 a 28 de agosto de 2026")
    print("=" * 100)

    dados = {}
    for st in ("OULU", "ATHN", "MXCO"):
        try:
            T, V = nmdb(st, T0.date(), T1.date())
            if T.size:
                dados[st] = (T, V)
                print("  [MEDIDO] %s: %d horas, contagem %.2f a %.2f" % (st, T.size, V.min(), V.max()))
        except Exception as ex:
            print("  %s falhou: %s" % (st, str(ex)[:60]))
    if not dados:
        raise SystemExit("nenhum monitor de neutrons respondeu")

    T, V = dados.get("OULU", list(dados.values())[0])
    base = np.median(V)
    horas = np.array([(t - T0).total_seconds() / 3600.0 for t in T])
    ut = np.array([t.hour for t in T])

    vi = VI_MEDIO * CARNEGIE[ut]                       # [CLIMATOLOGIA]
    fator = np.sqrt(V / base)                          # [MEDIDO]
    jz = vi / RC0 * fator * 1e12                       # pA/m2
    jz_sem_gcr = vi / RC0 * 1e12                       # so a curva de Carnegie

    print("\n  linha de base de GCR (mediana OULU): %.3f" % base)
    print("  Jz: min %.3f | media %.3f | max %.3f pA/m2" % (jz.min(), jz.mean(), jz.max()))
    print("  amplitude total da serie: %.3f pA/m2 (%.1f %%)"
          % (jz.max() - jz.min(), 100 * (jz.max() - jz.min()) / jz.mean()))
    print("  contribuicao da climatologia (Carnegie): %.3f pA/m2 (%.1f %%)"
          % (jz_sem_gcr.max() - jz_sem_gcr.min(),
             100 * (jz_sem_gcr.max() - jz_sem_gcr.min()) / jz_sem_gcr.mean()))
    resid = jz - jz_sem_gcr
    print("  contribuicao MEDIDA dos raios cosmicos:  %.3f pA/m2 (%.2f %%)"
          % (resid.max() - resid.min(),
             100 * (resid.max() - resid.min()) / jz.mean()))

    print("\n" + "=" * 100)
    print("Jz NOS INSTANTES-CHAVE")
    print("=" * 100)
    print("%-46s %-18s %10s %12s" % ("marco", "UTC", "Jz pA/m2", "GCR %"))
    for tm, rot in MARCOS:
        i = int(np.argmin(np.abs(horas - (tm - T0).total_seconds() / 3600.0)))
        print("%-46s %-18s %10.3f %+11.2f" %
              (rot, tm.strftime("%d/%m %H:%M"), jz[i], 100 * (V[i] - base) / base))

    print("\n" + "=" * 100)
    print("COMPARACAO COM O QUE O MODELO ANTERIOR AFIRMAVA")
    print("=" * 100)
    ifl = int(np.argmin(np.abs(horas - (MARCOS[0][0] - T0).total_seconds() / 3600.0)))
    print("  Jz medido na hora do flare        : %.3f pA/m2" % jz[ifl])
    print("  Jz maximo de toda a semana        : %.3f pA/m2  (em %s UTC)"
          % (jz.max(), T[int(np.argmax(jz))].strftime("%d/%m %H:%M")))
    print("  Jz alegado no modelo do repositorio: 4.570 pA/m2 no instante do flare")
    print("  o pico da serie medida ocorre em   : %s UTC" % T[int(np.argmax(jz))].strftime("%d/%m %H:%M"))
    print("  o colapso ocorreu em               : 26/08 02:52 UTC")

    np.save(r"C:\Users\haas\AppData\Local\Temp\jz_serie.npy",
            np.array([horas, jz, jz_sem_gcr, V], dtype=float))
    print("\n  serie salva para plotagem")


if __name__ == "__main__":
    main()
