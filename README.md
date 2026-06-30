# Projet d'étude M2 DevOps — Plateforme de gestion de cabinet d'audioprothèse

> MVP DevOps complet : application conteneurisée, infrastructure as code Azure,
> CI/CD, supervision, sécurité (DevSecOps) et maîtrise des coûts (FinOps).

[![CI](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/ci.yml/badge.svg)](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/ci.yml)
[![DevSecOps](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/security.yml/badge.svg)](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/security.yml)

## 1. Le besoin

Un cabinet d'audioprothèse doit gérer ses **patients**, leurs **appareils
auditifs** et les **rendez-vous** de suivi. Au-delà de l'application, le projet
démontre une **chaîne DevOps de bout en bout** : du commit du développeur
jusqu'au déploiement supervisé en production sur le cloud, de façon
automatisée, sécurisée et économe.

## 2. La solution en un coup d'œil

```
Développeur ──push──▶ GitHub ──▶ GitHub Actions (CI)
                                   ├─ lint + tests (back & front)
                                   ├─ scan sécurité (Trivy, CodeQL, Gitleaks)
                                   ├─ build images Docker ──▶ Azure ACR
                                   └─ déploiement Helm ──▶ AKS (Kubernetes)
                                                            │
   Patients/RDV ◀── Ingress NGINX + TLS ◀── Frontend React │
                                              Backend FastAPI ──▶ PostgreSQL Flexible
                                                            │
   Supervision : Prometheus + Grafana + Loki  ◀────────────┘
   Secrets     : Azure Key Vault
   Garde-fou   : budget FinOps + alertes e-mail
```

Architecture détaillée et diagrammes : [`docs/architecture.md`](docs/architecture.md).

## 3. Stack technique

| Domaine | Technologie |
|---|---|
| Backend | Python 3.11 · FastAPI · SQLAlchemy 2 · Pydantic |
| Frontend | React 18 · Vite |
| Base de données | PostgreSQL 16 (Azure Flexible Server) |
| Conteneurs | Docker (images multi-stage, non-root) |
| Orchestration | Kubernetes (AKS) · Helm |
| IaC | Terraform (provider azurerm) |
| CI/CD | GitHub Actions |
| Supervision | Prometheus · Grafana · Loki |
| Sécurité | Trivy · CodeQL · Gitleaks · Azure Key Vault · RBAC · Network Policies · TLS |
| FinOps | Azure Budget + alertes, dimensionnement minimal, scripts de teardown |

## 4. Démarrage rapide (local)

Prérequis : Docker + Docker Compose.

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:8080 |
| API (Swagger) | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin / admin) |

Peupler des données de démonstration :

```bash
docker compose exec backend python -m app.seed
```

Lancer les tests :

```bash
# Backend
cd app/backend && pip install -r requirements-dev.txt && pytest && ruff check .
# Frontend
cd app/frontend && npm install && npm run test && npm run build
```

## 5. Déploiement sur Azure

Voir le guide pas à pas : [`docs/installation.md`](docs/installation.md).
En résumé (poste équipé de `az`, `terraform`, `kubectl`, `helm`) :

```bash
az login
./scripts/deploy.sh        # provisionne l'infra + déploie l'application
# ... démonstration ...
./scripts/teardown.sh      # FinOps : détruit tout pour stopper la facturation
```

## 6. Structure du dépôt

```
app/backend        API FastAPI (+ tests, Dockerfile, métriques)
app/frontend       SPA React (+ tests, Dockerfile nginx)
infra/terraform    Infrastructure Azure as code (AKS, ACR, PostgreSQL, Key Vault, budget)
k8s/helm           Chart Helm de l'application (RBAC, network policies, ingress TLS, HPA)
monitoring         Configs Prometheus / Grafana / Loki (local + cluster)
.github/workflows  Pipelines CI/CD et DevSecOps
scripts            Déploiement, teardown FinOps, seed
docs               Documentation complète (voir ci-dessous)
```

## 7. Documentation

| Document | Contenu |
|---|---|
| [architecture.md](docs/architecture.md) | Architecture, diagrammes, workflow CI/CD |
| [installation.md](docs/installation.md) | Déploiement Azure pas à pas |
| [securite-devsecops.md](docs/securite-devsecops.md) | Sécurité de la chaîne (secrets, RBAC, TLS, scans) |
| [monitoring.md](docs/monitoring.md) | Supervision, dashboards, alertes |
| [finops-gestion-couts.md](docs/finops-gestion-couts.md) | Estimation et maîtrise des coûts (M2) |
| [pra-pca.md](docs/pra-pca.md) | Plan de reprise / continuité d'activité |
| [backlog.md](docs/backlog.md) | Backlog produit et technique |
| [planning-gantt.md](docs/planning-gantt.md) | Planning et diagramme de Gantt |
| [contributions.md](docs/contributions.md) | Contributions individuelles |
| [runbooks.md](docs/runbooks.md) | Procédures d'exploitation |
| [livrables.md](docs/livrables.md) | Correspondance livrables ↔ cahier des charges |

## 8. Conformité au cahier des charges

Le projet couvre les attendus du Mastère DevOps (M2) : infrastructure cloud,
IaC, CI/CD, conteneurs, orchestration Kubernetes, supervision/observabilité,
DevSecOps, FinOps, PRA/PCA et documentation complète. La table de correspondance
détaillée se trouve dans [`docs/livrables.md`](docs/livrables.md).
