# Le pouvoir change de mains ? · *Power Shift?*

**Révoltes de la génération Z, 2014–2026 · *Gen Z uprisings, 2014–2026***

StoryMap (StoryMapJS, Knight Lab) du #30DayMapChallenge 2026, jour 27 « New tool ». Elle reprend la carte du jour 12 « Power » : 38 mouvements, 12 cas limites, leurs issues et les symboles qui passent d'un continent à l'autre.

*StoryMap for #30DayMapChallenge 2026, Day 27 "New tool", based on the Day 12 "Power" map: 38 movements, 12 borderline cases, their outcomes and the symbols that travel between continents.*

## Voir la StoryMap · *View it*

Ouvrir <https://es1010.github.io/GenZUprisings-Storymap/> : `index.html` ouvre l'**intro globe**, puis « Entrer » mène à la StoryMap.

- **StoryMap** `storymap_genz.html` (version actuelle) : aplats bivariés âge médian × chômage des 15–24 ans, ronds de la carte du Day 12 (issue, durée, époque, picto) sans chevauchement, lignes fléchées des symboles qui voyagent, frise et waffle interactifs, visionneuse d'images, barre de navigation (chapitres, recherche). `storymap_genz.html?diapo=N` ouvre directement la diapositive N. *Current version.*
- **Intro globe** `globe_intro.html` : globe qui tourne vers chaque mouvement, l'un après l'autre, avec une onde à son apparition ; « Passer l'intro » mène directement à la StoryMap. *Spinning-globe intro.*
- **v1** `storymap_genz_v1.html` : version StoryMapJS d'origine (marqueurs et lignes standard), identique à l'éditeur en ligne. *Original plain StoryMapJS version.*
- `storymap_genz_v2.html` : ancienne adresse de la version actuelle, simple redirection (peut être supprimée).

## Contenu du dépôt · *Contents*

| Fichier | Rôle |
|---|---|
| `index.html` | Accueil : redirige vers l'intro globe · *home* |
| `storymap_genz.html`, `storymap_genz_v2.json`, `genz_v2_donnees.json`, `pays_bivarie.geojson` | Version actuelle : page, diapositives, ronds/lignes/chapitres, aplats des pays · *current page and data* |
| `frise_interactive.html`, `reussite_waffle.html` | Frise et waffle de réussite interactifs (Observable Plot), affichés dans les diapositives · *interactive charts* |
| `globe_intro.html` | Intro globe (D3) · *globe intro* |
| `storymap_genz_v1.html`, `storymap_genz_v1.json` | v1 : page StoryMapJS autonome et ses 60 diapositives · *v1 page and slides* |
| `storymap_genz_diapositives.csv` | Les diapositives v1 en tableau · *slides as a table* |
| `frise_genz_2014_2026.png`, `taux_reussite_epoques.png`, `carte_power_genz_day12.png` | Frise, graphique, carte (v1, et « version image » de la version actuelle) · *timeline, chart, map* |
| `storymap_genz_import.zip` | Paquet à importer dans storymap.knightlab.com (v1) · *import package* |
| `genere_storymap.py`, `genere_storymap_v2.py`, `explications_v2.py`, `genere_zip_import.py` | Scripts et textes qui génèrent tout cela · *generator scripts* |
| `GUIDE_storymap_genz.md` | Guide pour l'éditeur en ligne · *online editor guide* |

## Licences · *Licences*

- **Contenus** (carte, frise, graphique, textes, données JSON/CSV) : [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr), Estelle Sérèmes. *Content: CC BY-SA 4.0.*
- **Code** (`*.py`, `storymap_genz.html`, `storymap_genz_v1.html`, `frise_interactive.html`, `reussite_waffle.html`, `globe_intro.html`) : licence MIT, voir [`LICENSE`](LICENSE). *Code: MIT.*
- **Photos** : Wikimedia Commons, chargées depuis Commons et non incluses dans le dépôt. Chaque photo garde sa propre licence (CC BY, CC BY-SA, CC0…), avec son auteur crédité sur la diapositive et dans la diapositive « Sources et licences ». *Photos keep their own Commons licences.*
- **Limites des pays (v2)** : couche « pays » du Day 12 (Natural Earth, domaine public), simplifiée.
- **Fond de carte** : © contributeurs [OpenStreetMap](https://www.openstreetmap.org/copyright) (ODbL). *Basemap © OpenStreetMap contributors.*
- **StoryMapJS** : © Knight Lab, Northwestern University, licence MPL 2.0, chargé depuis le CDN Knight Lab.
- **D3** (ISC) et **Observable Plot** (ISC), chargés depuis jsDelivr. **Globe** d'après [Curran Kelleher](https://vizhub.com/curran/cv-zoomable-globe-with-cities) (MIT), réécrit en D3 sans React.
- **Palette bivariée (v2)** : axe chômage repris du Day 12 ; axe « population jeune » passé du bleu au vert pour ne pas se confondre avec l'océan.

## Sources

Wikipédia, presse internationale, ONG (HRW, Amnesty, FIDH) ; âge médian : ONU World Population Prospects 2024 (via Our World in Data) ; chômage des 15–24 ans : OIT via Banque mondiale (2025), Taïwan DGBAS, Kosovo KAS.

#30DayMapChallenge · Next Generation Cartographers
