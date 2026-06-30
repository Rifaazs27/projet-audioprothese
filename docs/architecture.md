# Architecture

## 1. Vue d'ensemble

La solution adopte une architecture **cloud-native** déployée sur Azure,
orchestrée par Kubernetes (AKS), avec une chaîne CI/CD entièrement automatisée
et une supervision intégrée. Le dimensionnement est volontairement minimal pour
respecter le budget d'un compte Azure Student (85 $) tout en restant fidèle aux
exigences du cahier des charges (cloud, conteneurs, orchestration, monitoring,
sécurité, FinOps).

```mermaid
flowchart LR
    Dev[Développeur] -->|git push| GH[GitHub]
    GH --> CI[GitHub Actions CI/CD]
    CI -->|lint + tests| CI
    CI -->|scan Trivy / CodeQL / Gitleaks| SEC[(Rapports sécurité)]
    CI -->|build & push images| ACR[(Azure Container Registry)]
    CI -->|helm upgrade| AKS

    subgraph AZ[Azure - Poland Central]
      subgraph AKS[Cluster AKS Kubernetes]
        ING[Ingress NGINX] --> FE[Frontend React]
        ING --> BE[Backend FastAPI]
        PROM[Prometheus] -. scrape /metrics .-> BE
        GRAF[Grafana] --> PROM
        GRAF --> LOKI[Loki]
        LOKI -. logs .- BE
      end
      BE -->|TLS, firewall Azure| PG[(PostgreSQL Flexible)]
      ACR --> AKS
      BUD[Budget + alertes FinOps]
    end

    User[Utilisateur / Client] -->|HTTP / HTTPS| ING
```

## 2. Composants

### Application
- **Frontend React (Vite)** : interface de gestion des patients, servie par
  un nginx non-root. Routage `/api` assuré par l'Ingress.
- **Backend FastAPI** : API REST (patients, appareils, rendez-vous), expose
  `/healthz`, `/readyz` (sondes Kubernetes) et `/metrics` (Prometheus).
- **PostgreSQL Flexible Server** : base managée, accès **privé** via un
  sous-réseau délégué (aucune IP publique).

### Plateforme
- **AKS** : cluster Kubernetes managé (plan de contrôle gratuit, 1 nœud B2s).
- **Ingress NGINX** : point d'entrée HTTP/HTTPS unique.
- **cert-manager** : émission automatique des certificats TLS (Let's Encrypt).
- **Azure Container Registry** : stockage des images, accès via identité managée
  (AcrPull), sans secret stocké.
- **Secrets applicatifs** : la chaîne de connexion à la base est produite par
  Terraform et injectée par la CI dans un Secret Kubernetes (via Helm). Les
  identifiants Azure sont stockés dans **GitHub Actions Secrets**. (Choix MVP :
  pas d'Azure Key Vault, pour rester léger — cf. §4.)

### Observabilité
- **Prometheus** : collecte des métriques (débit, latence, erreurs, ressources).
- **Grafana** : visualisation (dashboard fourni) + exploration des logs.
- **Loki + Promtail** : centralisation des logs applicatifs JSON (alternative
  économe à la stack ELK — voir `docs/monitoring.md`).

## 3. Workflow CI/CD

```mermaid
sequenceDiagram
    participant Dev as Développeur
    participant GH as GitHub
    participant CI as GitHub Actions
    participant ACR as Azure ACR
    participant AKS as AKS

    Dev->>GH: push (feature branch) / PR
    GH->>CI: déclenche CI
    CI->>CI: lint (ruff, eslint)
    CI->>CI: tests (pytest, vitest)
    CI->>CI: helm lint + terraform validate
    CI->>CI: scan sécurité (Trivy, CodeQL, Gitleaks)
    Note over CI: PR validée puis fusionnée sur main
    Dev->>GH: tag v* / dispatch
    GH->>CI: déclenche CD
    CI->>ACR: build + push images
    CI->>CI: scan image (Trivy, bloquant si CRITICAL)
    CI->>AKS: helm upgrade --install
    AKS-->>Dev: application déployée et supervisée
```

Étapes du pipeline, conformes au cahier des charges :
1. **Build** : compilation et génération des images Docker.
2. **Tests** : unitaires et d'intégration (backend et frontend).
3. **Scan de vulnérabilités** : Trivy (dépendances, IaC, images), CodeQL
   (analyse statique), Gitleaks (fuite de secrets).
4. **Déploiement automatisé** : Helm sur Kubernetes (AKS).

> Le cahier des charges cite GitLab CI/ArgoCD comme exemple. Le dépôt étant
> hébergé sur GitHub, nous utilisons **GitHub Actions** (équivalent fonctionnel)
> pour l'intégration et le déploiement continus. Le principe (build → test →
> scan → déploiement orchestré) est strictement respecté.

## 4. Choix d'architecture justifiés

| Décision | Justification |
|---|---|
| AKS plutôt que VM | Orchestration, auto-réparation, scalabilité (HPA), exigence pédagogique Kubernetes. |
| 1 nœud B2s | FinOps : plan de contrôle gratuit, nœud burstable à faible coût. |
| Loki plutôt qu'ELK | ELK (Elasticsearch) est lourd en RAM/CPU/stockage. Loki indexe les labels, coût d'exploitation très inférieur — adapté au budget. |
| Secrets dans GitHub Actions (pas de Key Vault) | Choix MVP « léger » : moins de pièces à gérer. Les identifiants Azure restent dans GitHub Secrets ; le secret DB est généré par Terraform et injecté via Helm. |
| PostgreSQL Flexible (public + firewall Azure) | Base managée, sauvegardes automatiques (PRA). Accès limité aux ressources Azure + TLS obligatoire, sans la complexité d'un réseau privé (MVP léger). |
| Région Poland Central | Région européenne récente et économique (RGPD). |
| AKS kubenet mono-nœud | Réseau par défaut, sans VNet à gérer : déploiement fiable et automatisable. |
| Connexion CI par az login user/pass | Simplicité de mise en route ; un service principal + OIDC est l'évolution recommandée en production. |

## 5. Données

```mermaid
erDiagram
    PATIENT ||--o{ APPAREIL_AUDITIF : possede
    PATIENT ||--o{ RENDEZ_VOUS : planifie
    PATIENT {
      int id
      string nom
      string prenom
      string email
      string telephone
      date date_naissance
    }
    APPAREIL_AUDITIF {
      int id
      string marque
      string modele
      string numero_serie
      string oreille
      date date_pose
    }
    RENDEZ_VOUS {
      int id
      datetime date_heure
      string motif
      enum statut
    }
```
