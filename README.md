# 🩺 Plateforme de gestion d'un cabinet d'audioprothèse

> **MVP DevOps de bout en bout** : application web conteneurisée, infrastructure
> as code sur Azure, CI/CD automatisée, supervision, sécurité (DevSecOps),
> architecture hybride (cloud + on-premise), plan de reprise d'activité et
> maîtrise des coûts (FinOps).

[![CI](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/ci.yml/badge.svg)](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/ci.yml)
[![DevSecOps](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/security.yml/badge.svg)](https://github.com/rifaazs27/projet-audioprothese/actions/workflows/security.yml)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Orchestration-AKS%20%2F%20Helm-326CE5?logo=kubernetes&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Azure](https://img.shields.io/badge/Cloud-Microsoft%20Azure-0078D4?logo=microsoftazure&logoColor=white)

Projet d'étude — **Mastère 2 DevOps (classe M2 DO C)** · SUP DE VINCI · 2025-2026.

---

## Sommaire

1. [Contexte & problématique](#1-contexte--problématique)
2. [Fonctionnalités](#2-fonctionnalités)
3. [Architecture](#3-architecture)
4. [Stack technique](#4-stack-technique)
5. [Démarrage rapide (local)](#5-démarrage-rapide-local)
6. [Déploiement sur Azure (CI/CD)](#6-déploiement-sur-azure-cicd)
7. [Chaîne CI/CD](#7-chaîne-cicd)
8. [Observabilité](#8-observabilité)
9. [Sécurité (DevSecOps)](#9-sécurité-devsecops)
10. [Sauvegarde & plan de reprise (PRA)](#10-sauvegarde--plan-de-reprise-pra)
11. [FinOps — maîtrise des coûts](#11-finops--maîtrise-des-coûts)
12. [API](#12-api)
13. [Tests](#13-tests)
14. [Structure du dépôt](#14-structure-du-dépôt)
15. [Documentation](#15-documentation)
16. [Équipe](#16-équipe)

---

## 1. Contexte & problématique

Le cabinet d'audioprothèse **AudioPro** accompagne ses patients tout au long de
leur appareillage. Son activité repose sur le suivi de données **sensibles** :
le dossier de chaque **patient**, les **appareils auditifs** qui lui sont posés
et les **rendez-vous** de contrôle.

Ces données étant des **données de santé**, la solution doit garantir :

- la **confidentialité** et la **traçabilité** (contexte RGPD) ;
- une **haute disponibilité** et une capacité d'**auto-rétablissement** ;
- une **reproductibilité** totale (tout est décrit en code) ;
- une **sobriété budgétaire** (compte Azure for Students plafonné à **85 $**).

Au-delà de l'application, le projet démontre une **chaîne DevOps complète**, du
commit du développeur jusqu'au déploiement supervisé en production.

## 2. Fonctionnalités

- 👤 **Gestion des patients** — créer, consulter, mettre à jour, supprimer.
- 🦻 **Enregistrement des appareils auditifs** — marque, modèle, n° de série,
  oreille appareillée, date de pose, rattachés à un patient.
- 📅 **Prise de rendez-vous** — date, heure, motif, statut, avec une vue des
  **rendez-vous à venir**.
- 📖 **API documentée** automatiquement (OpenAPI / Swagger) pour l'intégration.
- ❤️ **Sondes de santé** (`/healthz`, `/readyz`) et **métriques** (`/metrics`).

## 3. Architecture

Architecture **hybride** : le cloud héberge l'application, un site **on-premise**
(réseau séparé) accueille les sauvegardes chiffrées.

```
  Développeur ──push main──▶ GitHub Actions (CI + déploiement automatisé)
                               ├─ lint + tests (back & front)
                               ├─ scan sécurité (Trivy · CodeQL · Gitleaks)
                               ├─ az login → Terraform apply (infra Azure)
                               ├─ build images Docker ──▶ Azure ACR
                               └─ déploiement Helm ──────▶ AKS (Kubernetes)
                                                            │
   Utilisateurs ─▶ Ingress NGINX ─┬─▶ Frontend React       │
                                  └─▶ Backend FastAPI ──TLS──▶ PostgreSQL Flexible
                                          │
                     Prometheus · Grafana · Loki · Alertmanager (supervision)
                                          │
   Site on-premise (VNet séparé) ◀──backup chiffré── MinIO (SSE) · Ansible
```

> **Déploiement 100 % piloté par la CI** : un `push` sur `main` (ou un
> déclenchement manuel) provisionne l'infrastructure Azure **et** déploie
> l'application, sans aucune étape manuelle. Les secrets sont stockés dans
> **GitHub Actions Secrets** (pas de coffre managé, choix FinOps assumé).

Détail et diagrammes : [`docs/architecture.md`](docs/architecture.md).

## 4. Stack technique

| Domaine | Technologies |
|---|---|
| **Backend** | Python 3.11 · FastAPI · SQLAlchemy 2 · Pydantic |
| **Frontend** | React 18 · Vite (servi par nginx) |
| **Base de données** | PostgreSQL 16 — Azure Flexible Server (TLS) |
| **Conteneurs** | Docker (images multi-stage, non-root) |
| **Orchestration** | Kubernetes (Azure AKS) · Helm |
| **IaC / Config** | Terraform (provisionnement) · Ansible (on-prem, MinIO, backup) |
| **On-premise (hybride)** | VM Linux dans un VNet séparé · MinIO chiffré (SSE) |
| **CI/CD** | GitHub Actions (provisionnement + déploiement automatisés) |
| **Observabilité** | Prometheus · Grafana · Loki · Alertmanager → Slack/Teams |
| **Sécurité** | Trivy · CodeQL · Gitleaks · RBAC · NetworkPolicies · TLS · secrets chiffrés |
| **FinOps** | Région Poland Central · nœuds burstable B2s_v2 · Azure Budget + alertes · teardown à la demande |

## 5. Démarrage rapide (local)

**Prérequis :** Docker + Docker Compose.

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

## 6. Déploiement sur Azure (CI/CD)

1. **Renseigner 5 secrets GitHub** (une seule fois) — *Settings ▸ Secrets and
   variables ▸ Actions* :
   `AZURE_USERNAME`, `AZURE_PASSWORD`, `AZURE_TENANT_ID`,
   `AZURE_SUBSCRIPTION_ID`, `BUDGET_EMAIL` (+ `SLACK_WEBHOOK_URL` optionnel).
2. **Lancer le déploiement** — *Actions ▸ Deploy ▸ Run workflow ▸ `deploy`*
   (ou un `push` sur `main`). La chaîne provisionne l'infra, build/push les
   images et déploie l'application.
3. L'**URL publique** (IP de l'Ingress) s'affiche à la fin du job.
4. **Après la démo** — *Actions ▸ Deploy ▸ `destroy`* pour stopper la
   facturation (reconstruction à l'identique en ~12-14 min).

Guide pas à pas : [`docs/installation.md`](docs/installation.md).

## 7. Chaîne CI/CD

| Workflow | Déclencheur | Rôle |
|---|---|---|
| **Deploy** | push `main` · manuel | Terraform apply → build/push images → scan → déploiement Helm → MinIO |
| **CI** | push · pull request | Analyse statique + tests backend & frontend |
| **DevSecOps** | push `main` · PR · hebdo | Scans Trivy, CodeQL, Gitleaks (SARIF) |
| **Backup** | quotidien · manuel | Sauvegarde chiffrée / restauration (PRA) |

Le pipeline **Deploy** est **auto-réparant** : libération d'un verrou d'état
résiduel, nettoyage d'une release Helm bloquée, ordonnancement des dépendances.

## 8. Observabilité

- **Prometheus** collecte les métriques exposées par l'application (débit,
  latence, erreurs), découvertes automatiquement via un `ServiceMonitor`.
- **Grafana** présente un tableau de bord importé automatiquement (les
  « signaux dorés » d'un service) — exposé via l'Ingress (`grafana.<IP>.nip.io`).
- **Loki** centralise les journaux structurés, corrélables dans Grafana.
- **Alertmanager** route les alertes (indisponibilité, taux d'erreurs, latence)
  vers une messagerie d'équipe (Slack/Teams).

Détail : [`docs/monitoring.md`](docs/monitoring.md).

## 9. Sécurité (DevSecOps)

- **Analyse à chaque livraison** — Trivy (images & dépendances, **bloquant** si
  vulnérabilité critique), CodeQL (code), Gitleaks (fuite de secrets). Résultats
  publiés au format **SARIF** dans l'onglet *Security*.
- **Durcissement de l'exécution** — conteneurs **non-root**, capacités retirées,
  **RBAC** (moindre privilège), **NetworkPolicies** de cloisonnement.
- **Chiffrement** — TLS obligatoire vers PostgreSQL, sauvegardes chiffrées
  au repos (MinIO SSE).
- **Secrets** — jamais en clair dans le dépôt : stockés chiffrés dans GitHub,
  injectés en tant que *Secret* Kubernetes au déploiement.

Détail : [`docs/securite-devsecops.md`](docs/securite-devsecops.md).

## 10. Sauvegarde & plan de reprise (PRA)

- Sauvegardes **chiffrées** de la base répliquées vers **MinIO** sur le site
  on-premise (réseau séparé), pilotées par **Ansible**.
- **Restauration idempotente** (rejouable même sur une base peuplée).
- Objectifs : **RPO ≤ 24 h** · **RTO ≈ 15 min**.
- Cycle **validé en conditions réelles** : donnée créée → sauvegardée →
  supprimée → restaurée à l'identique.

Détail : [`docs/pra-pca.md`](docs/pra-pca.md).

## 11. FinOps — maîtrise des coûts

- **Rightsizing** : plan de contrôle AKS gratuit, nœuds burstable, base au
  palier le plus bas.
- **Outils sobres** : Loki plutôt qu'ELK, secrets GitHub plutôt qu'un coffre.
- **Budget Azure + alertes** à 50 / 80 / 100 %.
- **Destruction à la demande** : dépense réelle **≈ 10-20 $** sur le semestre
  (au lieu de ~650 $ en fonctionnement continu).

Détail : [`docs/finops-gestion-couts.md`](docs/finops-gestion-couts.md).

## 12. API

Base : `"/api"` (mutualisée derrière l'Ingress).

| Méthode & route | Rôle |
|---|---|
| `GET` / `POST` `/api/patients` | Lister / créer des patients |
| `GET` / `PATCH` / `DELETE` `/api/patients/{id}` | Consulter / modifier / supprimer un patient |
| `POST` `/api/patients/{id}/appareils` | Enregistrer un appareil auditif |
| `POST` `/api/patients/{id}/rendez-vous` | Planifier un rendez-vous |
| `GET` `/api/rendez-vous` | Lister l'ensemble des rendez-vous |
| `GET` `/healthz` · `/readyz` | Sondes de vivacité / disponibilité |
| `GET` `/metrics` · `/api/docs` | Métriques Prometheus · documentation OpenAPI |

## 13. Tests

```bash
# Backend — tests + lint
cd app/backend && pip install -r requirements-dev.txt && pytest && ruff check .

# Frontend — tests + build
cd app/frontend && npm install && npm run test && npm run build
```

Les tests s'exécutent aussi automatiquement à chaque *push* / *pull request*
via le workflow **CI**.

## 14. Structure du dépôt

```
app/backend        API FastAPI (modèles, CRUD, tests, Dockerfile, métriques)
app/frontend       SPA React (tests, Dockerfile nginx)
infra/terraform    Infrastructure Azure as code (AKS, ACR, PostgreSQL, VM on-prem, budget)
ansible            Playbooks on-premise : MinIO chiffré + backup/restore PostgreSQL
k8s/helm           Chart Helm de l'application (Ingress, Secret, HPA, ServiceMonitor, NetworkPolicy)
monitoring         Configs Prometheus / Grafana / Loki / Alertmanager
.github/workflows  Pipelines CI/CD et DevSecOps
scripts            Déploiement, teardown FinOps, seed
docs               Documentation technique complète
```

## 15. Documentation

| Document | Contenu |
|---|---|
| [architecture.md](docs/architecture.md) | Architecture, diagrammes, workflow CI/CD |
| [installation.md](docs/installation.md) | Déploiement Azure pas à pas |
| [securite-devsecops.md](docs/securite-devsecops.md) | Sécurité de la chaîne |
| [monitoring.md](docs/monitoring.md) | Supervision, dashboards, alertes |
| [finops-gestion-couts.md](docs/finops-gestion-couts.md) | Estimation et maîtrise des coûts |
| [pra-pca.md](docs/pra-pca.md) | Plan de reprise / continuité d'activité |
| [backlog.md](docs/backlog.md) | Backlog produit et technique |
| [planning-gantt.md](docs/planning-gantt.md) | Planning et diagramme de Gantt |
| [contributions.md](docs/contributions.md) | Contributions individuelles |
| [runbooks.md](docs/runbooks.md) | Procédures d'exploitation |
| [demo-runbook.md](docs/demo-runbook.md) · [demo-checklist.md](docs/demo-checklist.md) | Démonstration de bout en bout |
| [validation-conformite.md](docs/validation-conformite.md) | Tests par exigence + matrice de conformité |

## 16. Équipe

Classe **M2 DO C** — Promotion 2025-2026.

| Membre | Périmètre principal |
|---|---|
| **Zaafir Mougammadou Zaccaria** | Infrastructure (Terraform) & application, déploiement |
| **Elyess Rjafellah** | CI/CD & automatisation |
| **Adame Nianghane** | Observabilité & sécurité (DevSecOps) |
| **Anis Douadi** | Kubernetes/Helm & reprise d'activité (PRA) |
