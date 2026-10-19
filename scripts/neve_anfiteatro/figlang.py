# -*- coding: utf-8 -*-
"""
Figuras em ingles para o artigo, sem duplicar os scripts: com FIG_LANG=en, prepara(fig) troca os textos
(dicionario abaixo) e apaga os titulos descritivos (no artigo eles vao nas legendas); caminho(p) manda a
saida para FIG_DIR, se definido. Sem FIG_LANG, nada muda.
"""
import os

EN = [
    ("Landsat/HLS com SWIR < 0 em > 10 % dos pixels (rejeitado)", "Landsat/HLS with SWIR < 0 in > 10% of pixels (rejected)"),
    ("fração de neve/gelo nos pixels\nobservados do anfiteatro (NDSI > 0,42)", "snow/ice fraction of observed\namphitheatre pixels (NDSI > 0.42)"),
    ("Sentinel-2 L1C (topo da atmosfera)", "Sentinel-2 L1C (top of atmosphere)"),
    ("ΔVV médio das 3 geometrias (dB), pares de 12 dias com o colapso", "mean ΔVV of the three geometries (dB)"),
    ("neve/gelo (NDSI>0,42)\nsó SCL: azul escuro = neve, claro = sem neve, cinza = nuvem", "SCL mask only: dark blue = snow/ice,\nlight blue = no snow, grey = cloud"),
    ("% da faixa (±250 m) com\nΔVV > +3 dB", "% of ±250 m swath with\nΔVV > +3 dB"),
    ("distância ao longo do talvegue a partir do ponto de colapso (km)", "distance along thalweg from the USGS seismic location (km)"),
    ("linha de neve (m)\n(fração de neve = 50 %)", "snowline (m)\n(snow fraction = 50%)"),
    ("S1: ΔVV médio (3 geometrias)", "S1: mean ΔVV (3 geometries)"),
    (" colapso 26/08 02:52", " collapse 26 Aug 02:52"),
    (" exutório 4.010 m", " outlet 4,010 m"),
    ("ponto de colapso", "USGS seismic location"),
    ("falsa cor B11-B8A-B04", "false colour B11-B8A-B04"),
    (" cor verdadeira", " true colour"),
    ("(evento)", "(event)"),
    ("cota (m)", "elevation (m)"),
    (", máscara espectral", ", spectral mask"),
    (", máscara estrita", ", SCL-only mask"),
    (": sem cena", ": no scene"),
    (" colapso", " collapse"),
]


def ativo():
    return os.environ.get("FIG_LANG") == "en"


def prepara(fig):
    if not ativo():
        return
    from matplotlib.text import Text
    if getattr(fig, "_suptitle", None) is not None:
        fig._suptitle.set_text("")
    for ax in fig.axes:
        t = ax.get_title()
        if len(t) > 32:
            ax.set_title("")
    for t in fig.findobj(Text):
        s = t.get_text()
        for a, b in EN:
            if a in s:
                s = s.replace(a, b)
        if s != t.get_text():
            t.set_text(s)
    for ax in fig.axes:
        lg = ax.get_legend()
        if lg:
            for t in lg.get_texts():
                s = t.get_text()
                for a, b in EN:
                    s = s.replace(a, b)
                t.set_text(s)


def caminho(p):
    d = os.environ.get("FIG_DIR")
    return os.path.join(d, os.path.basename(p)) if (d and ativo()) else p
