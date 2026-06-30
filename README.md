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
Développeur ──push main──▶ GitHub Actions (CI + déploiement automatisé)
                             ├─ lint + tests (back & front)
                             ├─ scan sécurité (Trivy, CodeQL, Gitleaks)
                             ├─ az login (user/pass) → Terraform apply
                             ├─ build images Docker ──▶ Azure ACR
                             └─ déploiement Helm ──▶ AKS (Kubernetes)
                                                      │
   Patients/RDV ◀── Ingress NGINX ◀── Frontend React │
                                        Backend FastAPI ──▶ PostgreSQL Flexible
                                                      │
   Garde-fou : budget FinOps + alertes e-mail ◀───────┘
```

> Déploiement **100 % piloté par la CI** : un `push` sur `main` provisionne
> l'infrastructure Azure et déploie l'application, sans aucune étape manuelle.
> Les secrets (identifiants Azure) sont stockés dans **GitHub Actions Secrets**.

Architecture détaillée et diagrammes : [`docs/architecture.md`](docs/architecture.md).

## 3. Stack technique

| Domaine | Technologie |
|---|---|
| Backend | Python 3.11 · FastAPI · SQLAlchemy 2 · Pydantic |
| Frontend | React 18 · Vite |
| Base de données | PostgreSQL 16 (Azure Flexible Server) |
| Conteneurs | Docker (images multi-stage, non-root) |
| Orchestration | Kubernetes (AKS) · Helm |
| IaC / Config | Terraform (provisioning) · Ansible (on-prem, MinIO, backup) |
| On-premise (hybride) | VM Linux dans un VNet séparé · MinIO chiffré |
| CI/CD | GitHub Actions (provision + déploiement automatisés) |
| Supervision | Prometheus · Grafana · Loki · Alertmanager → Slack/Teams |
| Sécurité | Trivy · CodeQL · Gitleaks · GitHub Secrets · RBAC · TLS PostgreSQL · conteneurs non-root |
| FinOps | Région Poland Central · 1 nœud B2s_v2 · Azure Budget + alertes · teardown |

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

## 5. Déploiement sur Azure (automatisé par la CI)

1. Renseigner 5 secrets GitHub (une seule fois) : `AZURE_USERNAME`,
   `AZURE_PASSWORD`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `BUDGET_EMAIL`.
2. **Pousser sur `main`** (ou lancer le workflow *Deploy* manuellement) : la CI
   provisionne l'infra Azure, build/push les images et déploie l'application.
3. L'URL d'accès (IP publique de l'Ingress) s'affiche à la fin du job.
4. **Après la démo** : lancer le workflow *Deploy* avec l'action `destroy`
   (ou `./scripts/teardown.sh`) pour stopper la facturation.

Guide détaillé (dont configuration des secrets) :
[`docs/installation.md`](docs/installation.md).

## 6. Structure du dépôt

```
app/backend        API FastAPI (+ tests, Dockerfile, métriques)
app/frontend       SPA React (+ tests, Dockerfile nginx)
infra/terraform    Infrastructure Azure as code (AKS, ACR, PostgreSQL, VM on-prem, budget)
ansible            Playbooks on-premise : MinIO chiffré + backup/restore PostgreSQL
k8s/helm           Chart Helm de l'application (RBAC, network policies, ingress TLS, HPA)
monitoring         Configs Prometheus / Grafana / Loki / Alertmanager (local + cluster)
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
