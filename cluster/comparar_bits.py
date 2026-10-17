# -*- coding: utf-8 -*-
"""
Compara, variavel a variavel e byte a byte, duas saidas GrADS do CM1 (mesma grade, mesmo namelist) nos
registros de tempo comuns. Uso: python3 comparar_bits.py <dir_A> <dir_B> [s u v w]

z0t e z0q sao IGNORADOS: sao diagnosticos de saida da camada superficial (sfcmodel=2) com memoria nao
inicializada em parte da grade (NaN numa rodada, lixo desnormalizado noutra); nao realimentam o modelo
(verificado: todas as outras variaveis identicas com eles diferentes). Eles sao listados a parte.
"""
import os, re, sys
import numpy as np

IGNORAR = {"z0t", "z0q"}


def compara(ctl, a, b):
    txt = open(ctl).read()
    nx = int(re.search(r"xdef\s+(\d+)", txt).group(1)); ny = int(re.search(r"ydef\s+(\d+)", txt).group(1))
    linhas = re.search(r"\nvars\s+\d+\n(.*?)\nendvars", txt, re.S).group(1).splitlines()
    vs = [(l.split()[0], max(int(l.split()[1]), 1)) for l in linhas]
    rec = sum(k for _, k in vs) * nx * ny * 4
    nt = min(os.path.getsize(a), os.path.getsize(b)) // rec
    A = np.memmap(a, "<f4", "r"); B = np.memmap(b, "<f4", "r")
    ok = True
    for t in range(nt):
        off = t * rec // 4; dif, ign = [], []
        for nome, k in vs:
            n = k * nx * ny; x = A[off:off + n].view("<u4"); y = B[off:off + n].view("<u4"); off += n
            m = int((x != y).sum())
            if m:
                xf, yf = A[off - n:off], B[off - n:off]
                s = "%s(%d pts, max|d|=%.3g)" % (nome, m, np.nanmax(np.abs(xf - yf)) if np.isfinite(xf - yf).any() else float("nan"))
                (ign if nome in IGNORAR else dif).append(s)
        ok &= not dif
        print("  t=%d: %s%s" % (t, "IDENTICO" if not dif else "DIFERE: " + "; ".join(dif),
                                ("   [ignorados: %s]" % ", ".join(ign)) if ign else ""))
    return ok, nt


def main():
    da, db = sys.argv[1], sys.argv[2]
    arqs = sys.argv[3:] or ["s", "u", "v", "w"]
    tudo = True
    for f in arqs:
        ctl = os.path.join(da, "cm1out_%s.ctl" % f)
        print("cm1out_%s:" % f)
        ok, nt = compara(ctl, os.path.join(da, "cm1out_%s.dat" % f), os.path.join(db, "cm1out_%s.dat" % f))
        print("  -> %d saidas comparadas: %s" % (nt, "IDENTICAS" if ok else "DIFEREM"))
        tudo &= ok
    print("RESULTADO:", "BIT A BIT IDENTICO (exceto diagnosticos z0t/z0q)" if tudo else "HA DIFERENCAS")
    sys.exit(0 if tudo else 1)


if __name__ == "__main__":
    main()
