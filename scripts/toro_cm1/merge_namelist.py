# -*- coding: utf-8 -*-
"""
Monta um namelist completo para o CM1 r21.1 a partir de:
  base  = CM1/run/namelist.input   (23 grupos, o que o r21.1 le em sequencia)
  toro  = toro-CM1/namelist.input  (14 grupos; os valores do toro prevalecem)

Sobrescritas explicitas (registradas no cabecalho do arquivo gerado):
  do_ib = .false.   o toro-CM1 e de terreno plano; o base traz fronteira
                    imersa ligada (do_ib=.true., ib_init=6) de outro experimento.
  + overrides passados por linha de comando (ptype, timax etc.)
"""
import io
import re
import sys

BASE = r"C:\Users\haas\github\CM1\run\namelist.input"
TORO = r"C:\Users\haas\github\toro-CM1\namelist.input"


def parse(p):
    grupos, ordem, g = {}, [], None
    for ln in io.open(p, encoding="utf-8", errors="ignore"):
        s = ln.split("!", 1)[0].strip()          # remove comentario inline
        if not s:
            continue
        m = re.match(r"&(\w+)", s)
        if m:
            g = m.group(1)
            grupos[g] = {}
            ordem.append(g)
            continue
        if s == "/":
            g = None
            continue
        if g and "=" in s:
            k, _, v = s.partition("=")
            grupos[g][k.strip()] = v.strip().rstrip(",").strip()
    return grupos, ordem


def montar(saida, overrides):
    b, ordem = parse(BASE)
    t, _ = parse(TORO)
    for g, kv in t.items():
        b.setdefault(g, {}).update(kv)
        if g not in ordem:
            ordem.append(g)
    forc = {("param20", "do_ib"): ".false."}
    forc.update(overrides)
    for (g, k), v in forc.items():
        b.setdefault(g, {})[k] = v
        if g not in ordem:
            ordem.append(g)
    with io.open(saida, "w", encoding="utf-8", newline="\n") as f:
        f.write("! gerado por merge_namelist.py: base CM1/run (23 grupos) + valores do toro-CM1\n")
        f.write("! sobrescritas: " + "; ".join("%s.%s=%s" % (g, k, v) for (g, k), v in forc.items()) + "\n")
        for g in ordem:
            f.write(" &%s\n" % g)
            for k, v in b[g].items():
                f.write(" %-22s = %s,\n" % (k, v))
            f.write(" /\n\n")
    return b


if __name__ == "__main__":
    saida = sys.argv[1]
    ov = {}
    for a in sys.argv[2:]:
        gk, _, v = a.partition("=")
        g, _, k = gk.partition(".")
        ov[(g, k)] = v
    nl = montar(saida, ov)
    print("namelist gerado: %s  (%d grupos)" % (saida, len(nl)))
    for (g, k) in [("param2", "ptype"), ("param2", "isnd"), ("param2", "iinit"),
                   ("param1", "timax"), ("param1", "tapfrq"), ("param0", "terrain_flag"),
                   ("param20", "do_ib"), ("param3", "ndcnst")]:
        print("   %-8s %-13s = %s" % (g, k, nl.get(g, {}).get(k, "<ausente>")))
