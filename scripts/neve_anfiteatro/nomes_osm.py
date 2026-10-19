# -*- coding: utf-8 -*-
"""
Nomes dos cursos d'agua e geleiras ao longo do talvegue (corredor.geojson: talvegue_completo), pelo OpenStreetMap
(API Overpass, so leitura; dados (c) colaboradores do OpenStreetMap, licenca ODbL). Um nome e atribuido aos trechos
do talvegue que ficam a menos de 300 m da geometria do objeto do OSM. Grava nomes_osm_talvegue.json.
Uso: python nomes_osm.py <dir_dados>
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import numpy as np

Q = """[out:json][timeout:60];
(way["waterway"]["name"](28.24,85.36,28.36,85.56); relation["name"="Lhende Khola"];
 way["natural"="glacier"](28.24,85.48,28.30,85.56););
out geom;"""


def pontos(e):
    if e["type"] == "way":
        return [(p["lon"], p["lat"]) for p in e.get("geometry", [])]
    out = []
    for m in e.get("members", []):
        out += [(p["lon"], p["lat"]) for p in (m.get("geometry") or [])]
    return out


def main(d):
    r = urllib.request.Request("https://overpass-api.de/api/interpreter", data=urllib.parse.urlencode({"data": Q}).encode(),
                               headers={"User-Agent": "himalaia-auditoria/1.0"})
    el = json.load(urllib.request.urlopen(r, timeout=90))["elements"]
    tal = [f for f in json.load(open(os.path.join(d, "corredor.geojson")))["features"] if f["properties"]["nome"] == "talvegue_completo"][0]
    xy = np.array(tal["geometry"]["coordinates"]); dist = np.array(tal["properties"]["dist_m"]) / 1000
    res = {}
    for e in el:
        t = e.get("tags", {}); P = np.array(pontos(e))
        if len(P) == 0:
            continue
        D = np.hypot((P[:, None, 0] - xy[None, :, 0]) * 111.32 * np.cos(np.radians(28.3)), (P[:, None, 1] - xy[None, :, 1]) * 111.32)
        k = np.where(D.min(0) < 0.3)[0]
        if len(k) == 0:
            continue
        n = t.get("name:en") or t.get("name") or "(sem nome: %s)" % t.get("natural", "")
        a = res.setdefault(n, {"nome_local": t.get("name"), "tipo": t.get("waterway") or t.get("natural"), "km_ini": 99.0, "km_fim": 0.0, "osm": []})
        a["km_ini"] = round(min(a["km_ini"], float(dist[k].min())), 1); a["km_fim"] = round(max(a["km_fim"], float(dist[k].max())), 1)
        a["osm"].append("%s/%d" % (e["type"], e["id"]))
    out = {"fonte": "OpenStreetMap via Overpass API (ODbL)", "consulta_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
           "criterio": "trechos do talvegue a menos de 300 m da geometria do objeto; km a partir da localizacao USGS us7000tbwb",
           "trechos": dict(sorted(res.items(), key=lambda kv: kv[1]["km_ini"]))}
    json.dump(out, open(os.path.join(d, "nomes_osm_talvegue.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for n, v in out["trechos"].items():
        print("%-28s %-8s km %5.1f a %5.1f  (%s)" % (n, v["tipo"], v["km_ini"], v["km_fim"], v["nome_local"]))


if __name__ == "__main__":
    main(sys.argv[1])
