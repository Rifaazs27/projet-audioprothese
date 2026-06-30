# -*- coding: utf-8 -*-
"""Génère le PDF groupe + 4 PDF individuels du Projet d'étude M2 DevOps."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, ListFlowable, ListItem, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

OUT = "/home/user/projet-audioprothese/livrables"
os.makedirs(OUT, exist_ok=True)

CODE = "CODEPROMO"  # <- à remplacer par votre code promo réel
NAVY = colors.HexColor("#1f4e79")
BLUE = colors.HexColor("#2e75b6")
LIGHT = colors.HexColor("#dbe5f1")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=NAVY, fontSize=16, spaceBefore=14, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=BLUE, fontSize=12.5, spaceBefore=10, spaceAfter=5)
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontSize=10.3, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
SMALL = ParagraphStyle("SMALL", parent=BODY, fontSize=9, textColor=colors.HexColor("#555555"))
TITLE = ParagraphStyle("TITLE", parent=ss["Title"], textColor=NAVY, fontSize=24, leading=28)
SUBTITLE = ParagraphStyle("SUBTITLE", parent=ss["Title"], textColor=BLUE, fontSize=14, leading=18)
CENTER = ParagraphStyle("CENTER", parent=BODY, alignment=TA_CENTER)


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(t, BODY), leftIndent=10, value="•") for t in items],
        bulletType="bullet", start="•", leftIndent=14, bulletColor=BLUE,
    )


def table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#aab7c4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), NAVY),
                  ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                  ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                  ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT])]
    t.setStyle(TableStyle(style))
    return t


def P(t):
    return Paragraph(t, BODY)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawString(2 * cm, 1 * cm, "Projet d'étude M2 DevOps 2025-2026 — Cabinet d'audioprothèse")
    canvas.drawRightString(19 * cm, 1 * cm, "Page %d" % doc.page)
    canvas.restoreState()


def build(filename, story):
    doc = SimpleDocTemplate(os.path.join(OUT, filename), pagesize=A4,
                            topMargin=2 * cm, bottomMargin=2 * cm,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            title=filename)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("OK", filename)


MEMBERS = ["Zaafir Mougammadou Zaccaria", "Elyess Rjafellah",
           "Adame Nianghane", "Anis Douadi"]


def cover(title_lines, subtitle, extra=None):
    s = [Spacer(1, 3 * cm),
         Paragraph("Projet d'étude — Mastère DevOps", SUBTITLE),
         Spacer(1, 0.4 * cm)]
    for tl in title_lines:
        s.append(Paragraph(tl, TITLE))
    s.append(Spacer(1, 0.8 * cm))
    s.append(Paragraph(subtitle, SUBTITLE))
    s.append(Spacer(1, 1.5 * cm))
    if extra:
        s.append(extra)
    s.append(Spacer(1, 1 * cm))
    s.append(Paragraph("SUP DE VINCI — Promotion 2025-2026", CENTER))
    s.append(Paragraph("Code promo : <b>%s</b> (à compléter)" % CODE, CENTER))
    s.append(PageBreak())
    return s
