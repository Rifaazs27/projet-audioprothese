# Planning & diagramme de Gantt

Projet sur ~6 mois (kick-off → vidéo MVP + rendu technique final), en sprints
de 2 semaines.

```mermaid
gantt
    title Projet d'étude M2 DevOps — Audioprothèse
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%y

    section Cadrage
    Kick-off & constitution équipe      :done,    k1, 2026-01-06, 7d
    Analyse du besoin & backlog         :done,    k2, after k1, 14d
    Choix d'architecture & FinOps       :done,    k3, after k2, 10d

    section Développement
    Backend FastAPI + tests             :done,    d1, 2026-02-09, 21d
    Frontend React                      :done,    d2, after d1, 14d
    Conteneurisation (Docker/compose)   :done,    d3, after d1, 10d

    section Infrastructure & CI/CD
    Terraform Azure (AKS, DB, KV, ACR)  :done,    i1, 2026-03-09, 18d
    Helm chart + RBAC + network policies:done,    i2, after i1, 12d
    Pipelines GitHub Actions            :done,    i3, 2026-03-16, 18d

    section Observabilité & Sécurité
    Monitoring (Prometheus/Grafana/Loki):done,    o1, 2026-04-13, 14d
    DevSecOps (Trivy/CodeQL/Gitleaks)   :done,    o2, after i3, 12d
    TLS, secrets CI, durcissement       :done,    o3, after o1, 10d

    section Finalisation
    PRA/PCA & runbooks                  :active,  f1, 2026-05-11, 10d
    Documentation complète              :active,  f2, 2026-05-11, 18d
    Répétitions & vidéo MVP             :         f3, 2026-06-08, 14d
    Rendus finaux (zip, pdf, vidéo)     :         f4, after f3, 7d
```

## Jalons

| Jalon | Échéance | Livrable |
|---|---|---|
| M1 — Cadrage validé | Kick-off + 1 mois | Backlog, architecture, choix FinOps |
| M2 — MVP applicatif | + 3 mois | App conteneurisée + tests verts |
| M3 — Déploiement cloud | + 4,5 mois | Infra Terraform + CI/CD + monitoring |
| M4 — Vidéo MVP | + 6 mois | Vidéo 15-20 min (démo en production) |
| M5 — Rendu technique final | + 6 mois | Dépôt + docs + dashboards + analyse |

> Les dates sont indicatives (cf. cahier pédagogique : « toutes les dates sont
> indicatives »). À adapter au calendrier réel du campus.
