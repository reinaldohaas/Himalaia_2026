# -*- coding: utf-8 -*-
"""Monta o relatorio HTML auto-contido: troca {{figura}} por data URI JPEG (largura <= 1800 px).
Uso: python montar_relatorio.py <dir_dados> <saida.html>"""
import base64
import io
import os
import re
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))


def main(d, saida):
    s = open(os.path.join(AQUI, "relatorio_template.html"), encoding="utf-8").read()
    def troca(m):
        im = Image.open(os.path.join(d, m.group(1) + ".png")).convert("RGB")
        if im.width > 1800:
            im = im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=84, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    s = re.sub(r"\{\{(\w+)\}\}", troca, s)
    open(saida, "w", encoding="utf-8").write(s)
    print(saida, round(len(s) / 1e6, 2), "MB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
