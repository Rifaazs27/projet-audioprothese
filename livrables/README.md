# Livrables PDF — Projet d'étude M2 DevOps

Générés avec `generate_docs.py` (mise en page) + `content_docs.py` (contenu) via **reportlab**.

- `PE-2526_CODEPROMO_Mougammadou_Rjafellah_Nianghane_Douadi.pdf` — **rendu groupe** (6 p., schéma d'architecture + Gantt Jan→Juin 2026)
- `PE-2526_CODEPROMO_<NomPrenom>.pdf` — **rendus individuels** (3 p. chacun)

## Avant de rendre
1. Remplacer `CODEPROMO` par votre code promo réel :
   - dans les **noms de fichiers**,
   - dans `generate_docs.py` (variable `CODE`).
2. Régénérer :
   ```bash
   pip install reportlab
   cd livrables && python3 content_docs.py
   ```
3. Zipper : `PE_2526_CODEPROMO_Mougammadou_Rjafellah_Nianghane_Douadi.zip`.

Contenu rédigé en paragraphes, conforme au cadre pédagogique (groupe :
entreprise/équipe, problématique/solution, coûts FinOps M2, organisation/
planning, solution technique ; individuels : contribution, perspectives,
limites, annexes + analyse personnelle).
