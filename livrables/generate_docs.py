# -*- coding: utf-8 -*-
"""Génère les livrables PDF (groupe + individuels) — mise en page soignée,
rédaction en paragraphes, schéma d'architecture et diagramme de Gantt."""
import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, CondPageBreak, Flowable,
                                KeepTogether)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon

OUT = os.path.dirname(os.path.abspath(__file__))
CODE = "M2DOC"                # code promo (classe M2 DO C)
CLASSE = "M2 DO C"
PERIODE = "Janvier – Juin 2026"

# Palette « Canva »
NAVY = colors.HexColor("#15314b")
BLUE = colors.HexColor("#2f6fb0")
ACCENT = colors.HexColor("#00a39a")
LIGHT = colors.HexColor("#eef3f8")
LIGHT2 = colors.HexColor("#e4eef7")
GREY = colors.HexColor("#5b6b7b")
WHITE = colors.white

CONTENT_W = A4[0] - 4 * cm     # largeur utile (marges 2cm)

ss = getSampleStyleSheet()
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontName="Helvetica",
                      fontSize=10.5, leading=16, alignment=TA_JUSTIFY,
                      spaceAfter=8, textColor=colors.HexColor("#222b33"))
LEAD = ParagraphStyle("LEAD", parent=BODY, fontSize=11.5, leading=17,
                      textColor=NAVY)
CELL = ParagraphStyle("CELL", parent=BODY, fontSize=9, leading=12.5,
                      alignment=TA_LEFT, spaceAfter=0)
CELLH = ParagraphStyle("CELLH", parent=CELL, textColor=WHITE,
                       fontName="Helvetica-Bold")
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Helvetica-Bold",
                       textColor=NAVY)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=BLUE, fontSize=12.5,
                    spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
COVER_T = ParagraphStyle("COVER_T", parent=ss["Title"], textColor=WHITE,
                         fontSize=26, leading=30, alignment=TA_LEFT)
COVER_S = ParagraphStyle("COVER_S", parent=ss["Title"], textColor=colors.HexColor("#cfe2f3"),
                         fontSize=13, leading=18, alignment=TA_LEFT, fontName="Helvetica")
CENTER = ParagraphStyle("CENTER", parent=BODY, alignment=TA_CENTER)
NOTE = ParagraphStyle("NOTE", parent=BODY, fontSize=9, leading=13, textColor=GREY)


# --------------------------------------------------------------------- bandeaux
class Banner(Flowable):
    """Bandeau de couverture coloré, pleine largeur."""
    def __init__(self, title, subtitle, w=CONTENT_W, h=120):
        self.title, self.subtitle, self.w, self.h = title, subtitle, w, h

    def wrap(self, *a):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.w, self.h, 8, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, 0, 6, self.h, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(22, self.h - 42, self.title)
        c.setFillColor(colors.HexColor("#cfe2f3"))
        c.setFont("Helvetica", 12)
        # sous-titre sur plusieurs lignes si besoin
        y = self.h - 66
        for line in self.subtitle.split("\n"):
            c.drawString(22, y, line)
            y -= 17


def H1(text):
    """Titre de section : bande pleine largeur."""
    t = Table([[Paragraph(text, ParagraphStyle("h1", parent=BODY, fontSize=13.5,
              textColor=WHITE, fontName="Helvetica-Bold", spaceAfter=0))]],
              colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBEFORE", (0, 0), (0, -1), 5, ACCENT),
    ]))
    return KeepTogether([Spacer(1, 6), t, Spacer(1, 6)])


def P(text, style=BODY):
    return Paragraph(text, style)


def wrap_table(rows, widths, header=True, zebra=True):
    """Tableau dont chaque cellule est encapsulée (pas de débordement)."""
    data = []
    for i, row in enumerate(rows):
        line = []
        for cell in row:
            st = CELLH if (header and i == 0) else CELL
            line.append(Paragraph(str(cell), st))
        data.append(line)
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c4d2df")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), NAVY)]
    if zebra:
        style += [("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [WHITE, LIGHT])]
    t.setStyle(TableStyle(style))
    return t


# ------------------------------------------------------------ schéma archi
def architecture():
    W, H = CONTENT_W, 270
    d = Drawing(W, H)

    def box(x, y, w, h, lines, fill, fg=WHITE, fs=8.5, bold=True, r=5):
        d.add(Rect(x, y, w, h, rx=r, ry=r, fillColor=fill,
                   strokeColor=colors.HexColor("#9fb3c8"), strokeWidth=0.7))
        if isinstance(lines, str):
            lines = [lines]
        ty = y + h / 2 + (len(lines) - 1) * 5.5
        for ln in lines:
            s = String(x + w / 2, ty - 3, ln, fontSize=fs, fillColor=fg,
                       textAnchor="middle",
                       fontName="Helvetica-Bold" if bold else "Helvetica")
            d.add(s)
            ty -= 12

    def arrow(x1, y1, x2, y2):
        d.add(Line(x1, y1, x2, y2, strokeColor=GREY, strokeWidth=1.3))
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        l = 6
        d.add(Polygon([x2, y2,
                       x2 - l * math.cos(ang - 0.4), y2 - l * math.sin(ang - 0.4),
                       x2 - l * math.cos(ang + 0.4), y2 - l * math.sin(ang + 0.4)],
                      fillColor=GREY, strokeColor=GREY))

    # Ligne CI/CD (haut)
    box(0, H - 40, 95, 32, ["Développeur", "git push"], BLUE)
    arrow(95, H - 24, 120, H - 24)
    box(120, H - 40, 135, 32, ["GitHub Actions", "CI/CD"], ACCENT)
    arrow(255, H - 24, 280, H - 24)
    box(280, H - 40, 95, 32, ["Azure ACR", "(images)"], BLUE)
    arrow(327, H - 40, 327, H - 70)   # ACR -> AKS

    # Grand cadre AKS
    ax, ay, aw, ah = 30, 55, 330, 150
    d.add(Rect(ax, ay, aw, ah, rx=8, ry=8, fillColor=LIGHT2,
               strokeColor=BLUE, strokeWidth=1.2))
    d.add(String(ax + 12, ay + ah - 16, "Cluster AKS (Kubernetes)",
                 fontSize=10, fillColor=NAVY, fontName="Helvetica-Bold"))
    box(ax + 15, ay + ah - 60, aw - 30, 26, "Ingress NGINX (HTTP/HTTPS)", NAVY, fs=8.5)
    box(ax + 15, ay + 45, 135, 28, ["Frontend", "React"], BLUE)
    box(ax + 180, ay + 45, 135, 28, ["Backend", "FastAPI"], BLUE)
    box(ax + 15, ay + 8, 300, 26, ["Monitoring : Prometheus · Grafana · Loki · Alertmanager"],
        ACCENT, fs=8)
    # liens internes
    arrow(ax + aw / 2, ay + ah - 60, ax + 82, ay + 73)
    arrow(ax + aw / 2, ay + ah - 60, ax + 247, ay + 73)

    # PostgreSQL (droite)
    box(W - 120, ay + 95, 118, 40, ["PostgreSQL", "Flexible (TLS)"], GREY)
    arrow(ax + 315, ay + 59, W - 120, ay + 112)

    # Utilisateurs
    box(W - 120, ay + ah - 18, 118, 30, ["Utilisateurs", "(cabinet)"], BLUE)
    arrow(W - 120, ay + ah - 3, ax + aw - 20, ay + ah - 47)

    # Site on-premise (bas)
    box(0, 6, W, 34,
        ["Site on-premise simulé (réseau séparé)  —  VM + MinIO chiffré  ·  sauvegardes pilotées par Ansible"],
        NAVY, fs=8.5)
    arrow(W - 60, ay + 95, W - 60, 40)   # postgres -> on-prem (backup)
    d.add(String(W - 56, (ay + 95 + 40) / 2, "backup",
                 fontSize=7, fillColor=GREY, fontName="Helvetica"))
    return d


# ------------------------------------------------------------ diagramme Gantt
def gantt():
    months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"]
    tasks = [
        ("Cadrage & analyse du besoin", 0.0, 1.0, BLUE),
        ("Architecture & choix FinOps", 0.6, 0.9, BLUE),
        ("Développement application", 1.0, 1.6, ACCENT),
        ("Conteneurisation (Docker)", 1.4, 0.9, ACCENT),
        ("Infrastructure Terraform", 2.0, 1.2, BLUE),
        ("CI/CD GitHub Actions", 2.2, 1.4, ACCENT),
        ("Kubernetes & Helm", 2.4, 1.2, BLUE),
        ("Observabilité (monitoring)", 3.1, 1.1, ACCENT),
        ("Sécurité (DevSecOps)", 3.3, 1.0, BLUE),
        ("On-premise · MinIO · PRA", 4.0, 1.0, ACCENT),
        ("Tests & validation", 4.4, 0.8, BLUE),
        ("Documentation & vidéo", 5.0, 1.0, ACCENT),
    ]
    label_w = 168
    month_w = (CONTENT_W - label_w) / 6.0
    row_h = 16
    top_pad = 22
    H = top_pad + len(tasks) * row_h + 8
    d = Drawing(CONTENT_W, H)
    # entête mois + grille
    for i, m in enumerate(months):
        x = label_w + i * month_w
        d.add(Line(x, 0, x, H - top_pad + 4, strokeColor=colors.HexColor("#d6e0ea"), strokeWidth=0.6))
        d.add(String(x + month_w / 2, H - 14, m, fontSize=8.5, fillColor=NAVY,
                     textAnchor="middle", fontName="Helvetica-Bold"))
    d.add(Line(label_w, 0, label_w, H - top_pad + 4, strokeColor=GREY, strokeWidth=0.8))
    d.add(Line(CONTENT_W, 0, CONTENT_W, H - top_pad + 4, strokeColor=colors.HexColor("#d6e0ea"), strokeWidth=0.6))
    # barres
    for j, (name, start, dur, col) in enumerate(tasks):
        y = H - top_pad - (j + 1) * row_h + 3
        d.add(String(0, y + 2, name, fontSize=8.3, fillColor=colors.HexColor("#222b33"),
                     fontName="Helvetica"))
        bx = label_w + start * month_w
        bw = max(dur * month_w, 8)
        d.add(Rect(bx, y, bw, row_h - 6, rx=3, ry=3, fillColor=col, strokeColor=col))
    return d


# ---------------------------------------------------- boîte à outils diagrammes
def _dbox(d, x, y, w, h, lines, fill, fg=WHITE, fs=9, bold=True, r=5):
    d.add(Rect(x, y, w, h, rx=r, ry=r, fillColor=fill,
               strokeColor=colors.HexColor("#9fb3c8"), strokeWidth=0.7))
    if isinstance(lines, str):
        lines = [lines]
    ty = y + h / 2 + (len(lines) - 1) * 6
    for ln in lines:
        d.add(String(x + w / 2, ty - 3, ln, fontSize=fs, fillColor=fg,
                     textAnchor="middle",
                     fontName="Helvetica-Bold" if bold else "Helvetica"))
        ty -= 12.5


def _arrow(d, x1, y1, x2, y2, color=GREY):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.3))
    a = math.atan2(y2 - y1, x2 - x1)
    l = 7
    d.add(Polygon([x2, y2, x2 - l * math.cos(a - 0.4), y2 - l * math.sin(a - 0.4),
                   x2 - l * math.cos(a + 0.4), y2 - l * math.sin(a + 0.4)],
                  fillColor=color, strokeColor=color))


def flow_vertical(steps, color=BLUE, box_h=30, gap=18):
    n = len(steps)
    H = n * box_h + (n - 1) * gap + 6
    d = Drawing(CONTENT_W, H)
    bw = CONTENT_W * 0.60
    bx = (CONTENT_W - bw) / 2
    y = H - box_h
    for i, s in enumerate(steps):
        _dbox(d, bx, y, bw, box_h, s, color, fs=9.5)
        if i < n - 1:
            _arrow(d, CONTENT_W / 2, y, CONTENT_W / 2, y - gap)
        y -= box_h + gap
    return d


def flow_horizontal(steps, color=ACCENT, box_h=42):
    n = len(steps)
    gap = 14
    bw = (CONTENT_W - (n - 1) * gap) / n
    H = box_h + 8
    d = Drawing(CONTENT_W, H)
    x, y = 0, 4
    for i, s in enumerate(steps):
        _dbox(d, x, y, bw, box_h, s, color, fs=8.3)
        if i < n - 1:
            _arrow(d, x + bw, y + box_h / 2, x + bw + gap, y + box_h / 2)
        x += bw + gap
    return d


def barh(pairs, unit="$/mois", color=BLUE):
    n = len(pairs)
    row_h = 26
    H = n * row_h + 10
    label_w = 132
    axis_w = CONTENT_W - label_w - 70
    maxv = max(v for _, v in pairs)
    d = Drawing(CONTENT_W, H)
    y = H - row_h
    for label, v in pairs:
        d.add(String(0, y + 8, label, fontSize=9, fillColor=NAVY, fontName="Helvetica"))
        bw = max(axis_w * v / maxv, 2)
        d.add(Rect(label_w, y + 3, bw, row_h - 12, rx=2, ry=2, fillColor=color, strokeColor=color))
        d.add(String(label_w + bw + 6, y + 6, "%g %s" % (v, unit), fontSize=8.5,
                     fillColor=GREY, fontName="Helvetica-Bold"))
        y -= row_h
    return d


def obs_diagram():
    W, H = CONTENT_W, 190
    d = Drawing(W, H)
    _dbox(d, 0, H - 70, 110, 44, ["Application", "(métriques + logs)"], BLUE, fs=8.5)
    _dbox(d, 175, H - 46, 120, 30, "Prometheus", ACCENT)
    _dbox(d, 175, H - 110, 120, 30, "Loki", ACCENT)
    _dbox(d, 360, H - 78, 120, 40, ["Grafana", "tableaux de bord"], BLUE, fs=8.5)
    _dbox(d, 175, H - 170, 120, 30, "Alertmanager", GREY)
    _dbox(d, 360, H - 170, 120, 30, ["Slack / Teams"], BLUE)
    _arrow(d, 110, H - 40, 175, H - 31)      # app -> prometheus (métriques)
    _arrow(d, 110, H - 56, 175, H - 95)      # app -> loki (logs)
    _arrow(d, 295, H - 31, 360, H - 52)      # prometheus -> grafana
    _arrow(d, 295, H - 95, 360, H - 62)      # loki -> grafana
    _arrow(d, 235, H - 46, 235, H - 140)     # prometheus -> alertmanager
    _arrow(d, 295, H - 155, 360, H - 155)    # alertmanager -> slack
    d.add(String(118, H - 34, "métriques", fontSize=7, fillColor=GREY))
    d.add(String(118, H - 70, "logs", fontSize=7, fillColor=GREY))
    return d


def helm_diagram():
    W, H = CONTENT_W, 200
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=8, ry=8, fillColor=LIGHT2, strokeColor=BLUE, strokeWidth=1.1))
    d.add(String(14, H - 20, "Chart Helm « audioprothese »", fontSize=11,
                 fillColor=NAVY, fontName="Helvetica-Bold"))
    objs = ["Deployment backend", "Deployment frontend", "Service", "Ingress",
            "Secret (DB)", "HorizontalPodAutoscaler", "ServiceMonitor", "NetworkPolicy"]
    cols, cw, ch, gx, gy = 2, (W - 60) / 2, 30, 20, 14
    x0, y0 = 24, H - 60
    for i, o in enumerate(objs):
        r, c = divmod(i, cols)
        _dbox(d, x0 + c * (cw + gx), y0 - r * (ch + gy), cw, ch, o, BLUE, fs=9)
    return d


def layered_stack(layers, colors_list=None, box_h=34, gap=7):
    """Empilement de couches (architecture applicative en couches)."""
    n = len(layers)
    if colors_list is None:
        colors_list = [BLUE, ACCENT, BLUE, GREY, NAVY][:n] + [BLUE] * max(0, n - 5)
    H = n * box_h + (n - 1) * gap + 6
    d = Drawing(CONTENT_W, H)
    y = H - box_h
    for i, lay in enumerate(layers):
        _dbox(d, 0, y, CONTENT_W, box_h, lay, colors_list[i], fs=9.3)
        y -= box_h + gap
    return d


def fan_out(source, targets, lcolor=ACCENT, rcolor=BLUE, box_h=30, gap=12):
    """Une source (gauche) reliée par des flèches à plusieurs cibles (droite)."""
    n = len(targets)
    H = max(n * box_h + (n - 1) * gap + 6, 70)
    d = Drawing(CONTENT_W, H)
    lw = CONTENT_W * 0.30
    rw = CONTENT_W * 0.44
    rx = CONTENT_W - rw
    _dbox(d, 0, H / 2 - 28, lw, 56, source, lcolor, fs=9.3)
    y = H - box_h
    for t in targets:
        _dbox(d, rx, y, rw, box_h, t, rcolor, fs=8.8)
        _arrow(d, lw, H / 2, rx, y + box_h / 2, color=GREY)
        y -= box_h + gap
    return d


def network_topology():
    """Deux réseaux isolés : VNet Azure (cloud) et VNet on-premise, sans peering."""
    W, H = CONTENT_W, 210
    d = Drawing(W, H)
    # ------ VNet cloud (gauche)
    lx, lw = 0, W * 0.52
    d.add(Rect(lx, 10, lw, H - 30, rx=8, ry=8, fillColor=LIGHT2,
               strokeColor=BLUE, strokeWidth=1.2))
    d.add(String(lx + 12, H - 20, "VNet Azure  10.10.0.0/16  —  Cluster AKS",
                 fontSize=9.5, fillColor=NAVY, fontName="Helvetica-Bold"))
    _dbox(d, lx + 18, H - 95, lw - 36, 30, "Subnet nœuds AKS  (pods app · ingress)", BLUE, fs=8.2)
    _dbox(d, lx + 18, H - 140, lw - 36, 30, "PostgreSQL Flexible  (pare-feu · TLS)", GREY, fs=8.2)
    _dbox(d, lx + 18, 24, lw - 36, 28, "Ingress NGINX — entrée publique unique", NAVY, fs=8.2)
    # ------ VNet on-premise (droite)
    rw = W * 0.40
    rx = W - rw
    d.add(Rect(rx, 42, rw, H - 92, rx=8, ry=8, fillColor=colors.HexColor("#f3ece2"),
               strokeColor=ACCENT, strokeWidth=1.2))
    d.add(String(rx + 12, H - 60, "VNet on-premise  10.20.0.0/16",
                 fontSize=9.5, fillColor=NAVY, fontName="Helvetica-Bold"))
    _dbox(d, rx + 16, H - 112, rw - 32, 30, "VM Linux (site distant simulé)", ACCENT, fs=8.2)
    _dbox(d, rx + 16, H - 157, rw - 32, 30, "MinIO — objet chiffré (SSE)", ACCENT, fs=8.2)
    # ------ séparation + flux de sauvegarde
    midx = (lx + lw + rx) / 2
    d.add(Line(midx, 24, midx, H - 30, strokeColor=GREY, strokeWidth=1,
               strokeDashArray=[4, 3]))
    _arrow(d, lx + lw - 18, H - 125, rx + 18, H - 142, color=GREY)
    d.add(String(midx, H - 118, "backup chiffré", fontSize=7, fillColor=GREY,
                 textAnchor="middle"))
    d.add(String(midx, 12, "réseaux isolés — aucun peering", fontSize=7,
                 fillColor=GREY, textAnchor="middle"))
    return d


# ----------------------------------------------------------------- assemblage
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d6e0ea"))
    canvas.line(2 * cm, 1.3 * cm, A4[0] - 2 * cm, 1.3 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(2 * cm, 1 * cm, "Projet d'étude M2 DevOps — Cabinet d'audioprothèse — %s" % PERIODE)
    canvas.drawRightString(A4[0] - 2 * cm, 1 * cm, "Page %d" % doc.page)
    canvas.restoreState()


def build(filename, story):
    SimpleDocTemplate(os.path.join(OUT, filename), pagesize=A4,
                      topMargin=1.7 * cm, bottomMargin=1.8 * cm,
                      leftMargin=2 * cm, rightMargin=2 * cm,
                      title=filename.replace(".pdf", "")
                      ).build(story, onFirstPage=footer, onLaterPages=footer)
    print("OK", filename)


def cover(title, subtitle, infos_rows):
    s = [Spacer(1, 0.4 * cm), Banner(title, subtitle), Spacer(1, 0.9 * cm)]
    s.append(wrap_table(infos_rows, [4.3 * cm, CONTENT_W - 4.3 * cm], header=False, zebra=True))
    s.append(Spacer(1, 0.6 * cm))
    s.append(P("SUP DE VINCI — Expert en Systèmes d'Information — Mastère DevOps — "
               "Classe <b>%s</b> — Promotion 2025-2026. Document réalisé dans le cadre du "
               "projet d'étude de fin d'année." % CLASSE, NOTE))
    s.append(PageBreak())
    return s
