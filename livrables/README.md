# Livrables PDF — Projet d'étude M2 DevOps (classe M2 DO C)

Générés avec **reportlab** :
- `generate_docs.py` : mise en page (bandeaux, styles, schéma d'archi, Gantt).
- `content_docs.py` : contenu groupe + fonction `individual()`.
- `individuals_content.py` / `individuals_content2.py` : contenu détaillé des rendus individuels.

## Fichiers
- `PE-2526_M2DOC_Mougammadou_Rjafellah_Nianghane_Douadi.pdf` — **rendu groupe** (8 p. : entreprise/équipe, problématique/solution + schéma, FinOps détaillé, organisation/Gantt, solution technique).
- `PE-2526_M2DOC_MougammadouZaafir.pdf` — individuel Zaafir (10 p.).
- `PE-2526_M2DOC_RjafellahElyess.pdf` — individuel Elyess (10 p.).
- `PE-2526_M2DOC_NianghaneAdame.pdf` — individuel Adame (10 p.).
- `PE-2526_M2DOC_DouadiAnis.pdf` — individuel Anis (10 p.).

## Régénérer
```bash
pip install reportlab
cd livrables
python3 content_docs.py            # génère le groupe
python3 individuals_content.py     # Zaafir + Elyess
python3 individuals_content2.py    # Adame + Anis
```

## À rendre
Zipper : `PE_2526_M2DOC_Mougammadou_Rjafellah_Nianghane_Douadi.zip` (contenant le PDF groupe + les 4 PDF individuels).
