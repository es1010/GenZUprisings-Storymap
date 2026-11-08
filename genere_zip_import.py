# -*- coding: utf-8 -*-
"""
Fabrique storymap_genz_import.zip, à importer dans storymap.knightlab.com (bouton Import).

Format repris du code source de StoryMapJS (storymap/api.py, fonctions storymap_export et storymap_import) :
  - metadata.json, draft.json et draft.html sont OBLIGATOIRES, sinon le site répond
    « This doesn't look like a StoryMap exported package » ;
  - published.json et index.html sont facultatifs ;
  - les images vont dans _images/. Les media.url de la forme « …/_images/<fichier> » sont réécrites
    par le serveur vers son stockage, à condition que le fichier soit présent dans le zip.
Lit storymap_genz.json et les PNG de ce dossier sans les modifier, et n'écrit que le zip.
"""
import datetime as dt, json, zipfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
SRC = ICI / "storymap_genz.json"
ZIP = ICI / "storymap_genz_import.zip"
IMAGES = ["frise_genz_2014_2026.png", "taux_reussite_epoques.png", "carte_power_genz_day12.png"]
TITRE = "Power Shift Gen Z 2014-2026"

EMBED = """<!DOCTYPE html>
<html lang="fr">
<head>
<title>StoryMapJS: {titre}</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<link rel="stylesheet" href="https://cdn.knightlab.com/libs/storymapjs/latest/css/storymap.css">
<script type="text/javascript" src="https://cdn.knightlab.com/libs/storymapjs/latest/js/storymap-min.js"></script>
<style>html, body {{ width: 100%; height: 100%; padding: 0; margin: 0; }}</style>
</head>
<body>
<div id="storymap-embed"></div>
<script type="text/javascript">
  var storymap;
  fetch("{json}").then(function (r) {{ return r.json(); }}).then(function (data) {{
    storymap = new KLStoryMap.StoryMap("storymap-embed", data, {{}});
    setTimeout(function () {{ storymap.updateDisplay(); }}, 500);
  }});
  window.onresize = function () {{ if (storymap) storymap.updateDisplay(); }};
</script>
</body>
</html>
"""

if ZIP.exists():
    raise SystemExit(f"{ZIP.name} existe déjà : supprimez-le ou renommez-le d'abord (rien n'est écrasé).")

doc = json.loads(SRC.read_text(encoding="utf-8"))
for s in doc["storymap"]["slides"]:
    u = s.get("media", {}).get("url", "")
    if u in IMAGES:
        s["media"]["url"] = "_images/" + u
maintenant = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
meta = {"id": "power-shift-gen-z-2014-2026", "title": TITRE, "draft_on": maintenant, "published_on": "",
        "description": "Révoltes de la génération Z, 2014–2026 · #30DayMapChallenge Day 27"}
texte = json.dumps(doc, ensure_ascii=False)

with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("metadata.json", json.dumps(meta, ensure_ascii=False))
    z.writestr("draft.json", texte)
    z.writestr("published.json", texte)
    z.writestr("draft.html", EMBED.format(titre=TITRE, json="draft.json"))
    z.writestr("index.html", EMBED.format(titre=TITRE, json="published.json"))
    for im in IMAGES:
        z.write(ICI / im, "_images/" + im)

with zipfile.ZipFile(ZIP) as z:
    print(ZIP.name, "->", z.namelist())
    assert {"metadata.json", "draft.json", "draft.html"} <= set(z.namelist())
    d = json.loads(z.read("draft.json"))
    print(len(d["storymap"]["slides"]), "diapositives ;",
          [s["media"]["url"] for s in d["storymap"]["slides"] if s["media"]["url"].startswith("_images/")])
