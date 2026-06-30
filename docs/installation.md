# Guide d'installation et de déploiement

## A. Développement local (5 minutes)

Prérequis : Docker + Docker Compose.

```bash
git clone https://github.com/rifaazs27/projet-audioprothese.git
cd projet-audioprothese
docker compose up --build
docker compose exec backend python -m app.seed   # données de démo
```

Accès : frontend http://localhost:8080 · API http://localhost:8000/docs ·
Grafana http://localhost:3000 (admin/admin) · Prometheus http://localhost:9090.

## B. Déploiement sur Azure

### B.1 Prérequis poste

- Compte Azure Student (crédit 85 $).
- CLI installés : `az`, `terraform` (≥ 1.6), `kubectl`, `helm`.

```bash
az login
az account show          # vérifier l'abonnement actif
```

### B.2 (Recommandé) État Terraform distant

Pour le travail en équipe, stockez le `tfstate` dans Azure :

```bash
az group create -n rg-tfstate-audioprothese -l francecentral
az storage account create -n sttfstateaudio$RANDOM -g rg-tfstate-audioprothese -l francecentral --sku Standard_LRS
# puis décommentez le bloc backend "azurerm" dans infra/terraform/providers.tf
```

### B.3 Provisionnement + déploiement automatisé

```bash
cp infra/terraform/terraform.tfvars.example infra/terraform/terraform.tfvars
# éditez budget_alert_emails avec votre adresse

./scripts/deploy.sh
```

Le script :
1. exécute `terraform apply` (AKS, ACR, PostgreSQL, Key Vault, budget) ;
2. configure `kubectl` ;
3. installe ingress-nginx, cert-manager, kube-prometheus-stack et Loki ;
4. déploie l'application via Helm.

### B.4 Récupérer l'URL et tester

```bash
kubectl get ingress -n audioprothese
kubectl get svc -n ingress-nginx ingress-nginx-controller   # IP publique
```

Pointez votre nom de domaine (ou `/etc/hosts`) vers l'IP de l'Ingress, puis
ouvrez `https://<host>/`. Swagger : `https://<host>/api/docs`.

### B.5 Données de démonstration

```bash
./scripts/seed-db.sh
```

## C. CI/CD — secrets GitHub à configurer

Pour activer le déploiement automatique (`.github/workflows/cd-deploy.yml`),
ajoutez dans **Settings → Secrets and variables → Actions** :

| Secret | Description |
|---|---|
| `AZURE_CLIENT_ID` | App registration (fédération OIDC GitHub) |
| `AZURE_TENANT_ID` | Tenant Azure |
| `AZURE_SUBSCRIPTION_ID` | Abonnement |
| `ACR_NAME` / `ACR_LOGIN_SERVER` | Registre de conteneurs |
| `AKS_RESOURCE_GROUP` / `AKS_CLUSTER_NAME` | Cluster cible |
| `APP_HOSTNAME` | Nom de domaine de l'application |
| `BUDGET_EMAIL` | E-mail des alertes budget (workflow infra) |

La fédération OIDC (pas de mot de passe stocké) se configure ainsi :

```bash
az ad app create --display-name "github-audioprothese"
# Ajoutez un federated credential pour le sujet :
#   repo:rifaazs27/projet-audioprothese:ref:refs/heads/main
#   repo:rifaazs27/projet-audioprothese:environment:production
# Puis attribuez les rôles Contributor + AcrPush sur le resource group.
```

## D. Désactivation (FinOps — IMPORTANT)

Après chaque démonstration, **détruisez l'infrastructure** pour ne pas
consommer le crédit :

```bash
./scripts/teardown.sh
```

Voir [`finops-gestion-couts.md`](finops-gestion-couts.md) pour les détails.
