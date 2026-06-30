# Checklist déploiement & démonstration

Guide pas à pas, côté utilisateur, pour déployer sur Azure et **prouver que
tout fonctionne** (utile pour la vidéo MVP).

## Étape 0 — Récupérer ses identifiants Azure

```bash
az login                 # ouvre le navigateur
az account show          # note "id" (= SUBSCRIPTION_ID) et "tenantId" (= TENANT_ID)
```

- `AZURE_USERNAME` / `AZURE_PASSWORD` = ton e-mail + mot de passe Azure.
- ⚠️ **Si ton compte a la MFA activée**, le login user/mot de passe échouera en
  CI. Utilise alors un **service principal** (voir « Annexe MFA » en bas).
- Ton compte Azure for Students est **Owner** de son abonnement → il peut créer
  les ressources ET les attributions de rôle (AcrPull). ✅

## Étape 1 — Configurer les secrets GitHub

Dépôt → **Settings → Secrets and variables → Actions → New repository secret** :

| Secret | Valeur |
|---|---|
| `AZURE_USERNAME` | ton e-mail Azure |
| `AZURE_PASSWORD` | ton mot de passe |
| `AZURE_TENANT_ID` | `tenantId` de `az account show` |
| `AZURE_SUBSCRIPTION_ID` | `id` de `az account show` |
| `BUDGET_EMAIL` | ton e-mail (alertes budget) |
| `SLACK_WEBHOOK_URL` | *(optionnel)* webhook Slack/Teams |

## Étape 2 — Lancer le déploiement (CI)

- **Actions → Deploy (Azure tout-en-un) → Run workflow → `deploy`**.
- Ou pousse un commit sur `main`.

Suis les logs du job. À la fin s'affiche :

```
 Application accessible sur : http://<IP_INGRESS>/
 API (Swagger)             : http://<IP_INGRESS>/api/docs
 MinIO (on-prem)           : http://<IP_ONPREM>:9000  (console :9001)
```

Durée typique : ~15-25 min (création AKS + PostgreSQL + VM).

## Étape 3 — Récupérer les infos d'accès (depuis ton poste)

```bash
# IP de l'application
az aks get-credentials -g rg-audioprothese-mvp -n aks-audioprothese-mvp
kubectl get svc -n ingress-nginx ingress-nginx-controller

# Identifiants MinIO (lecture des sorties Terraform)
cd infra/terraform
SA="sttf$(echo -n "$AZURE_SUBSCRIPTION_ID" | md5sum | cut -c1-12)"
KEY=$(az storage account keys list -g rg-tfstate-audioprothese -n "$SA" --query '[0].value' -o tsv)
terraform init \
  -backend-config="resource_group_name=rg-tfstate-audioprothese" \
  -backend-config="storage_account_name=$SA" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=mvp.tfstate" \
  -backend-config="access_key=$KEY"
terraform output -raw minio_root_user
terraform output -raw minio_root_password
terraform output -raw onprem_public_ip
```

## Étape 4 — Tests à effectuer (preuves que tout marche)

### 4.1 Application & API
```bash
IP=<IP_INGRESS>
curl http://$IP/healthz        # {"status":"ok"}
curl http://$IP/readyz         # {"status":"ready"}  (DB joignable)
# Créer un patient
curl -X POST http://$IP/api/patients -H 'Content-Type: application/json' \
  -d '{"nom":"Demo","prenom":"Jury"}'
curl http://$IP/api/patients   # le patient apparaît
```
- Ouvrir `http://$IP/` (UI) → créer/supprimer un patient.
- Ouvrir `http://$IP/api/docs` (Swagger).

### 4.2 Conteneurs / Kubernetes
```bash
kubectl get pods -n audioprothese          # backend + frontend Running
kubectl get hpa -n audioprothese           # autoscaling actif
# Résilience : suppression d'un pod -> recréé automatiquement
kubectl delete pod -n audioprothese -l component=backend
kubectl get pods -n audioprothese -w
```

### 4.3 Persistance / base de données
- Créer un patient, supprimer le pod backend, re-lister : la donnée persiste
  (stockée dans PostgreSQL, pas dans le pod).

### 4.4 Observabilité (dashboard + logs)
Le plus simple pour la démo dashboard : **en local**
```bash
docker compose up -d
# Grafana http://localhost:3000 (admin/admin) -> dashboard "Audioprothèse"
# Prometheus http://localhost:9090  | Alertmanager http://localhost:9093
```
Sur le cluster (optionnel) : installer kube-prometheus-stack (cf. docs/monitoring.md).

### 4.5 Alertes Slack/Teams
- Local : `docker compose stop backend` → après ~1 min, l'alerte `BackendDown`
  part vers Slack (si `SLACK_WEBHOOK_URL` défini).

### 4.6 Sécurité / DevSecOps
- Onglet **Actions** : workflow `DevSecOps` vert (Trivy, CodeQL, Gitleaks).
- Onglet **Security** : résultats CodeQL / Trivy (SARIF).
- `kubectl get pods -n audioprothese -o jsonpath='{..securityContext}'` → non-root.

### 4.7 On-premise / MinIO / PRA
- Console MinIO : `http://<IP_ONPREM>:9001` (login = minio_root_user/password).
- Lancer une sauvegarde : **Actions → Backup → Run workflow → `backup`**.
- Vérifier l'objet `.sql.gz` créé dans le bucket `audioprothese-backups`.
- Restauration : **Actions → Backup → `restore`**.

### 4.8 CI/CD
- Montrer le pipeline `Deploy` qui a tout provisionné et déployé sans
  intervention manuelle.

## Étape 5 — FinOps (À FAIRE après la démo)

```bash
# Soit via la CI : Actions -> Deploy -> Run workflow -> destroy
# Soit en local :
./scripts/teardown.sh
```
> À ~80 $/mois en 24/7, ne pas laisser tourner : détruire après chaque session.
> Suivi du crédit : Portail Azure → Subscriptions → Azure for Students.

---

## Annexe MFA — utiliser un service principal (si le login user/pass échoue)

```bash
az ad sp create-for-rbac --name sp-audioprothese \
  --role Owner --scopes /subscriptions/$AZURE_SUBSCRIPTION_ID
# Renvoie appId / password / tenant
```
Mettre `appId` dans `AZURE_USERNAME`, `password` dans `AZURE_PASSWORD`, puis
adapter l'étape de login des workflows en ajoutant `--service-principal` :
`az login --service-principal -u $AZURE_USERNAME -p $AZURE_PASSWORD --tenant $AZURE_TENANT_ID`
(demande-moi de faire la modif si besoin).

## Dépannage rapide

| Symptôme | Cause probable | Solution |
|---|---|---|
| `az login` échoue en CI | MFA activée | Service principal (annexe) |
| Quota / région refusée | Quota vCPU Student ou région indispo | Changer `location` (ex. `westeurope`) ou `aks_node_size` dans `variables.tf` |
| Pods `ImagePullBackOff` | AcrPull pas encore propagé | Re-lancer le job deploy |
| Pas d'IP d'Ingress | LoadBalancer en cours | Attendre 1-2 min, re-vérifier |
