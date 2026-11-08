# Le pouvoir change de mains ? · *Power Shift?*

**Révoltes de la génération Z, 2014–2026 · *Gen Z uprisings, 2014–2026***

StoryMap (StoryMapJS, Knight Lab) du #30DayMapChallenge 2026, jour 27 « New tool ». Elle reprend la carte du jour 12 « Power » : 38 mouvements, 12 cas limites, leurs issues et les symboles qui passent d'un continent à l'autre.

*StoryMap for #30DayMapChallenge 2026, Day 27 "New tool", based on the Day 12 "Power" map: 38 movements, 12 borderline cases, their outcomes and the symbols that travel between continents.*

## Voir la StoryMap · *View it*

Ouvrir `https://<utilisateur>.github.io/<depot>/` : `index.html` redirige vers la **v2**.

- **v2** `storymap_genz_v2.html` : aplats bivariés âge médian × chômage des 15–24 ans, ronds de la carte du Day 12 (issue, durée, époque, picto), lignes des symboles qui voyagent, barre de navigation (chapitres, recherche). *Bivariate choropleth, Day 12 symbols, travelling-symbol lines, navigation bar.*
- **v1** `storymap_genz.html` : version StoryMapJS d'origine (marqueurs et lignes standard), identique à l'éditeur en ligne. *Original plain StoryMapJS version.*

## Contenu du dépôt · *Contents*

| Fichier | Rôle |
|---|---|
| `storymap_genz.html` | v1 : page StoryMapJS autonome · *standalone page* |
| `storymap_genz_v2.html`, `storymap_genz_v2.json`, `genz_v2_donnees.json`, `pays_bivarie.geojson` | v2 : page, diapositives, ronds/lignes/chapitres, aplats des pays · *v2 page and data* |
| `storymap_genz.json` | Les 60 diapositives (format StoryMapJS) · *the 60 slides* |
| `storymap_genz_diapositives.csv` | Les mêmes diapositives en tableau · *same slides as a table* |
| `frise_genz_2014_2026.png`, `taux_reussite_epoques.png`, `carte_power_genz_day12.png` | Frise, graphique, carte · *timeline, chart, map* |
| `storymap_genz_import.zip` | Paquet à importer dans storymap.knightlab.com · *import package* |
| `genere_storymap.py`, `genere_storymap_v2.py`, `genere_zip_import.py` | Scripts qui génèrent tout cela · *generator scripts* |
| `GUIDE_storymap_genz.md` | Guide pour l'éditeur en ligne · *online editor guide* |

## Licences · *Licences*

- **Contenus** (carte, frise, graphique, textes, données JSON/CSV) : [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr), Estelle Sérèmes. *Content: CC BY-SA 4.0.*
- **Code** (`*.py`, `storymap_genz.html`, `storymap_genz_v2.html`) : licence MIT, voir [`LICENSE`](LICENSE). *Code: MIT.*
- **Photos** : Wikimedia Commons, chargées depuis Commons et non incluses dans le dépôt. Chaque photo garde sa propre licence (CC BY, CC BY-SA, CC0…), avec son auteur crédité sur la diapositive et dans la diapositive « Sources et licences ». *Photos keep their own Commons licences.*
- **Limites des pays (v2)** : couche « pays » du Day 12 (Natural Earth, domaine public), simplifiée.
- **Fond de carte** : © contributeurs [OpenStreetMap](https://www.openstreetmap.org/copyright) (ODbL). *Basemap © OpenStreetMap contributors.*
- **StoryMapJS** : © Knight Lab, Northwestern University, licence MPL 2.0, chargé depuis le CDN Knight Lab.

## Sources

Wikipédia, presse internationale, ONG (HRW, Amnesty, FIDH) ; âge médian : ONU World Population Prospects 2024 (via Our World in Data) ; chômage des 15–24 ans : OIT via Banque mondiale (2025), Taïwan DGBAS, Kosovo KAS.

#30DayMapChallenge · Next Generation Cartographers
