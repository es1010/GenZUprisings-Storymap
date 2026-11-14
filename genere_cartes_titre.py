# -*- coding: utf-8 -*-
"""
Cartes-titre (PNG 1280×800) pour les diapositives sans photo libre fiable, dans la charte de la carte du Day 12 :
fond = couleur de l'issue, grand pictogramme du mouvement dans un rond blanc, nom + pays + dates FR/EN,
slogan (ou symbole) en violet gras, police Segoe UI.

Lance avec le Python de QGIS (Qt sait dessiner les pictos SVG) :
    C:\\OSGeo4W\\bin\\python-qgis-ltr.bat genere_cartes_titre.py
Lit ../power/mouvements_genz.csv et ../power/pictos/*.svg (lecture seule) ; écrit uniquement dans cartes_titre/.
"""
import csv, datetime as dt, re, sys
from pathlib import Path
from PyQt5.QtCore import Qt, QRectF, QByteArray
from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QPen, QBrush, QFontMetrics
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QApplication

ICI = Path(__file__).resolve().parent
POWER = ICI.parent / "power"
SORTIE = ICI / "cartes_titre"
# diapositives sans photo libre fiable (recherche Commons du 14/11/2026)
VILLES = ["Addis-Abeba", "Leh", "Dar es Salaam", "Athènes", "Asunción", "Malé", "Muzaffarabad", "Dakar 2023"]

COUL = {"victoire": "#ffd23f", "concession": "#f28c28", "repression": "#2b2d42", "en_cours": "#9d4edd", "cas_limite": "#bdbdbd"}
ISSUE = {"victoire": ("victoire", "won"), "concession": ("concessions obtenues", "concessions won"),
         "repression": ("réprimé", "crushed"), "en_cours": ("en cours", "ongoing")}
VIOLET, ENCRE = "#9d4edd", "#2b2d42"
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def slug(v):
    s = v.lower()
    for a, b in (("é", "e"), ("è", "e"), ("ó", "o"), ("ç", "c"), ("à", "a")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def dates(r):
    d = dt.date.fromisoformat(r["debut"])
    fr = lambda x: f"{x.day} {MOIS[x.month - 1]} {x.year}"
    en = lambda x: f"{MONTHS[x.month - 1]} {x.day}, {x.year}"
    if not r["fin"]:
        return f"depuis le {fr(d)}", f"since {en(d)}"
    f = dt.date.fromisoformat(r["fin"])
    return f"{fr(d)} – {fr(f)}", f"{en(d)} – {en(f)}"


def picto(painter, nom, rect, couleur):
    chemin = POWER / "pictos" / f"{nom}.svg"
    if not nom or not chemin.exists():
        return False
    s = chemin.read_text(encoding="utf-8")
    s = re.sub(r'fill="param\(fill\)[^"]*"', f'fill="{couleur}"', s)
    s = re.sub(r'stroke="param\(outline\)[^"]*"', f'stroke="{couleur}"', s)
    s = re.sub(r'="param\([^)]*\)\s*([^"]*)"', r'="\1"', s)
    rd = QSvgRenderer(QByteArray(s.encode("utf-8")))
    if not rd.isValid():
        return False
    rd.setAspectRatioMode(Qt.KeepAspectRatio)
    rd.render(painter, rect)
    return True


def texte(p, x, y, w, h, s, taille, gras=False, italique=False, couleur=ENCRE, flags=Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap):
    f = QFont("Segoe UI"); f.setPixelSize(taille); f.setBold(gras); f.setItalic(italique)
    p.setFont(f); p.setPen(QColor(couleur))
    r = p.boundingRect(QRectF(x, y, w, h), flags, s)
    p.drawText(QRectF(x, y, w, h), flags, s)
    return r.height()


def carte(r, picto_nom):
    W, H = 1280, 800
    issue = "cas_limite" if r["cas_limite"] == "1" else r["resultat"]
    fond = COUL[issue]
    clair = issue in ("repression", "en_cours")
    txt, doux = ("#ffffff", "#e6e6ee") if clair else (ENCRE, "#4a4a55")
    img = QImage(W, H, QImage.Format_ARGB32); img.fill(QColor(fond))
    p = QPainter(img); p.setRenderHint(QPainter.Antialiasing); p.setRenderHint(QPainter.TextAntialiasing)

    texte(p, 64, 44, 1150, 40, "Le pouvoir change de mains ? · Power Shift?", 24, True, couleur=doux)
    # grand rond blanc avec le pictogramme (couleur d'issue), comme les ronds de la carte
    cx, cy, R = 300, 420, 190
    p.setPen(Qt.NoPen); p.setBrush(QBrush(QColor("#ffffff"))); p.drawEllipse(QRectF(cx - R - 14, cy - R - 14, 2 * R + 28, 2 * R + 28))
    p.setBrush(QBrush(QColor(fond))); p.drawEllipse(QRectF(cx - R, cy - R, 2 * R, 2 * R))
    if issue == "cas_limite":
        pen = QPen(QColor("#6b6b6b")); pen.setWidth(6); p.setPen(pen); p.setBrush(Qt.NoBrush)
        p.drawEllipse(QRectF(cx - R, cy - R, 2 * R, 2 * R))
        texte(p, cx - R, cy - 60, 2 * R, 120, "cas limite\nborderline", 40, True, couleur=ENCRE, flags=Qt.AlignCenter)
    else:
        coul_picto = "#ffffff" if clair else "#1b1b1b"
        t = R * 1.24
        if not picto(p, picto_nom, QRectF(cx - t / 2, cy - t / 2, t, t), coul_picto):
            texte(p, cx - R, cy - 90, 2 * R, 180, r["picto"] or "", 150, flags=Qt.AlignCenter, couleur=coul_picto)

    x, y, w = 560, 190, 660
    y += texte(p, x, y, w, 260, r["nom_fr"], 54, True, couleur=txt) + 6
    if r["nom_en"] and r["nom_en"] != r["nom_fr"]:
        y += texte(p, x, y, w, 80, r["nom_en"], 26, italique=True, couleur=doux) + 14
    fr, en = dates(r)
    y += texte(p, x, y, w, 60, f"{r['pays_fr']} · {fr}", 26, couleur=txt) + 2
    y += texte(p, x, y, w, 60, f"{r['pays_en']} · {en}", 21, italique=True, couleur=doux) + 14
    iss = ISSUE[r["resultat"]]
    y += texte(p, x, y, w, 60, ("cas limite · " if issue == "cas_limite" else "") + f"{iss[0]} · {iss[1]}", 24, True, couleur=txt) + 26
    # slogan (ou, à défaut, le symbole du mouvement) en violet gras, sur un cartouche blanc pour rester lisible
    ligne = f"« {r['slogan']} »" if r["slogan"] else (r["symbole_fr"] or "")
    if ligne:
        f = QFont("Segoe UI"); f.setPixelSize(30); f.setBold(True); p.setFont(f)
        br = p.boundingRect(QRectF(x + 18, y + 12, w - 36, 200), Qt.AlignLeft | Qt.TextWordWrap, ligne)
        p.setPen(Qt.NoPen); p.setBrush(QBrush(QColor(255, 255, 255, 235)))
        p.drawRoundedRect(QRectF(x, y, min(w, br.width() + 40), br.height() + 24), 12, 12)
        p.setPen(QColor(VIOLET)); p.drawText(QRectF(x + 18, y + 12, w - 36, 200), Qt.AlignLeft | Qt.TextWordWrap, ligne)
    texte(p, 64, H - 52, 1150, 30, "Illustration (pas de photo libre fiable) · Estelle Sérèmes, CC BY-SA 4.0 · #30DayMapChallenge 2026",
          16, couleur=doux)
    p.end()
    SORTIE.mkdir(exist_ok=True)
    out = SORTIE / f"{slug(r['ville'])}.png"
    if out.resolve().parent != SORTIE.resolve():
        raise SystemExit("refus d'écrire hors de cartes_titre")
    img.save(str(out), "PNG")
    return out


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    import sqlite3
    c = sqlite3.connect(f"file:{(POWER / 'genz_power.gpkg').as_posix()}?mode=ro", uri=True)
    pictos = {v: (Path(s).stem if s else None) for v, s in c.execute("select ville, picto_svg from mouvements")}
    c.close()
    with open(POWER / "mouvements_genz.csv", encoding="utf-8-sig", newline="") as fh:
        rows = {r["ville"]: r for r in csv.DictReader(fh, delimiter=";")}
    for v in VILLES:
        r = rows[v]
        print(carte(r, None if r["cas_limite"] == "1" else pictos.get(v)).name)


if __name__ == "__main__":
    main()
