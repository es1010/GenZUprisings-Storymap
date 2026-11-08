# -*- coding: utf-8 -*-
"""
StoryMap Gen Z, v2 : mêmes diapositives que la v1, mais la page storymap_genz_v2.html ajoute
  - les aplats bivariés âge médian × chômage des 15–24 ans (palette 3×3 du Day 12) sous les marqueurs ;
  - les ronds de la carte du Day 12 (couleur = issue, taille = durée, anneau = époque, picto)
    à la place des marqueurs rouges de StoryMapJS ;
  - des lignes seulement sur les 4 diapositives « symbole qui voyage », une couleur par symbole ;
  - une barre de navigation (vue d'ensemble, chapitres, recherche de mouvement).

Lit (lecture seule) : ../power/mouvements_genz.csv, ../power/genz_power.gpkg, ../power/pictos/*.svg,
photos_commons_cache.json (v1). Écrit uniquement dans « new tool » :
  storymap_genz_v2.json, genz_v2_donnees.json, pays_bivarie.geojson.
Lancer :  py -3.12 genere_storymap_v2.py
"""
import json, re, sqlite3, subprocess, tempfile
from pathlib import Path

import genere_storymap as v1   # fonctions de la v1 (lecture CSV/gpkg, diapositives)

ICI = v1.ICI
POWER = v1.POWER
OUT_JSON = ICI / "storymap_genz_v2.json"
OUT_DATA = ICI / "genz_v2_donnees.json"
OUT_GEO = ICI / "pays_bivarie.geojson"
OGR = r"C:\OSGeo4W\bin\o4w_env.bat"

# Style de la couche « Mouvements Gen Z – monde » (power.qgz)
COUL = v1.COUL
ENCRE = "#2b2d42"
ANNEAU = {"precurseurs": ("dot", 0.5), "vague1": ("dash", 0.42), "vague2": ("solid", 0.6), "2026": ("double", 0.32)}
# Palette de la couche « Pays (bivarié) » : clé = classe chômage - classe jeunesse
BIVAR = {"1-1": "#e8e8e8", "2-1": "#e4acac", "3-1": "#c85a5a",
         "1-2": "#b0d5df", "2-2": "#ad9ea5", "3-2": "#985356",
         "1-3": "#64acbe", "2-3": "#627f8c", "3-3": "#574249"}
# Couleurs de la couche « Diffusion – monde »
COUL_FAMILLE = {"milk_tea": "#8d6e63", "one_piece": "#d62828", "discord": "#5865f2", "lyceens": "#0b6e4f"}


def diametre_mm(duree, cas_limite):
    """scale_exp("duree_j", 1, 1400, 3, 10, 0.5) comme dans le style QGIS."""
    if cas_limite:
        return 2.2
    t = max(0.0, min(1.0, (duree - 1) / 1399))
    return 3 + 7 * t ** 0.5


def picto_svg(chemin):
    """Contenu intérieur du SVG du picto (fill QGIS « param(fill) » remplacé par currentColor)."""
    s = Path(chemin).read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', s)
    corps = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", s, flags=re.S)
    corps = re.sub(r'fill="param\(fill\)[^"]*"', 'fill="currentColor"', corps)
    corps = re.sub(r'stroke="param\(outline\)[^"]*"', 'stroke="currentColor"', corps)
    corps = re.sub(r'(stroke-width|fill-opacity|stroke-opacity)="param\([^)]*\)\s*([^"]*)"', r'\1="\2"', corps)
    return {"viewBox": vb.group(1) if vb else "0 0 100 100", "corps": corps}


def exporter_pays():
    """Couche pays du gpkg -> GeoJSON WGS84 simplifié (via ogr2ogr d'OSGeo4W)."""
    tmp = Path(tempfile.mkdtemp()) / "pays.geojson"
    cmd = (f'call "{OGR}" && ogr2ogr -f GeoJSON -t_srs EPSG:4326 -simplify 20000 -lco RFC7946=YES '
           f'-lco COORDINATE_PRECISION=2 -select NAME,ISO_A3,age_median,chom_jeunes,bivar '
           f'"{tmp}" "{POWER / "genz_power.gpkg"}" pays')
    bat = tmp.with_suffix(".bat")
    bat.write_text("@echo off\r\n" + cmd.replace(" && ", "\r\n") + "\r\n", encoding="mbcs")
    r = subprocess.run([str(bat)], capture_output=True, text=True, shell=True)
    if not tmp.exists():
        raise SystemExit("ogr2ogr a échoué :\n" + r.stdout + r.stderr)
    geo = json.loads(tmp.read_text(encoding="utf-8"))
    # Leaflet 0.7 (celui de StoryMapJS) s'arrête sur une géométrie vide : on retire les micro-pays effacés par la simplification
    geo["features"] = [f for f in geo["features"] if f.get("geometry") and f["geometry"].get("coordinates")]
    for f in geo["features"]:
        p = f["properties"]
        p["age_median"] = round(p["age_median"], 1) if p.get("age_median") is not None else None
        p["chom_jeunes"] = round(p["chom_jeunes"], 1) if p.get("chom_jeunes") is not None else None
    v1.sortie(OUT_GEO).write_text(json.dumps(geo, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(geo["features"])


def main():
    rows = v1.lire_csv()
    pays, diff = v1.lire_gpkg()
    ph = json.loads((ICI / "photos_commons_cache.json").read_text(encoding="utf-8"))  # cache de la v1, non réécrit
    S, mv, lim = v1.construire(rows, pays, diff, ph)

    # pictos et durées depuis la couche « mouvements » du gpkg
    c = sqlite3.connect(f"file:{(POWER / 'genz_power.gpkg').as_posix()}?mode=ro", uri=True)
    gp = {v: (svg, d) for v, svg, d in c.execute("select ville, picto_svg, duree_j from mouvements")}
    c.close()

    # repérer les diapositives (même ordre que la v1)
    idx = {"intro": 0, "contexte": 1, "frise": 2}
    i = 3
    slide_de = {}
    for r in mv:
        slide_de[r["ville"]] = i; i += 1
    familles_slide = {}
    for code in v1.FAMILLES:
        familles_slide[code] = i; i += 1
    idx["cas_limites"] = i; i += 1
    for r in lim:
        slide_de[r["ville"]] = i; i += 1
    idx["reussite"], idx["sources"] = i, i + 1
    assert i + 2 == len(S), (i, len(S))
    for r in mv + lim:   # contrôle : le titre de la diapositive contient le nom du mouvement
        assert v1.esc(r["nom_fr"]) in S[slide_de[r["ville"]]]["text"]["headline"], r["nom_fr"]

    # diapositives « symbole qui voyage » : cadrer tout le réseau plutôt que le seul foyer d'origine
    villes_rows = {r["ville"]: r for r in rows}
    for code, n in familles_slide.items():
        vs = [villes_rows[v] for t, a, b in diff if t == code for v in (a, b) if v in villes_rows]
        la = [r["lat"] for r in vs]; lo = [r["lon"] for r in vs]
        etendue = max(max(lo) - min(lo), 1.5 * (max(la) - min(la)))
        S[n]["location"].update(lat=round((max(la) + min(la)) / 2, 4), lon=round((max(lo) + min(lo)) / 2, 4),
                                zoom=2 if etendue > 80 else 3 if etendue > 30 else 4)

    # pas de ligne StoryMapJS entre les points
    for s in S:
        s["location"]["line"] = False
    slides = [{k: v for k, v in s.items() if not k.startswith("_")} for s in S]
    doc = {"storymap": {"language": "fr", "map_type": "osm:standard", "calculate_zoom": False, "slides": slides}}
    v1.sortie(OUT_JSON).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    pictos, mouvements = {}, []
    for r in mv + lim:
        svg, duree = gp.get(r["ville"], (None, None))
        duree = duree or v1.duree_jours(r)
        cle = Path(svg).stem if svg else None
        if svg and cle not in pictos and Path(svg).exists():
            pictos[cle] = picto_svg(svg)
        style, ep = ANNEAU.get(r["epoque"], ("solid", 0.5))
        mouvements.append({
            "slide": slide_de[r["ville"]], "nom": r["nom_fr"], "nom_en": r["nom_en"], "pays": r["pays_fr"],
            "ville": r["ville"], "annee": r["debut"][:4], "lat": r["lat"], "lon": r["lon"],
            "resultat": r["resultat"], "issue": v1.ISSUE[r["resultat"]][0], "epoque": r["epoque"],
            "cas_limite": r["cas_limite"], "duree": duree,
            "d_mm": round(diametre_mm(duree, r["cas_limite"]), 2),
            "remplissage": COUL["cas_limite"] if r["cas_limite"] else COUL[r["resultat"]],
            "anneau": None if r["cas_limite"] else style, "anneau_mm": ep,
            "picto": None if r["cas_limite"] else cle,
            "picto_couleur": "#ffffff" if r["resultat"] in ("repression", "en_cours") else "#1b1b1b",
        })

    par_ville = {r["ville"]: r for r in rows}
    familles = []
    for code, f in v1.FAMILLES.items():
        seg = [[[par_ville[a]["lat"], par_ville[a]["lon"]], [par_ville[b]["lat"], par_ville[b]["lon"]]]
               for t, a, b in diff if t == code and a in par_ville and b in par_ville]
        villes = sorted({v for t, a, b in diff if t == code for v in (a, b)})
        familles.append({"code": code, "fr": f["fr"], "en": f["en"], "couleur": COUL_FAMILLE[code],
                         "slide": familles_slide[code], "segments": seg,
                         "slides_mouvements": [slide_de[v] for v in villes if v in slide_de]})

    chapitres = [("Introduction", idx["intro"]), ("Contexte : âge × chômage", idx["contexte"]),
                 ("Frise 2014–2026", idx["frise"])]
    for code, an, fr, en in v1.EPOQUES:
        prem = [r for r in mv if r["epoque"] == code]
        if prem:
            chapitres.append((f"Mouvements · {fr} ({an})", slide_de[prem[0]["ville"]]))
    chapitres += [("Symboles qui voyagent", familles_slide["milk_tea"]), ("Cas limites", idx["cas_limites"]),
                  ("Et ça marche ? (réussite)", idx["reussite"]), ("Sources et licences", idx["sources"])]

    data = {"mouvements": mouvements, "pictos": pictos, "familles": familles,
            "chapitres": [{"label": l, "slide": n} for l, n in chapitres],
            "bivar": BIVAR, "coul_issue": COUL, "encre": ENCRE,
            "issues": {k: list(v) for k, v in v1.ISSUE.items()}}
    v1.sortie(OUT_DATA).write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    n_pays = exporter_pays()
    print(f"{len(slides)} diapositives ; {len(mouvements)} ronds ; {len(pictos)} pictos ; "
          f"{sum(len(f['segments']) for f in familles)} segments ; {n_pays} pays ; "
          f"{OUT_GEO.stat().st_size // 1024} Ko de GeoJSON")
    sans_picto = [m["nom"] for m in mouvements if not m["cas_limite"] and not m["picto"]]
    print("mouvements sans picto :", sans_picto or "-")


if __name__ == "__main__":
    main()
