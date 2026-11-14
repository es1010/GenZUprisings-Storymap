# StoryMap Gen Z · Day 27 « New tool » : guide

Les diapositives viennent de la carte du Day 12 (« Le pouvoir change de mains ? · Power Shift? »).
Le script `genere_storymap.py` les génère (lancer `py -3.12 genere_storymap.py`, ou `--hors-ligne` pour ne pas interroger Wikimedia).

| Fichier | À quoi il sert |
|---|---|
| `storymap_genz_diapositives.csv` | **Pour l'éditeur en ligne** : une ligne par diapositive, à copier-coller champ par champ (UTF-8 avec BOM, séparateur `;`, s'ouvre dans Excel). |
| `storymap_genz_v1.json` + `storymap_genz_v1.html` (v1) | **Version auto-hébergée** (GitHub Pages ou serveur local) : la page charge StoryMapJS depuis le CDN Knight Lab et lit le JSON. Elle marche aussi ouverte en double-clic, grâce à une copie du JSON intégrée à la page. |
| `frise_genz_2014_2026.png`, `taux_reussite_epoques.png`, `carte_power_genz_day12.png` | Images des diapositives Frise, Taux de réussite et Contexte (la carte est une **copie** de `power/export/power_v2.png`). |
| `photos_commons_cache.json` | Photo Commons retenue pour chaque mouvement, avec l'auteur, la licence et la façon dont elle a été trouvée. Pour changer une photo, modifiez ce fichier puis relancez le script avec `--hors-ligne`. |

> **L'éditeur storymap.knightlab.com n'importe aucun fichier** (ni JSON, ni CSV). Il faut copier-coller chaque champ depuis le CSV. Le JSON et le HTML servent uniquement à la version auto-hébergée.

## Correspondance champs de l'éditeur ↔ colonnes du CSV

| Éditeur StoryMapJS | Colonne du CSV |
|---|---|
| Barre de recherche de la carte : *« Search for a location or enter coordinates like lat:… lon:… »* | `recherche_carte` (déjà au format exact `lat:12.3456 lon:-1.2345`) |
| Media : *« URL to your media »* | `media_url` |
| Media : **Credit** | `media_credit` |
| Media : **Caption** | `media_caption` |
| **HEADLINE** | `headline` (le `<i>…</i>` met l'anglais en italique ; en mode texte simple, tapez-le sans balises) |
| Zone de texte | `texte_html` : cliquez sur le bouton **`</>`** (mode HTML) de la barre d'outils, **puis** collez. Sinon les balises s'affichent telles quelles. |
| **Marker Options** | rien à remplir : on garde le marqueur par défaut. Le zoom (colonne `zoom`) se règle à la molette sur la carte de la diapositive : 2 = monde, 4 = région, 6 = ville. |
| **Background Options**, fenêtre « Slide 背景 » (背景 = *background* : bug de traduction de l'interface) → **Color** | `fond_couleur` (ex. `#2b2d42`) |
| Background Options → **Image** | Seulement pour la frise, si vous voulez `frise_genz_2014_2026.png` en fond plutôt qu'en média. |
| **+ Add Slide** | une nouvelle ligne du CSV (colonne `n`) |
| Colonnes `date`, `issue`, `lat`, `lon`, `commons_page` | Aide-mémoire : la date est déjà dans le texte, et `commons_page` donne la page de la photo pour vérifier son auteur. |

La **ligne 0** (`type = overview`) correspond à la **diapositive de titre** de l'éditeur. Celle-ci ne prend pas de lieu : la carte montre tous les marqueurs. Remplissez seulement le titre, le texte, le média et le fond.

## Options générales (icône ≡ / *Options*)

- **Map type** : *OpenStreetMap* (= `osm:standard` dans le JSON).
- **Language** : *Français*.
- Laissez décoché le calcul automatique du zoom, pour garder les zooms ville/région/monde choisis (`calculate_zoom: false`).
- Gardez la ligne entre les marqueurs (*Show lines between markers*).

Ensuite, **Preview** pour vérifier, puis **Publish** / **Share** pour obtenir le lien et le code `<iframe>`.

## Points à savoir

- **Texte blanc** : StoryMapJS écrit le texte en blanc dès qu'une couleur de fond est choisie. C'est pour cela que les fonds sont foncés, dans la teinte de l'issue (ocre = victoire, orange brûlé = concessions, bleu nuit = réprimé, violet = en cours, gris = cas limite).
- **Images locales** (frise, graphique, carte) : l'éditeur en ligne veut une URL publique. Utilisez son bouton d'envoi d'image s'il apparaît, sinon déposez les PNG sur GitHub (dépôt Pages) et collez leur URL `https://…`. Dans la version auto-hébergée, les chemins relatifs suffisent.
- **Photos** : liens directs `https://commons.wikimedia.org/wiki/Special:FilePath/<fichier>?width=1280`. Les photos de la carte du Day 12 (Hong Kong, Lagos, Manille, Berlin) sont reprises telles quelles. Les autres ont été cherchées automatiquement : d'abord l'image principale de l'article Wikipédia, sinon une recherche sur Commons. Elles ont été survolées, mais **une relecture reste utile**. Quatre images hors sujet ont été écartées (`REJETS` dans le script).
- **Sans photo** (11) : Qeerroo (Éthiopie), Ladakh, Tanzanie 2025, Marche Génération Z (Mexique), Blocus lycéens (Belgique), Logement étudiant (Grèce), et les cas limites Paraguay, Maldives, Cameroun, Azad Cachemire et Sénégal 2023. La diapositive s'affiche alors sans média.
- **Licences** : CC BY-SA → crédit (auteur + licence) obligatoire, et réutilisation sous la même licence. La dernière diapositive liste toutes les photos avec leur page Commons.
- **Version auto-hébergée** : déposez le dossier sur GitHub Pages (ou lancez `py -3.12 -m http.server` dans le dossier) et ouvrez `storymap_genz_v1.html` (v1) ou `index.html` (version actuelle, avec l'intro globe).
