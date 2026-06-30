# Correspondance livrables ↔ cahier des charges

Ce document met en regard les exigences du cadre pédagogique M2 DevOps et leur
réalisation dans le dépôt.

## 1. Attendus techniques (livrable final)

| Exigence (cahier des charges) | Réalisation | Emplacement |
|---|---|---|
| Code source versionné | Dépôt Git structuré | tout le dépôt |
| Architecture cloud | AKS + ACR + PostgreSQL Flexible | `infra/terraform`, `docs/architecture.md` |
| Infra-as-Code (Terraform/Ansible) | Terraform azurerm | `infra/terraform` |
| Conteneurs | Dockerfiles multi-stage non-root | `app/*/Dockerfile` |
| Orchestration Kubernetes | Chart Helm (Deployments, Ingress, HPA) | `k8s/helm` |
| Fichiers de config (docker-compose, YAML K8s, scripts CI/CD) | Compose + Helm + Workflows | `docker-compose.yml`, `k8s/`, `.github/workflows` |
| CI/CD | GitHub Actions (build/test/scan/deploy) | `.github/workflows` |
| Scan de vulnérabilités (Trivy/Clair) | Trivy (fs + image) + CodeQL + Gitleaks | `.github/workflows/security.yml`, `deploy.yml` |
| Sécurité (secrets, RBAC, TLS, RGPD) | GitHub Secrets, RBAC, NetworkPolicies, TLS, région UE | `docs/securite-devsecops.md` |
| Supervision : métriques | Prometheus + Grafana | `monitoring/`, `docs/monitoring.md` |
| Supervision : logs | Loki + Promtail | `monitoring/`, `docs/monitoring.md` |
| Dashboard (screenshot) | Dashboard Grafana provisionné | `monitoring/grafana/dashboards` |
| Alertes (Slack/Teams) | Règles Prometheus + Alertmanager | `monitoring/prometheus/alerts.yml` |
| PRA/PCA & runbooks | Sauvegardes, rollback, reconstruction | `docs/pra-pca.md`, `docs/runbooks.md` |
| Gestion des coûts (M2 / FinOps) | Estimation, leviers, budget + alertes | `docs/finops-gestion-couts.md` |
| Backlog | Backlog produit & technique | `docs/backlog.md` |
| Diagramme de Gantt | Planning Mermaid | `docs/planning-gantt.md` |
| Justification des choix | Tableau de décisions | `docs/architecture.md` §4 |
| Contributions individuelles | Modèle à compléter | `docs/contributions.md` |
| Documentation installation/exploitation | Guides | `docs/installation.md`, `docs/runbooks.md` |

## 2. Cours M2 couverts

| Cours M2 | Couverture |
|---|---|
| DevSecOps | Trivy, CodeQL, Gitleaks, durcissement, secrets |
| Azure / Architecture as a Service | AKS, ACR, PostgreSQL Flexible, Storage |
| Gestion des configurations | Helm, Terraform, GitOps-ready |
| CI/CD | GitHub Actions (CI + CD + infra) |
| FinOps | `docs/finops-gestion-couts.md` |
| Monitoring & Microservice / Load Balancing | Prometheus/Grafana/Loki, Ingress, HPA |

## 3. Livrables de rendu (à produire par l'équipe)

> Ces éléments ne sont pas du code mais des rendus administratifs ; ils
> suivent la nomenclature du cadre pédagogique.

### Vidéo MVP (15-20 min)
- Plan : entreprise/équipe → problématique/solution → organisation/méthodo →
  solution technique → **démo en production** (pipeline, logs, sécurité,
  redéploiement à chaud).
- Prise de parole de chaque membre, nom affiché.
- Nomenclature : `PE-2526_<codepromo>_NomPrenom.mp4`
  (ou fichier `.txt` avec lien YouTube non répertorié).
- Zip : `PE_2526_<codepromo>_nom1_nom2_...zip`

### Document technique final (PDF)
- Rendu **groupe** : entreprise/équipe, problématique/solution, **gestion des
  coûts (M2)**, organisation/planification, solution technique.
- Rendu **individuel** : perspectives d'évolution, analyse critique des limites,
  annexes (doc utilisateur, analyse personnelle, défis, forces/faiblesses,
  compétences, axes d'amélioration).
- Nomenclature groupe : `PE-2526_<codepromo>_nom1_nom2_....pdf`
- Nomenclature individuelle : `PE-2526_<codepromo>_NomPrenom.pdf`

> Une grande partie du contenu PDF peut être directement reprise des documents
> de `docs/` (architecture, FinOps, sécurité, monitoring, PRA/PCA).
