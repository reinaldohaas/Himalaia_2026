# -*- coding: utf-8 -*-
"""Monta viz/visualizador_cm1_lhende_2026.html: embute viz/dados/*.json no modelo visualizador_template.html."""
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
WT = os.path.dirname(os.path.dirname(AQUI))
D = os.path.join(WT, "viz", "dados")
html = open(os.path.join(AQUI, "visualizador_template.html"), encoding="utf-8").read()
for marca, arq in (("/*DADOS_RAD06*/", "cm1_rad06_ref.json"), ("/*DADOS_RAD12*/", "cm1_rad12_ref.json"), ("/*DADOS_OBS*/", "obs.json")):
    txt = open(os.path.join(D, arq), encoding="utf-8").read().replace("</", "<" + chr(92) + "/")
    html = html.replace(marca, txt)
saida = os.path.join(WT, "viz", "visualizador_cm1_lhende_2026.html")
open(saida, "w", encoding="utf-8").write(html)
print("%s: %.1f MB" % (saida, os.path.getsize(saida) / 1e6))
