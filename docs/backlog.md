# Backlog produit & technique

Méthodologie **agile (Scrum/Kanban)**, sprints de 2 semaines. Priorisation
MoSCoW (Must / Should / Could / Won't).

## 1. Epics

| # | Epic | Objectif |
|---|---|---|
| E1 | Application métier | Gérer patients, appareils, rendez-vous |
| E2 | Conteneurisation | Images Docker reproductibles |
| E3 | Infrastructure as Code | Provisionner Azure via Terraform |
| E4 | CI/CD | Automatiser build, test, déploiement |
| E5 | Observabilité | Métriques, logs, dashboards, alertes |
| E6 | Sécurité / DevSecOps | Scans, secrets, RBAC, TLS |
| E7 | FinOps | Maîtriser et suivre les coûts |
| E8 | Documentation & livrables | Doc complète, démo, rendus |

## 2. User stories (extrait)

| ID | Story | Epic | Prio | État |
|---|---|---|---|---|
| US-01 | En tant qu'audioprothésiste, je crée/consulte/modifie/supprime un patient | E1 | Must | ✅ Fait |
| US-02 | J'enregistre les appareils auditifs d'un patient | E1 | Must | ✅ Fait |
| US-03 | Je planifie des rendez-vous de suivi | E1 | Must | ✅ Fait |
| US-04 | L'API expose des sondes de santé | E1 | Must | ✅ Fait |
| US-05 | Les services tournent en conteneurs non-root | E2 | Must | ✅ Fait |
| US-06 | `docker compose up` lance toute la stack locale | E2 | Must | ✅ Fait |
| US-07 | L'infra Azure est créée par Terraform | E3 | Must | ✅ Fait |
| US-08 | Un budget + alertes protègent le crédit | E3/E7 | Must | ✅ Fait |
| US-09 | La CI lint + teste à chaque push | E4 | Must | ✅ Fait |
| US-10 | La CD build, scanne et déploie sur AKS | E4 | Must | ✅ Fait |
| US-11 | Les métriques sont visibles dans Grafana | E5 | Must | ✅ Fait |
| US-12 | Les logs sont centralisés (Loki) | E5 | Should | ✅ Fait |
| US-13 | Des alertes se déclenchent en cas d'incident | E5 | Should | ✅ Fait |
| US-14 | Les images sont scannées (Trivy) avant déploiement | E6 | Must | ✅ Fait |
| US-15 | Les secrets sont dans Key Vault, pas dans Git | E6 | Must | ✅ Fait |
| US-16 | Trafic chiffré TLS de bout en bout | E6 | Must | ✅ Fait |
| US-17 | Network policies cloisonnent les pods | E6 | Should | ✅ Fait |
| US-18 | Documentation d'installation et d'exploitation | E8 | Must | ✅ Fait |

## 3. Backlog d'évolution (post-MVP)

| ID | Story | Prio |
|---|---|---|
| US-19 | Authentification / autorisation (OIDC, rôles utilisateurs) | Should |
| US-20 | Traçage distribué OpenTelemetry → Tempo/Jaeger | Could |
| US-21 | GitOps avec ArgoCD | Could |
| US-22 | Géo-réplication PostgreSQL + cluster multi-région (HA) | Won't (budget) |
| US-23 | Module facturation / tiers payant | Could |
| US-24 | Tests de charge (k6) et tests E2E (Playwright) | Should |
| US-25 | Notifications RDV (e-mail/SMS) | Could |

## 4. Definition of Done

- Code revu (PR) et tests verts en CI.
- Lint sans erreur (ruff, eslint).
- Scans sécurité sans vulnérabilité CRITICAL.
- Documentation mise à jour.
- Déployable via Helm sans étape manuelle.
