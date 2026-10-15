# -*- coding: utf-8 -*-
"""
Serie horaria de raios cosmicos (OULU) em torno dos 15 eventos, e analise de
superposicao de epocas — a tecnica padrao para procurar um sinal comum.

Cada evento e alinhado em t = 0 (instante do colapso) e a contagem e expressa
em % da mediana dos 27 dias anteriores. Se houvesse um decrescimo de Forbush
sistematico antes dos desastres, ele apareceria como um vale na media empilhada.
"""
import ssl
import urllib.request
import datetime as dt

import numpy as np

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

EVENTOS = [
    ("Kedarnath 2013",   dt.datetime(2013, 6, 17, 1, 45)),
    ("Chamoli 2021",     dt.datetime(2021, 2,  7, 4, 51)),
    ("Lhende 2026",      dt.datetime(2026, 8, 26, 2, 52)),
    ("Aru 2016",         dt.datetime(2016, 7, 17, 4,  0)),
    ("Seti 2012",        dt.datetime(2012, 5,  5, 3, 30)),
    ("South Lhonak 2023",dt.datetime(2023,10,  3,18, 30)),
    ("Leh 2010",         dt.datetime(2010, 8,  5,20,  0)),
    ("Melamchi 2021",    dt.datetime(2021, 6, 15,12,  0)),
    ("Parechu 2000",     dt.datetime(2000, 8,  1,12,  0)),
    ("Zhangzangbo 1981", dt.datetime(1981, 7, 11,12,  0)),
    ("Dig Tsho 1985",    dt.datetime(1985, 8,  4,12,  0)),
    ("Luggye 1994",      dt.datetime(1994,10,  7,12,  0)),
    ("Bhotekoshi 2016",  dt.datetime(2016, 7,  5,12,  0)),
    ("Himachal 2023",    dt.datetime(2023, 7,  9,12,  0)),
    ("Parechu 2005",     dt.datetime(2005, 6, 26,12,  0)),
]

ANTES, DEPOIS = 10, 3        # dias
ST = "OULU"


def nmdb(st, d0, d1):
    u = ("https://www.nmdb.eu/nest/draw_graph.php?formchk=1&stations[]=%s"
         "&tabchoice=revori&dtype=corr_for_efficiency&tresolution=60&force=1"
         "&yunits=0&date_choice=bydate"
         "&start_day=%d&start_month=%d&start_year=%d&start_hour=0&start_min=0"
         "&end_day=%d&end_month=%d&end_year=%d&end_hour=23&end_min=59"
         "&output=ascii") % (st, d0.day, d0.month, d0.year, d1.day, d1.month, d1.year)
    with urllib.request.urlopen(u, timeout=240, context=CTX) as r:
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


GRADE = np.arange(-ANTES * 24, DEPOIS * 24 + 1, 1.0)   # horas relativas ao evento


def main():
    print("=" * 92)
    print("SUPERPOSICAO DE EPOCAS — raios cosmicos (%s) em torno dos 15 eventos" % ST)
    print("=" * 92)
    print("Janela: -%d a +%d dias. Linha de base: mediana dos 27 dias anteriores.\n"
          % (ANTES, DEPOIS))
    emp = []
    nomes = []
    print("%-20s %8s %10s %10s %10s" % ("evento", "horas", "min %", "no t=0 %", "max %"))
    for nome, tev in EVENTOS:
        d0 = (tev - dt.timedelta(days=ANTES + 28)).date()
        d1 = (tev + dt.timedelta(days=DEPOIS)).date()
        try:
            T, V = nmdb(ST, d0, d1)
        except Exception as ex:
            print("%-20s  falha: %s" % (nome, str(ex)[:44])); continue
        if T.size < 200:
            print("%-20s  dado insuficiente" % nome); continue
        rel = np.array([(t - tev).total_seconds() / 3600.0 for t in T])
        base = np.median(V[(rel < -24) & (rel > -27 * 24)])
        pct = 100.0 * (V - base) / base
        y = np.interp(GRADE, rel, pct, left=np.nan, right=np.nan)
        emp.append(y); nomes.append(nome)
        jan = (GRADE >= -72) & (GRADE <= 0)
        i0 = int(np.argmin(np.abs(GRADE)))
        print("%-20s %8d %10.2f %10.2f %10.2f"
              % (nome, T.size, np.nanmin(y[jan]), y[i0], np.nanmax(y[jan])))

    E = np.array(emp)
    med = np.nanmean(E, axis=0)
    sem = np.nanstd(E, axis=0, ddof=1) / np.sqrt(np.sum(~np.isnan(E), axis=0))
    print("\n" + "=" * 92)
    print("MEDIA EMPILHADA (n=%d eventos)" % len(emp))
    print("=" * 92)
    print("%10s %12s %12s" % ("h rel.", "media %", "erro-padrao"))
    for hh in (-168, -120, -96, -72, -48, -24, -12, -6, 0, 6, 12, 24, 48, 72):
        i = int(np.argmin(np.abs(GRADE - hh)))
        print("%10d %12.3f %12.3f" % (hh, med[i], sem[i]))
    i0 = int(np.argmin(np.abs(GRADE)))
    print("\n  no instante do evento (t=0): %+.3f %% +/- %.3f  ->  dJz = %+.3f %%"
          % (med[i0], sem[i0], 0.5 * med[i0]))
    jan = (GRADE >= -72) & (GRADE <= 0)
    print("  minimo da media empilhada nas 72 h anteriores: %+.3f %%" % np.nanmin(med[jan]))
    print("  (um decrescimo de Forbush tipico tem 3 a 10 %%; aqui a escala e de decimos)")

    np.save(r"C:\Users\haas\AppData\Local\Temp\gcr_epocas.npy",
            np.vstack([GRADE, med, sem, E]))
    with open(r"C:\Users\haas\AppData\Local\Temp\gcr_nomes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(nomes))
    print("\n  series salvas (%d eventos x %d horas)" % (E.shape[0], E.shape[1]))


if __name__ == "__main__":
    main()
