# -*- coding: utf-8 -*-
"""
Day 27 « New tool » : StoryMapJS (Knight Lab) à partir de la carte Gen Z du Day 12 (« Power »).

Lit (lecture seule) : ../power/mouvements_genz.csv, ../power/genz_power.gpkg (âge médian × chômage,
familles de symboles), ../power/photos/credits_commons.json, ../power/export/power_v2.png.
Écrit UNIQUEMENT dans ce dossier « new tool » :
  storymap_genz.json, storymap_genz_diapositives.csv, storymap_genz.html,
  frise_genz_2014_2026.png, taux_reussite_epoques.png, carte_power_genz_day12.png,
  photos_commons_cache.json (cache des recherches Wikimedia, à relire/corriger à la main).

Lancer avec un Python qui a matplotlib, ex. :  py -3.12 genere_storymap.py
Option --hors-ligne : n'interroge pas Wikimedia, utilise seulement le cache.
"""
import csv, datetime as dt, html, json, re, shutil, sqlite3, sys, urllib.parse, urllib.request
from pathlib import Path

ICI = Path(__file__).resolve().parent
POWER = ICI.parent / "power"
CSV_SRC = POWER / "mouvements_genz.csv"
GPKG = POWER / "genz_power.gpkg"
CREDITS_LOCAUX = POWER / "photos" / "credits_commons.json"
CARTE_SRC = POWER / "export" / "power_v2.png"

CACHE = ICI / "photos_commons_cache.json"
OUT_JSON = ICI / "storymap_genz.json"
OUT_CSV = ICI / "storymap_genz_diapositives.csv"
OUT_HTML = ICI / "storymap_genz.html"
OUT_FRISE = ICI / "frise_genz_2014_2026.png"
OUT_TAUX = ICI / "taux_reussite_epoques.png"
OUT_CARTE = ICI / "carte_power_genz_day12.png"


def sortie(p):
    """Garde-fou : on n'écrit jamais hors du dossier « new tool »."""
    p = Path(p).resolve()
    if p.parent != ICI:
        raise SystemExit(f"Refus d'écrire hors de « new tool » : {p}")
    return p


# --------------------------------------------------------------------------- constantes
COUL = {"victoire": "#ffd23f", "concession": "#f28c28", "repression": "#2b2d42",
        "en_cours": "#9d4edd", "cas_limite": "#bdbdbd"}
# StoryMapJS écrit le texte en BLANC dès qu'une couleur de fond est donnée : fonds foncés, teinte de l'issue
FOND = {"victoire": "#6e5600", "concession": "#8a4512", "repression": "#2b2d42",
        "en_cours": "#55287f", "cas_limite": "#5a5a5a", "neutre": "#33364d",
        "contexte": "#2f5361", "symbole": "#1f4f5c"}
PAPIER = "#efeeea"   # fond des graphiques matplotlib
ISSUE = {"victoire": ("victoire", "won"), "concession": ("concessions obtenues", "concessions won"),
         "repression": ("réprimé", "crushed"), "en_cours": ("en cours", "ongoing")}
EPOQUES = [("precurseurs", "2014–2018", "Précurseurs", "Forerunners"),
           ("vague1", "2019–2023", "1re vague numérique", "First digital wave"),
           ("vague2", "2023–2025", "Vague Gen Z", "Gen Z wave"),
           ("2026", "2026", "Vague européenne", "European wave")]
EPO = {c: (a, f, e) for c, a, f, e in EPOQUES}
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Familles de symboles qui voyagent (table « diffusion » du gpkg) : foyer d'origine = ville source
FAMILLES = {
    "milk_tea": dict(fr="Milk Tea Alliance", en="Milk Tea Alliance", foyer="Hong Kong 2019", zoom=4,
                     txt_fr="Née en 2020 d'une querelle en ligne avec des internautes nationalistes chinois, l'« alliance du thé au lait » "
                            "relie Hong Kong, Taïwan, la Thaïlande et le Myanmar : mêmes mèmes, salut à trois doigts, entraide numérique.",
                     txt_en="Born from a 2020 online spat, the Milk Tea Alliance links Hong Kong, Taiwan, Thailand and Myanmar."),
    "one_piece": dict(fr="Drapeau One Piece", en="One Piece flag", foyer="Jakarta", zoom=4,
                      txt_fr="Le Jolly Roger au chapeau de paille du manga <i>One Piece</i> part d'Indonésie (août 2025), "
                             "flotte à Katmandou, puis se coiffe d'un satroka à Madagascar, d'un chullo à Lima, d'un sombrero à Mexico…",
                      txt_en="The straw-hat Jolly Roger from the manga <i>One Piece</i> spread from Indonesia (Aug. 2025) to Nepal, "
                             "Madagascar, Peru, Mexico, Bulgaria and France."),
    "discord": dict(fr="Organisation sur Discord", en="Organised on Discord", foyer="Katmandou", zoom=4,
                    txt_fr="Au Népal, une Première ministre intérimaire est choisie par un vote sur un serveur Discord (sept. 2025). "
                           "Le modèle est repris par GenZ 212 au Maroc et à Madagascar.",
                    txt_en="In Nepal an interim PM was picked through a Discord poll (Sept. 2025); Morocco's GenZ 212 and Madagascar followed."),
    "lyceens": dict(fr="Contagion lycéenne", en="High-school contagion", foyer="Créteil", zoom=4,
                    txt_fr="À l'automne 2026, les blocus des lycées français essaiment : Bruxelles, Rome, Berlin, Athènes, Tirana.",
                    txt_en="In autumn 2026, French high-school blockades spread to Brussels, Rome, Berlin, Athens and Tirana."),
}

# correspondance pays_en du CSV -> NAME de la couche « pays » quand ils diffèrent
PAYS_ALIAS = {"Sweden (global)": "Sweden", "USA (campuses)": "United States of America",
              "Pakistan (Azad Kashmir)": "Pakistan", "Timor-Leste": "Timor-Leste"}

UA = {"User-Agent": "storymap-genz-day27/1.0 (personal cartography project; python urllib)"}
EN_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
MOTS_VIDES = {"protests", "protest", "movement", "the", "and", "student", "students", "riots", "march",
              "revolution", "against", "general", "strike", "strikes"}


# --------------------------------------------------------------------------- utilitaires
def esc(s):
    return html.escape(s or "", quote=False)


def date_fr(d):
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"


def date_en(d):
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def periode(r):
    d = dt.date.fromisoformat(r["debut"])
    if not r["fin"]:
        return f"depuis le {date_fr(d)}", f"since {date_en(d)}"
    f = dt.date.fromisoformat(r["fin"])
    return f"{date_fr(d)} – {date_fr(f)}", f"{date_en(d)} – {date_en(f)}"


def duree_jours(r, ref=dt.date(2026, 11, 8)):
    d = dt.date.fromisoformat(r["debut"])
    f = dt.date.fromisoformat(r["fin"]) if r["fin"] else ref
    return (f - d).days + 1


def bi(fr, en):
    """FR puis EN en italique."""
    return f"{fr} · <i>{en}</i>" if en and en != fr else fr


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def jetons(s):
    return {w for w in re.findall(r"[a-zà-ÿ]{4,}", (s or "").lower()) if w not in MOTS_VIDES}


def api(base, **p):
    """Requête API Wikimedia polie : 1 requête/seconde, nouvel essai si 429 (trop de requêtes)."""
    import time, urllib.error
    p.update(format="json", formatversion=2, maxlag=5)
    req = urllib.request.Request(base + "?" + urllib.parse.urlencode(p), headers=UA)
    for essai in range(5):
        time.sleep(1.0 + 4 * essai ** 2)
        try:
            with urllib.request.urlopen(req, timeout=40) as rep:
                return json.load(rep)
        except urllib.error.HTTPError as e:
            if e.code != 429 or essai == 4:
                raise


# Photos trouvées automatiquement mais hors sujet (vérifiées à la main le 2026-11-08)
REJETS = {"Chris_Meloni.jpg",                                   # un acteur, pas le No Meloni Day
          "Road_Padum_Zanskar_Range_Jun24_A7CR_00818.jpg",      # paysage du Zanskar, pas la manifestation
          "THE_PERAPLE_OF_WOLKAIT.jpg",                         # manifestation du Wolkait, pas les Oromo
          "Oromo_Cultural_dressing.jpg"}                        # costume traditionnel, pas une manifestation


def photo_ok(nom):
    """Écarte schémas, cartes, logos, drapeaux, portraits officiels : on veut une photo de rue."""
    if nom in REJETS:
        return False
    n = nom.lower()
    return (re.search(r"\.(jpe?g|png|webp|tiff?)$", n) is not None
            and not re.search(r"map|logo|flag|chart|graph|diagram|seal|emblem|coat_of_arms|official|portrait|svg", n))


def nom_fichier(valeur):
    """Extrait un nom de fichier Commons d'une URL de page File: ou d'un 'File:xxx'. None sinon."""
    v = (valeur or "").strip()
    m = re.search(r"(?:File|Fichier):([^?#]+)$", urllib.parse.unquote(v))
    if m:
        return m.group(1).replace(" ", "_")
    if re.search(r"\.(jpe?g|png|gif|svg|tiff?|webp)$", v, re.I) and "/" not in v:
        return v.replace(" ", "_")
    return None


def filepath_url(nom):
    return ("https://commons.wikimedia.org/wiki/Special:FilePath/"
            + urllib.parse.quote(nom.replace(" ", "_"), safe="()_,.-'!") + "?width=1280")


def page_url(nom):
    return "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(nom.replace(" ", "_"), safe="()_,.-'!")


def infos_commons(nom):
    """Métadonnées d'un fichier hébergé sur Commons (None s'il n'y est pas, ex. image non libre locale à en.wiki)."""
    d = api(COMMONS_API, action="query", titles="File:" + nom, prop="imageinfo", iiprop="extmetadata|mime")
    pg = d["query"]["pages"][0]
    if pg.get("missing") or "imageinfo" not in pg:
        return None
    meta = pg["imageinfo"][0].get("extmetadata", {})
    g = lambda k: strip_tags(meta.get(k, {}).get("value", ""))
    return dict(fichier=pg["title"].split(":", 1)[1].replace(" ", "_"), auteur=g("Artist")[:120],
                licence=g("LicenseShortName"), page=page_url(pg["title"].split(":", 1)[1]))


def chercher_photo(terme):
    """1) image principale de l'article Wikipédia (en) correspondant ; 2) recherche dans l'espace File: de Commons."""
    tj = jetons(terme)
    try:
        d = api(EN_API, action="query", generator="search", gsrsearch=terme, gsrlimit=3,
                prop="pageimages", piprop="name")
        for p in sorted(d.get("query", {}).get("pages", []), key=lambda p: p.get("index", 9)):
            if p.get("pageimage") and photo_ok(p["pageimage"]) and tj & jetons(p["title"]):
                inf = infos_commons(p["pageimage"])
                if inf:
                    inf["methode"] = f"image principale de l'article en.wikipedia « {p['title']} »"
                    return inf
        d = api(COMMONS_API, action="query", list="search", srsearch=terme + " filetype:bitmap",
                srnamespace=6, srlimit=5)
        for h in d.get("query", {}).get("search", []):
            nom = h["title"].split(":", 1)[1]
            if photo_ok(nom) and tj & jetons(nom):
                inf = infos_commons(nom)
                if inf:
                    inf["methode"] = "recherche Commons (1er résultat pertinent)"
                    return inf
    except Exception as e:  # réseau indisponible, etc.
        return dict(erreur=str(e))
    return None


# --------------------------------------------------------------------------- données
def lire_csv():
    with open(CSV_SRC, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))
    for r in rows:
        r["lat"], r["lon"] = float(r["lat"]), float(r["lon"])
        r["cas_limite"] = r["cas_limite"].strip() == "1"
    return rows


def lire_gpkg():
    c = sqlite3.connect(f"file:{GPKG.as_posix()}?mode=ro", uri=True)
    pays = {n: (a, ch, b) for n, a, ch, b in c.execute("select NAME, age_median, chom_jeunes, bivar from pays")}
    diff = list(c.execute("select type, de, vers from diffusion"))
    c.close()
    return pays, diff


def photos(rows, hors_ligne):
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    # photos déjà retenues pour la carte du Day 12 (crédits vérifiés) : prioritaires
    locaux = json.loads(CREDITS_LOCAUX.read_text(encoding="utf-8")) if CREDITS_LOCAUX.exists() else {}
    par_ville = {"Hong Kong": "hongkong", "Lagos": "nigeria", "Berlin": "berlin", "Manille": "manille"}
    for r in rows:
        cle = r["nom_en"]
        ok = cache.get(cle) and "erreur" not in cache[cle]
        if ok and (cache[cle].get("methode", "").startswith(("photo de la carte", "nom de fichier", "manuel"))
                   or photo_ok(cache[cle].get("fichier", ""))):
            continue
        if cle in cache and cache[cle] is None and hors_ligne:
            continue
        loc = locaux.get(par_ville.get(r["ville"], ""), None)
        nf = nom_fichier(r["commons"]) or (nom_fichier(loc["page"]) if loc else None)
        if loc:
            aut = loc["auteur"] if loc["auteur"] not in ("[1]", "") else "auteur sur la page Commons"
            cache[cle] = dict(fichier=nf, auteur=aut, licence=loc["licence"], page=loc["page"],
                              methode="photo de la carte Day 12 (power/photos/credits_commons.json)")
        elif nf:
            cache[cle] = (infos_commons(nf) if not hors_ligne else None) or dict(
                fichier=nf, auteur="", licence="", page=page_url(nf), methode="nom de fichier de la colonne commons")
        elif not hors_ligne:
            cache[cle] = chercher_photo(r["commons"] or r["nom_en"])
            print(f"  photo {r['nom_en'][:40]:40s} -> {(cache[cle] or {}).get('fichier', 'AUCUNE')}")
    CACHE_OUT = sortie(CACHE)
    CACHE_OUT.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return cache


def media_de(ph, caption=""):
    if not ph or not ph.get("fichier"):
        return {"url": "", "credit": "", "caption": caption}
    morceaux = [m for m in (ph.get("auteur"), ph.get("licence")) if m]
    credit = " · ".join(morceaux + ["Wikimedia Commons"])
    return {"url": filepath_url(ph["fichier"]), "credit": credit, "caption": caption}


# --------------------------------------------------------------------------- graphiques
def graphiques(mv, lim):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    import matplotlib.dates as mdates
    plt.rcParams["font.family"] = ["Segoe UI", "DejaVu Sans"]

    # ---- frise
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    fig.patch.set_facecolor(PAPIER); ax.set_facecolor(PAPIER)
    bandes = [("precurseurs", "2014-01-01", "2019-01-01"), ("vague1", "2019-01-01", "2023-07-01"),
              ("vague2", "2023-07-01", "2026-01-01"), ("2026", "2026-01-01", "2026-12-31")]
    tons = ["#e3e1da", "#d8dde3", "#e3e1da", "#d8dde3"]
    for (code, a, b), t in zip(bandes, tons):
        a, b = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
        ax.axvspan(a, b, color=t, zorder=0)
        an, fr, en = EPO[code]
        ax.text(a + (b - a) / 2, 13.3, f"{fr}\n{an}", ha="center", va="top", fontsize=12, color="#2b2d42", weight="bold")
        ax.text(a + (b - a) / 2, 12.35, en, ha="center", va="top", fontsize=10, color="#666", style="italic")
    pos = []  # anti-chevauchement : chaque rond + étiquette occupe un intervalle de dates ; on empile
    for r in sorted(mv + lim, key=lambda r: r["debut"]):
        d = dt.date.fromisoformat(r["debut"])
        lib0 = r["ville"].replace(" 2019", "").replace(" 2023", "").replace(" 2025", "")
        a0, b0 = d - dt.timedelta(days=25), d + dt.timedelta(days=70 + 17 * len(lib0))
        y = 0.8 if not r["cas_limite"] else -0.8
        pas = 0.85 if not r["cas_limite"] else -0.85
        while any(a0 < b and a < b0 and abs(y - yy) < 0.8 for a, b, yy in pos):
            y += pas
        pos.append((a0, b0, y))
        if r["cas_limite"]:
            ax.scatter(d, y, s=170, facecolor="white", edgecolor=COUL["cas_limite"], linewidth=2, zorder=3)
        else:
            ax.scatter(d, y, s=230, color=COUL[r["resultat"]], edgecolor="white", linewidth=1.2, zorder=3)
        lib = r["ville"].replace(" 2019", "").replace(" 2023", "").replace(" 2025", "")
        ax.text(d + dt.timedelta(days=38), y, lib, fontsize=7.6, va="center",
                color="#2b2d42" if not r["cas_limite"] else "#8a8a8a", zorder=4)
    ax.axhline(0, color="#2b2d42", lw=1)
    ax.set_ylim(-6.6, 13.6)
    ax.set_xlim(dt.date(2014, 1, 1), dt.date(2026, 12, 31))
    ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", labelsize=12, colors="#2b2d42"); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    leg = [Line2D([], [], marker="o", ls="", ms=12, color=COUL[k], label=f"{ISSUE[k][0]} · {ISSUE[k][1]}") for k in ISSUE]
    leg.append(Line2D([], [], marker="o", ls="", ms=11, mfc="white", mec=COUL["cas_limite"], mew=2,
                      label="cas limite (sous l'axe) · borderline case"))
    ax.legend(handles=leg, loc="upper left", bbox_to_anchor=(0, -0.05), ncol=5, frameon=False, fontsize=10.5)
    ax.set_title("Révoltes de la génération Z, 2014–2026 · Gen Z uprisings, 2014–2026\n"
                 "un rond par mouvement, à sa date de début · one dot per movement, at its start date",
                 fontsize=15, color="#2b2d42", loc="left")
    fig.text(0.99, 0.01, "Données : Wikipédia, presse, ONG · #30DayMapChallenge 2026, Day 27", ha="right",
             fontsize=8.5, color="#777")
    fig.tight_layout()
    fig.savefig(sortie(OUT_FRISE), facecolor=fig.get_facecolor()); plt.close(fig)

    # ---- taux de réussite par époque
    fig, ax = plt.subplots(figsize=(12, 6.75), dpi=110)
    fig.patch.set_facecolor(PAPIER); ax.set_facecolor(PAPIER)
    lignes = [(c, [r for r in mv if r["epoque"] == c]) for c, *_ in EPOQUES] + [("total", mv)]
    for i, (c, rs) in enumerate(lignes[::-1]):
        x = 0
        for k in ISSUE:
            n = sum(r["resultat"] == k for r in rs)
            if n:
                ax.barh(i, n / len(rs) * 100, left=x, color=COUL[k], edgecolor=PAPIER, height=0.62)
                ax.text(x + n / len(rs) * 50, i, str(n), ha="center", va="center", fontsize=11,
                        color="white" if k in ("repression", "en_cours") else "#2b2d42", weight="bold")
                x += n / len(rs) * 100
        ok = sum(r["resultat"] in ("victoire", "concession") for r in rs)
        lib = "Total" if c == "total" else f"{EPO[c][1]}\n{EPO[c][0]}"
        ax.text(-2, i, lib, ha="right", va="center", fontsize=11, color="#2b2d42")
        ax.text(102, i, f"{round(100 * ok / len(rs))} %", ha="left", va="center", fontsize=15, weight="bold", color="#2b2d42")
        ax.text(102, i - 0.3, f"{ok}/{len(rs)}", ha="left", va="center", fontsize=9, color="#666")
    ax.set_xlim(-30, 115); ax.set_ylim(-0.6, len(lignes) - 0.2); ax.axis("off")
    ax.set_title("Victoire ou concessions, par époque · won or conceded, by period  (38 mouvements · movements)",
                 fontsize=13, color="#2b2d42", loc="left")
    leg = [Line2D([], [], marker="s", ls="", ms=11, color=COUL[k], label=f"{ISSUE[k][0]} · {ISSUE[k][1]}") for k in ISSUE]
    ax.legend(handles=leg, loc="lower center", bbox_to_anchor=(0.5, -0.09), ncol=4, frameon=False, fontsize=10)
    fig.tight_layout()
    fig.savefig(sortie(OUT_TAUX), facecolor=fig.get_facecolor()); plt.close(fig)


# --------------------------------------------------------------------------- diapositives
def slide(n_type, headline, date, lat, lon, zoom, text, media, fond, issue="", background_image=None):
    s = {"date": date, "location": {"lat": round(lat, 4), "lon": round(lon, 4), "zoom": zoom, "line": True},
         "text": {"headline": headline, "text": text}, "media": media, "background": {"color": fond}}
    if n_type == "overview":
        s = {"type": "overview", **s}
    if background_image:
        s["background"]["url"] = background_image
    s["_issue"] = issue
    return s


def construire(rows, pays, diff, ph):
    mv = sorted([r for r in rows if not r["cas_limite"]], key=lambda r: r["debut"])
    lim = sorted([r for r in rows if r["cas_limite"]], key=lambda r: r["debut"])
    par_ville = {r["ville"]: r for r in rows}
    fam_de = {}
    for t, de, vers in diff:
        for v in (de, vers):
            fam_de.setdefault(v, [])
            if t not in fam_de[v]:
                fam_de[v].append(t)

    def contexte_pays(r):
        nom = PAYS_ALIAS.get(r["pays_en"], r["pays_en"])
        p = pays.get(nom)
        if not p or p[0] is None:
            return ""
        age, ch, _ = p
        ch_txt = f"{ch:.1f} %".replace(".", ",") if ch is not None else "n. d."
        return (f"<p><b>Contexte</b> : âge médian {age:.0f} ans, chômage des 15–24 ans {ch_txt} · "
                f"<i>median age {age:.0f}, youth unemployment {ch_txt.replace(',', '.')}</i></p>")

    S = []
    # 0 ---- titre
    S.append(slide("overview", "Le pouvoir change de mains ? · <i>Power Shift?</i>", "2014–2026", 20, 20, 2,
                   "<p><b>Révoltes de la génération Z, 2014–2026</b> · <i>Gen Z uprisings, 2014–2026</i></p>"
                   "<p>Des parapluies zillennials de Hong Kong (2014) aux lycéens de Paris (2026) : 38 mouvements, "
                   "leurs issues et les symboles qui sautent d'un continent à l'autre.</p>"
                   "<p><i>From the zillennial umbrellas of Hong Kong (2014) to the high-schoolers of Paris (2026): "
                   "38 movements, their outcomes and the symbols that jump between continents.</i></p>"
                   "<p><small>#30DayMapChallenge 2026 · Day 27 « New tool » · d'après la carte du Day 12 « Power »</small></p>",
                   media_de(ph.get("Umbrella Movement"), "Hong Kong, 2014 · parapluies jaunes · yellow umbrellas"),
                   FOND["neutre"]))

    # 1 ---- contexte bivarié
    ages = [p[0] for p in pays.values() if p[0] is not None]
    chs = [p[1] for p in pays.values() if p[1] is not None]
    ag_mv, ch_mv = [], []
    for r in mv:
        p = pays.get(PAYS_ALIAS.get(r["pays_en"], r["pays_en"]))
        if p and p[0] is not None:
            ag_mv.append(p[0])
        if p and p[1] is not None:
            ch_mv.append(p[1])
    med = lambda l: sorted(l)[len(l) // 2]
    S.append(slide("", "Jeunes et sans emploi ? · <i>Young and jobless?</i>", "ONU WPP 2024 × OIT 2025", 15, 30, 2,
                   "<p>Sur la carte du Day 12, chaque pays croise deux variables : l'<b>âge médian</b> (ONU, World Population "
                   "Prospects 2024, via Our World in Data) et le <b>chômage des 15–24 ans</b> (OIT via Banque mondiale, 2025 ; "
                   "Taïwan : DGBAS ; Kosovo : KAS), en 3 classes chacune.</p>"
                   f"<p>Âge médian : moins de 25 ans, 25–36 ans, plus de 36 ans. Chômage des jeunes : moins de 9,3 %, 9,3–18,2 %, "
                   f"plus de 18,2 %.</p>"
                   f"<p>Âge médian (valeur médiane) des pays touchés : <b>{med(ag_mv):.0f} ans</b> contre {med(ages):.0f} ans pour "
                   f"l'ensemble des pays ; chômage des jeunes : <b>{med(ch_mv):.1f} %</b> contre {med(chs):.1f} %.</p>"
                   .replace(f"{med(ch_mv):.1f}", f"{med(ch_mv):.1f}".replace(".", ","))
                   .replace(f"{med(chs):.1f}", f"{med(chs):.1f}".replace(".", ","))
                   + "<p><i>Each country crosses median age (UN WPP 2024) and youth unemployment (ILO/World Bank 2025). "
                   f"Median for countries with a movement: {med(ag_mv):.0f} years and {med(ch_mv):.1f} % (all countries: "
                   f"{med(ages):.0f} years, {med(chs):.1f} %).</i></p>",
                   {"url": OUT_CARTE.name, "credit": "Carte Day 12 « Power » · CC BY-SA 4.0",
                    "caption": "Âge médian × chômage des 15–24 ans · median age × youth unemployment"},
                   FOND["contexte"]))

    # 2 ---- frise
    blocs = []
    for code, an, fr, en in EPOQUES:
        items = [r for r in mv if r["epoque"] == code]
        lis = "".join(f"<li>{r['debut'][:4]} · <b>{esc(r['nom_fr'])}</b> ({esc(r['pays_fr'])}) – {ISSUE[r['resultat']][0]}</li>"
                      for r in items)
        blocs.append(f"<p><b>{an} · {fr}</b> · <i>{en}</i> ({len(items)})</p><ul>{lis}</ul>")
    S.append(slide("", "Frise 2014–2026 · <i>Timeline 2014–2026</i>", "2014–2026", 20, 20, 2,
                   "<p>Un rond par mouvement, à sa date de début ; couleur = issue. Sous l'axe, les cas limites. "
                   "· <i>One dot per movement at its start date; colour = outcome.</i></p>" + "".join(blocs),
                   {"url": OUT_FRISE.name, "credit": "Frise réalisée avec matplotlib · CC BY-SA 4.0",
                    "caption": "4 époques, 38 mouvements · 4 periods, 38 movements"},
                   FOND["neutre"]))

    # 3 ---- un mouvement par diapositive
    for r in mv:
        pfr, pen = periode(r)
        ifr, ien = ISSUE[r["resultat"]]
        an, efr, een = EPO[r["epoque"]]
        fams = [FAMILLES[f] for f in fam_de.get(r["ville"], [])]
        t = (f"<p><b>Dates</b> : {pfr} ({duree_jours(r)} jours) · <i>{pen}</i></p>"
             f"<p><b>Issue</b> : {bi(ifr, ien)}</p>"
             f"<p><b>Symbole</b> : {esc(r['picto'])} {bi(esc(r['symbole_fr']), esc(r['symbole_en']))}</p>")
        if r["slogan"]:
            t += f"<p><b>Slogan</b> : « {esc(r['slogan'])} »</p>"
        if fams:
            t += "<p><b>Famille de symbole</b> : " + ", ".join(bi(f["fr"], f["en"]) for f in fams) + "</p>"
        t += f"<p><b>Époque</b> : {bi(efr + ' ' + an, een)}</p>" + contexte_pays(r)
        p = ph.get(r["nom_en"])
        if p and p.get("page"):
            t += f'<p><small>Photo : <a href="{p["page"]}" target="_blank">page Wikimedia Commons</a></small></p>'
        cap = f"« {r['slogan']} »" if r["slogan"] else bi(r["symbole_fr"], r["symbole_en"]).replace("<i>", "").replace("</i>", "")
        S.append(slide("", f"{esc(r['nom_fr'])} · {esc(r['pays_fr'])}", pfr, r["lat"], r["lon"], 6, t,
                       media_de(p, cap), FOND[r["resultat"]], r["resultat"]))

    # 4 ---- symboles qui voyagent
    for code, f in FAMILLES.items():
        villes = []
        for t_, de, vers in diff:
            if t_ == code:
                for v in (de, vers):
                    if v not in villes:
                        villes.append(v)
        concernes = sorted([par_ville[v] for v in villes if v in par_ville], key=lambda r: r["debut"])
        foyer = par_ville[f["foyer"]]
        lis = "".join(f"<li><b>{esc(r['nom_fr'])}</b> ({esc(r['pays_fr'])}, {r['debut'][:4]}) : {esc(r['picto'])} "
                      f"{esc(r['symbole_fr'])}" + (f" – « {esc(r['slogan'])} »" if r["slogan"] else "") + "</li>"
                      for r in concernes)
        p = ph.get(foyer["nom_en"])
        S.append(slide("", f"Symbole qui voyage : {f['fr']} · <i>Travelling symbol: {f['en']}</i>",
                       f"{concernes[0]['debut'][:4]}–{concernes[-1]['debut'][:4]}", foyer["lat"], foyer["lon"], f["zoom"],
                       f"<p>{f['txt_fr']}</p><p><i>{f['txt_en']}</i></p>"
                       f"<p><b>Symboles &amp; slogans</b> · <i>Symbols &amp; slogans</i></p><ul>{lis}</ul>"
                       f"<p><small>Foyer d'origine : {esc(foyer['ville'])} · origin</small></p>",
                       media_de(p, f"{f['fr']} · {f['en']}"), FOND["symbole"], "symbole"))

    # 5 ---- cas limites
    lis = "".join(f"<li>{r['debut'][:4]} · <b>{esc(r['nom_fr'])}</b> ({esc(r['pays_fr'])})</li>" for r in lim)
    S.append(slide("", f"Cas limites ({len(lim)}) · <i>Borderline cases</i>", "2023–2026", 25, 20, 2,
                   "<p>Des mobilisations où la jeunesse était très présente sans que le mouvement soit spécifiquement « Gen Z » "
                   "(intergénérationnel, syndical, campus, crise économique…). Laissées en gris sur la carte, hors des statistiques.</p>"
                   "<p><i>Protests with a strong youth presence but not specifically “Gen Z”; shown in grey, excluded "
                   "from the statistics.</i></p>" + f"<ul>{lis}</ul>",
                   {"url": "", "credit": "", "caption": ""}, FOND["cas_limite"], "cas_limite"))
    for r in lim:
        pfr, pen = periode(r)
        ifr, ien = ISSUE[r["resultat"]]
        t = (f"<p><b>Cas limite</b> · <i>borderline case</i></p>"
             f"<p><b>Dates</b> : {pfr} · <i>{pen}</i></p><p><b>Issue</b> : {bi(ifr, ien)}</p>")
        if r["symbole_fr"]:
            t += f"<p><b>Pourquoi limite</b> : {bi(esc(r['symbole_fr']), esc(r['symbole_en']))}</p>"
        if r["slogan"]:
            t += f"<p><b>Slogan</b> : « {esc(r['slogan'])} »</p>"
        t += contexte_pays(r)
        p = ph.get(r["nom_en"])
        if p and p.get("page"):
            t += f'<p><small>Photo : <a href="{p["page"]}" target="_blank">page Wikimedia Commons</a></small></p>'
        cap = f"« {r['slogan']} »" if r["slogan"] else f"Cas limite · {r['nom_en']}"
        S.append(slide("", f"Cas limite · {esc(r['nom_fr'])} · {esc(r['pays_fr'])}", pfr, r["lat"], r["lon"], 6, t,
                       media_de(p, cap), FOND["cas_limite"], "cas_limite"))

    # 6 ---- taux de réussite
    stats = []
    for code, an, fr, en in EPOQUES + [("total", "2014–2026", "Total", "Total")]:
        rs = mv if code == "total" else [r for r in mv if r["epoque"] == code]
        c = {k: sum(r["resultat"] == k for r in rs) for k in ISSUE}
        ok = c["victoire"] + c["concession"]
        stats.append((an, fr, en, len(rs), c, ok))
    lignes = "".join(f"<li><b>{an} · {fr}</b> : {n} mouvements, <b>{round(100 * ok / n)} %</b> victoire ou concession "
                     f"({c['victoire']} V, {c['concession']} C, {c['repression']} R, {c['en_cours']} en cours)</li>"
                     for an, fr, en, n, c, ok in stats)
    tot = stats[-1]
    pc = {k: round(100 * v / tot[3]) for k, v in tot[4].items()}
    d26 = stats[3]
    decides26 = d26[3] - d26[4]["en_cours"]
    S.append(slide("", "Et ça marche ? · <i>Does it work?</i>", "2014–2026", 20, 20, 2,
                   f"<p>Sur les {tot[3]} mouvements : {pc['victoire']} % ont fait tomber un gouvernement ou obtenu ce qu'ils "
                   f"demandaient, {pc['concession']} % ont arraché des concessions, {pc['repression']} % ont été écrasés et "
                   f"{pc['en_cours']} % sont encore en cours.</p><ul>{lignes}</ul>"
                   f"<p>Les précurseurs ne comptent que {stats[0][3]} mouvements ; la vague 2019–2023 voit Hong Kong, la Thaïlande, "
                   f"le Myanmar et l'Iran réprimés ; puis tout s'accélère en 2023–2025. En 2026, {d26[4]['en_cours']} mouvements "
                   f"sur {d26[3]} sont encore en cours ({d26[5]} succès sur {decides26} issues connues).</p>"
                   f"<p><i>Of {tot[3]} movements: {pc['victoire']} % won, {pc['concession']} % won concessions, "
                   f"{pc['repression']} % were crushed, {pc['en_cours']} % are ongoing. Success rate by period: "
                   + ", ".join(f"{an} {round(100 * ok / n)} %" for an, fr, en, n, c, ok in stats[:4]) + ".</i></p>"
                   "<p><small>Recalculé sur le CSV (cas limites exclus), état au 8 nov. 2026.</small></p>",
                   {"url": OUT_TAUX.name, "credit": "Graphique matplotlib · CC BY-SA 4.0",
                    "caption": "Victoire ou concessions par époque · won or conceded, by period"},
                   FOND["neutre"]))

    # 7 ---- sources et licences
    vus, cred = set(), []
    for r in mv + lim:
        p = ph.get(r["nom_en"])
        if p and p.get("fichier") and p["fichier"] not in vus:
            vus.add(p["fichier"])
            cred.append(f'<li>{esc(r["nom_fr"])} : <a href="{p["page"]}" target="_blank">{esc(p.get("auteur") or "auteur sur la page")}</a>'
                        f'{", " + esc(p["licence"]) if p.get("licence") else ""}</li>')
    S.append(slide("", "Sources et licences · <i>Sources &amp; licences</i>", "", 20, 20, 2,
                   "<p><b>Données</b> : Wikipédia, presse internationale, ONG (HRW, Amnesty, FIDH) ; âge médian ONU WPP 2024 "
                   "(via OWID) ; chômage des 15–24 ans OIT via Banque mondiale (2025), Taïwan DGBAS, Kosovo KAS. "
                   "Pour aller plus loin : <a href=\"https://theconversation.com/topics/gen-z-protests-175785\" target=\"_blank\">"
                   "dossier The Conversation</a>.</p>"
                   "<p><b>Fond de carte</b> : © contributeurs OpenStreetMap (ODbL). <b>Outil</b> : StoryMapJS, Knight Lab.</p>"
                   "<p><b>Photos</b> : Wikimedia Commons, licences libres (CC BY, CC BY-SA, domaine public) ; auteur et licence de "
                   "chaque photo dans son crédit et ci-dessous. Les photos CC BY-SA restent sous CC BY-SA.</p>"
                   f"<ul>{''.join(cred)}</ul>"
                   "<p><small>Carte, frise et textes : Estelle Sérèmes, CC BY-SA 4.0 · #30DayMapChallenge 2026 · Next Generation "
                   "Cartographers</small></p>",
                   {"url": "", "credit": "", "caption": ""}, FOND["neutre"]))
    return S, mv, lim


# --------------------------------------------------------------------------- écriture
def ecrire(S):
    slides = [{k: v for k, v in s.items() if not k.startswith("_")} for s in S]
    doc = {"storymap": {"language": "fr", "map_type": "osm:standard", "calculate_zoom": False, "slides": slides}}
    sortie(OUT_JSON).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    cols = ["n", "type", "headline", "date", "lat", "lon", "zoom", "recherche_carte", "media_url", "media_credit",
            "media_caption", "texte_html", "issue", "fond_couleur", "commons_page"]
    with open(sortie(OUT_CSV), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        w.writerow(cols)
        for i, s in enumerate(S):
            loc = s["location"]
            m = re.search(r'href="(https://commons\.wikimedia\.org/wiki/File:[^"]+)"', s["text"]["text"])
            w.writerow([i, s.get("type", "slide"), s["text"]["headline"], s["date"], f"{loc['lat']:.4f}", f"{loc['lon']:.4f}",
                        loc["zoom"], f"lat:{loc['lat']:.4f} lon:{loc['lon']:.4f}", s["media"]["url"], s["media"]["credit"],
                        s["media"]["caption"], s["text"]["text"], s["_issue"], s["background"]["color"],
                        m.group(1) if m else ""])

    inline = json.dumps(doc, ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Power Shift · StoryMap</title>
<link rel="stylesheet" href="https://cdn.knightlab.com/libs/storymapjs/latest/css/storymap.css">
<script src="https://cdn.knightlab.com/libs/storymapjs/latest/js/storymap-min.js"></script>
<style>
  html, body {{ height: 100%; margin: 0; background: #efeeea; }}
  #mapdiv {{ width: 100%; height: 100%; }}
</style>
</head>
<body>
<div id="mapdiv"></div>
<!-- Copie intégrée du JSON : la page marche aussi ouverte en file:// (sans serveur). -->
<script id="donnees" type="application/json">{inline}</script>
<script>
  var options = {{ language: "fr", map_type: "osm:standard", calculate_zoom: false }};
  var Classe = window.KLStoryMap ? KLStoryMap.StoryMap : VCO.StoryMap;
  function lancer(data) {{ window.storymap = new Classe("mapdiv", data, options);
    window.addEventListener("resize", function () {{ storymap.updateDisplay(); }});
    // la feuille de style arrive parfois après l'initialisation : on recalcule la mise en page
    [300, 1200, 3000].forEach(function (t) {{ setTimeout(function () {{ storymap.updateDisplay(); }}, t); }}); }}
  fetch("storymap_genz.json").then(function (r) {{ if (!r.ok) throw r; return r.json(); }})
    .then(lancer)
    .catch(function () {{ lancer(JSON.parse(document.getElementById("donnees").textContent)); }});
</script>
</body>
</html>
"""
    sortie(OUT_HTML).write_text(page, encoding="utf-8")


def verifier(S, rows):
    doc = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    sl = doc["storymap"]["slides"]
    assert len(sl) == len(S)
    assert sl[0].get("type") == "overview"
    pb = []
    for i, s in enumerate(sl):
        loc = s["location"]
        if loc.get("lat") in (None, "") or loc.get("lon") in (None, ""):
            pb.append(f"slide {i} : coordonnées vides")
        u = s["media"]["url"]
        if u.startswith("http") and not re.fullmatch(r"https://commons\.wikimedia\.org/wiki/Special:FilePath/[^\s?]+\?width=1280", u):
            pb.append(f"slide {i} : lien Commons mal formé {u}")
    sans_photo = [r["nom_fr"] for r in rows if not any(
        s["text"]["headline"].endswith(esc(r["pays_fr"])) and esc(r["nom_fr"]) in s["text"]["headline"] and s["media"]["url"]
        for s in sl)]
    sans_coord = [r["nom_fr"] for r in rows if r["lat"] in (None, "") or r["lon"] in (None, "")]
    return len(sl), pb, sans_photo, sans_coord


def main():
    hors_ligne = "--hors-ligne" in sys.argv
    rows = lire_csv()
    pays, diff = lire_gpkg()
    print(f"{len(rows)} lignes : {sum(not r['cas_limite'] for r in rows)} mouvements, {sum(r['cas_limite'] for r in rows)} cas limites")
    ph = photos(rows, hors_ligne)
    if not OUT_CARTE.exists() and CARTE_SRC.exists():
        shutil.copyfile(CARTE_SRC, sortie(OUT_CARTE))  # copie (l'original n'est pas touché)
    S, mv, lim = construire(rows, pays, diff, ph)
    graphiques(mv, lim)
    ecrire(S)
    n, pb, sans_photo, sans_coord = verifier(S, rows)
    print(f"{n} diapositives ; problèmes : {pb or 'aucun'}")
    print(f"sans photo ({len(sans_photo)}) : {', '.join(sans_photo) or '-'}")
    print(f"sans coordonnées : {', '.join(sans_coord) or '-'}")


if __name__ == "__main__":
    main()
