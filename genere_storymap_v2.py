# -*- coding: utf-8 -*-
"""
StoryMap Gen Z, v2 : mêmes diapositives que la v1, mais la page storymap_genz.html (version actuelle) ajoute
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
# (14/11/2026) : l'axe « jeunesse » du Day 12 était bleu et se confondait avec l'océan OSM.
# On garde l'axe chômage rouge du Day 12 et la logique 3×3, mais l'axe jeunesse passe au vert.
BIVAR_DAY12 = {"1-1": "#e8e8e8", "2-1": "#e4acac", "3-1": "#c85a5a",
               "1-2": "#b0d5df", "2-2": "#ad9ea5", "3-2": "#985356",
               "1-3": "#64acbe", "2-3": "#627f8c", "3-3": "#574249"}
BIVAR = {"1-1": "#e8e8e8", "2-1": "#e4acac", "3-1": "#c85a5a",
         "1-2": "#c2dba8", "2-2": "#b9a58e", "3-2": "#985356",
         "1-3": "#7aa95c", "2-3": "#7b7a45", "3-3": "#574249"}
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
    # (14/11/2026) Simplifier en Equal Earth effaçait 26 pays (Allemagne, Russie, Mexique, Chine, Inde…) :
    # on reprojette d'abord en WGS84 (géométries rendues valides), puis on simplifie en degrés.
    d = Path(tempfile.mkdtemp())
    wgs, tmp = d / "pays_wgs84.geojson", d / "pays.geojson"
    cmd = (f'call "{OGR}" && ogr2ogr -f GeoJSON -t_srs EPSG:4326 -makevalid '
           f'-select NAME,ISO_A3,age_median,chom_jeunes,bivar "{wgs}" "{POWER / "genz_power.gpkg"}" pays && '
           f'ogr2ogr -f GeoJSON -simplify 0.12 -lco RFC7946=YES -lco COORDINATE_PRECISION=2 "{tmp}" "{wgs}"')
    bat = d / "export.bat"
    bat.write_text("@echo off\r\n" + cmd.replace(" && ", "\r\n") + "\r\n", encoding="mbcs")
    r = subprocess.run([str(bat)], capture_output=True, text=True, shell=True)
    if not tmp.exists():
        raise SystemExit("ogr2ogr a échoué :\n" + r.stdout + r.stderr)
    geo = json.loads(tmp.read_text(encoding="utf-8"))
    # -makevalid peut produire des GeometryCollection (polygones + bouts de lignes) : on ne garde que les polygones
    for f in geo["features"]:
        g = f.get("geometry")
        if g and g["type"] == "GeometryCollection":
            polys = []
            for m in g["geometries"]:
                if m["type"] == "Polygon":
                    polys.append(m["coordinates"])
                elif m["type"] == "MultiPolygon":
                    polys.extend(m["coordinates"])
            f["geometry"] = {"type": "MultiPolygon", "coordinates": polys} if polys else None
    # Leaflet 0.7 (celui de StoryMapJS) s'arrête sur une géométrie vide : on retire les micro-îles effacées par la simplification
    perdus = [f["properties"].get("NAME") for f in geo["features"] if not (f.get("geometry") and f["geometry"].get("coordinates"))]
    if perdus:
        print("pays sans géométrie après simplification :", perdus)
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

    # paragraphe d'explication (déclencheur, déroulement, issue) en tête du panneau de chaque mouvement
    from explications_v2 import EXPLICATIONS
    manquants = []
    for r in mv + lim:
        ex = EXPLICATIONS.get(r["ville"])
        if not ex:
            manquants.append(r["nom_fr"]); continue
        t = S[slide_de[r["ville"]]]["text"]
        t["text"] = (f'<p class="genz-explication">{v1.esc(ex[0])}</p><p><i>{v1.esc(ex[1])}</i></p>' + t["text"])
    if manquants:
        print("sans explication :", manquants)

    # (14/11) diapositives sans photo libre fiable : carte-titre dans la charte (genere_cartes_titre.py)
    sans_media = []
    for r in mv + lim:
        s = S[slide_de[r["ville"]]]
        if s["media"].get("url"):
            continue
        carte = ICI / "cartes_titre" / (re.sub(r"[^a-z0-9]+", "_", r["ville"].lower().translate(str.maketrans("éèóçà", "eeoca"))).strip("_") + ".png")
        if carte.exists():
            s["media"] = {"url": "cartes_titre/" + carte.name, "credit": "Illustration · Estelle Sérèmes, CC BY-SA 4.0",
                          "caption": f"« {r['slogan']} »" if r["slogan"] else (r["symbole_fr"] or r["nom_fr"])}
        else:
            sans_media.append(r["nom_fr"])
    if sans_media:
        print("toujours sans média :", sans_media)

    # graphiques interactifs (Observable Plot) dans les diapositives Frise et Réussite ; PNG gardés en repli
    def iframe(src, titre, h=470):
        return (f'<iframe src="{src}" title="{titre}" width="100%" height="{h}" frameborder="0" '
                f'style="border:0;background:#efeeea" loading="lazy"></iframe>')
    for n, src, png, titre, h in ((idx["frise"], "frise_interactive.html", v1.OUT_FRISE.name, "Frise interactive 2014–2026", 540),
                                  (idx["reussite"], "reussite_waffle.html", v1.OUT_TAUX.name, "Réussite par époque", 360)):
        S[n]["media"] = {"url": iframe(src, titre, h), "credit": "Observable Plot · CC BY-SA 4.0",
                         "caption": "Survoler pour le détail, cliquer pour ouvrir la diapositive · hover for details, click to open"}
        liens = (f'<p><small><a href="{src}" target="_blank">⤢ Plein écran · full screen</a> · '
                 f'<a href="{png}" target="_blank">version image</a></small></p>')
        if n == idx["frise"]:   # (14/11) le graphique montre tout : plus de longue liste qui obligeait à défiler
            S[n]["text"]["text"] = liens + (
                "<p>Un rond par mouvement, à sa date de début ; couleur = issue, taille = durée. Sous l'axe, les cas limites. "
                "Quatre époques : précurseurs (2014–2018), 1re vague numérique (2019–2023), vague Gen Z (2023–2025) et vague "
                "européenne (2026).</p><p><i>One dot per movement at its start date; colour = outcome, size = duration.</i></p>")
        else:                   # réussite : on garde le texte, sans la liste par époque déjà lisible dans le graphique
            S[n]["text"]["text"] = liens + re.sub(r"<ul>.*?</ul>", "", S[n]["text"]["text"], flags=re.S)
    # sources : crédits photo sur deux colonnes, petite police
    S[idx["sources"]]["text"]["text"] = ('<div class="genz-sources">' +
        S[idx["sources"]]["text"]["text"].replace("<ul>", '<ul class="genz-credits">', 1) + "</div>")
    # contexte : la carte du Day 12 s'ouvre en grand
    S[idx["contexte"]]["text"]["text"] += ('<p class="genz-agrandir">🔍 Cliquer sur la carte pour l\'agrandir et zoomer · '
                                           '<i>click the map to enlarge and zoom</i></p>')

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
            "debut": r["debut"], "fin": r["fin"] or None, "periode": v1.periode(r)[0], "slogan": r["slogan"] or None,
            "picto_txt": r["picto"] or None,
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
            chapitres.append((f"{fr} ({an})", slide_de[prem[0]["ville"]]))   # libellé court : la liste ne coupe plus
    chapitres += [("Symboles qui voyagent", familles_slide["milk_tea"]), ("Cas limites", idx["cas_limites"]),
                  ("Et ça marche ? (réussite)", idx["reussite"]), ("Sources et licences", idx["sources"])]

    data = {"mouvements": mouvements, "pictos": pictos, "familles": familles,
            "chapitres": [{"label": l, "slide": n} for l, n in chapitres],
            "bivar": BIVAR, "coul_issue": COUL, "encre": ENCRE,
            "issues": {k: list(v) for k, v in v1.ISSUE.items()},
            "epoques": [{"code": c, "annees": an, "fr": fr, "en": en} for c, an, fr, en in v1.EPOQUES]}
    v1.sortie(OUT_DATA).write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    n_pays = exporter_pays()
    print(f"{len(slides)} diapositives ; {len(mouvements)} ronds ; {len(pictos)} pictos ; "
          f"{sum(len(f['segments']) for f in familles)} segments ; {n_pays} pays ; "
          f"{OUT_GEO.stat().st_size // 1024} Ko de GeoJSON")
    sans_picto = [m["nom"] for m in mouvements if not m["cas_limite"] and not m["picto"]]
    print("mouvements sans picto :", sans_picto or "-")


if __name__ == "__main__":
    main()
