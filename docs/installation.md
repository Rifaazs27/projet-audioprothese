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

## B. Déploiement sur Azure — 100 % par la CI (recommandé)

Tout est automatisé par le workflow **`.github/workflows/deploy.yml`**. Aucune
commande manuelle : la CI se connecte à Azure, crée l'infrastructure, construit
les images et déploie l'application.

### B.1 Configurer les secrets GitHub (une seule fois)

**Settings → Secrets and variables → Actions → New repository secret** :

| Secret | Description |
|---|---|
| `AZURE_USERNAME` | Identifiant de connexion Azure (`az login -u`) |
| `AZURE_PASSWORD` | Mot de passe associé |
| `AZURE_TENANT_ID` | ID du tenant Azure AD |
| `AZURE_SUBSCRIPTION_ID` | ID de l'abonnement (Azure for Students) |
| `BUDGET_EMAIL` | E-mail pour les alertes de budget (FinOps) |
| `SLACK_WEBHOOK_URL` | *(optionnel)* webhook Slack/Teams pour les alertes |

> Le compte utilisé ne doit pas exiger de MFA (la connexion CI est non
> interactive), et doit avoir le rôle **Contributor** sur l'abonnement.
> Récupérer les IDs : `az account show` → `id` (subscription) et `tenantId`.

### B.2 Lancer le déploiement

- **Automatique** : tout `push` sur `main` (hors fichiers `docs/`/markdown)
  déclenche le provisionnement + déploiement.
- **Manuel** : onglet **Actions → Deploy (Azure tout-en-un) → Run workflow**,
  choisir `deploy`.

Le pipeline enchaîne :
1. `az login` (utilisateur / mot de passe) ;
2. création automatique du Storage Account d'état Terraform ;
3. `terraform apply` (AKS, ACR, PostgreSQL, **VM on-prem + MinIO**, budget) ;
4. build + push des images vers ACR, scan Trivy ;
5. installation de l'Ingress NGINX ;
6. déploiement Helm de l'application ;
7. **Ansible** configure MinIO (chiffré) sur la VM on-prem.

> Sauvegardes : le workflow `.github/workflows/backup.yml` (cron quotidien, ou
> manuel) réalise un `pg_dump` vers MinIO et permet la **restauration** via
> Ansible (`mode: restore`).

À la fin du job, l'**URL d'accès** (IP publique de l'Ingress) est affichée dans
les logs :

```
 Application accessible sur : http://<IP>/
 API (Swagger)             : http://<IP>/api/docs
```

### B.3 Données de démonstration

```bash
az aks get-credentials -g rg-audioprothese-mvp -n aks-audioprothese-mvp
kubectl exec -n audioprothese deploy/backend -- python -m app.seed
```

## C. Désactivation (FinOps — IMPORTANT)

Après chaque démonstration, **détruisez l'infrastructure** pour ne pas
consommer le crédit :

- **Manuel** : Actions → *Deploy (Azure tout-en-un)* → Run workflow → `destroy`.
- **En local** : `./scripts/teardown.sh`.

Voir [`finops-gestion-couts.md`](finops-gestion-couts.md) pour les détails.

## D. Déploiement manuel en local (optionnel)

Pour déboguer hors CI (poste équipé de `az`, `terraform`, `kubectl`, `helm`,
`docker`) :

```bash
az login
./scripts/deploy.sh
```

## E. Région et dimensionnement

- Région : **Poland Central** (`polandcentral`).
- Nœud AKS : **Standard_B2s_v2** (2 vCPU), 1 nœud, plan de contrôle gratuit.
- PostgreSQL : Flexible Server **B_Standard_B1ms** (burstable).

Ces valeurs sont dans `infra/terraform/variables.tf` et ajustables.
