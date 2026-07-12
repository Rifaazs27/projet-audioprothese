# Runbook de démonstration — A → Z (valeurs réelles)

> Toutes les infos sont pré-remplies. À dérouler dans l'ordre pour prouver que
> tout fonctionne (vidéo / soutenance).

## Coordonnées de l'environnement

| Élément | Valeur |
|---|---|
| Dépôt | https://github.com/rifaazs27/projet-audioprothese |
| Application | http://20.215.177.162/ |
| API (Swagger) | http://20.215.177.162/api/docs |
| Grafana | http://grafana.20.215.177.162.nip.io/ — `admin` / `AudioGrafana2026!` |
| MinIO (on-prem) | http://74.248.17.27:9001 — user `audiominio` |
| Resource Group | `rg-audioprothese-mvp` (région `polandcentral`) |
| Cluster AKS | `aks-audioprothese-mvp` |
| VM on-prem | `vm-onprem-audioprothese-mvp` (IP 74.248.17.27, VNet 10.20.0.0/16) |

Connexion au cluster (une fois) :
```bash
az login
az aks get-credentials -g rg-audioprothese-mvp -n aks-audioprothese-mvp --overwrite-existing
```
Mot de passe MinIO (si besoin de se connecter à la console) :
```bash
cd ~/projet-audioprothese/infra/terraform
SUB=$(az account show --query id -o tsv)
SA="sttf$(echo -n "$SUB" | md5sum | cut -c1-12)"
KEY=$(az storage account keys list -g rg-tfstate-audioprothese -n "$SA" --query '[0].value' -o tsv)
terraform init -reconfigure \
  -backend-config="resource_group_name=rg-tfstate-audioprothese" \
  -backend-config="storage_account_name=$SA" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=mvp.tfstate" -backend-config="access_key=$KEY"
terraform output -raw minio_root_password; echo
```

---

## A. Le pipeline CI/CD (point de départ DevOps)
👉 GitHub → **Actions → Deploy (Azure tout-en-un)** : montrer un run **vert**.
Message clé : « un `git push` provisionne l'infra + déploie tout, sans action manuelle ».

## B. Test automatique global (preuve rapide)
```bash
cd ~/projet-audioprothese
APP_IP=20.215.177.162 ./scripts/smoke-test.sh
```
Attendu : **0 échec** (API, DB, Swagger, metrics, pods, ServiceMonitor, HPA, monitoring, Ingress Grafana).

## C. Application & base de données
```bash
curl http://20.215.177.162/healthz     # {"status":"ok"}
curl http://20.215.177.162/readyz      # {"status":"ready"}  (PostgreSQL OK)
curl -X POST http://20.215.177.162/api/patients \
  -H 'Content-Type: application/json' -d '{"nom":"Demo","prenom":"Soutenance"}'
curl http://20.215.177.162/api/patients
```
Navigateur : http://20.215.177.162/ (UI) puis http://20.215.177.162/api/docs (Swagger).

## D. Conteneurs & Kubernetes (résilience)
```bash
kubectl get pods -n audioprothese
kubectl delete pod -n audioprothese -l component=backend   # recréé automatiquement
kubectl get pods -n audioprothese -w
kubectl get hpa -n audioprothese                            # autoscaling
```

## E. Observabilité (Grafana / Prometheus / Loki)
```bash
for i in $(seq 1 60); do curl -s http://20.215.177.162/api/patients >/dev/null; done
```
Puis http://grafana.20.215.177.162.nip.io/ (`admin` / `AudioGrafana2026!`) :
- Dashboard **« Audioprothèse — Vue d'ensemble »** : débit, latence p95, erreurs, dispo.
- Explore → datasource **Loki** → requête `{namespace="audioprothese"}` (logs).

## F. Sécurité / DevSecOps
- GitHub → onglet **Security** : résultats Trivy, CodeQL, Gitleaks.
- GitHub → **Actions → DevSecOps** : run vert.
```bash
kubectl get pod -n audioprothese -l component=backend \
  -o jsonpath='{.items[0].spec.securityContext}'; echo   # non-root, durci
kubectl get serviceaccount,role -n audioprothese          # RBAC
```

## G. PRA / PCA (sauvegarde → perte → restauration)
1. Créer un témoin :
   ```bash
   curl -X POST http://20.215.177.162/api/patients \
     -H 'Content-Type: application/json' -d '{"nom":"DEMO_PRA","prenom":"Temoin"}'
   curl -s http://20.215.177.162/api/patients | grep DEMO_PRA   # noter l'id
   ```
2. GitHub → **Actions → Backup → Run workflow → `backup`** (attendre le vert).
   Montrer l'objet `.sql.gz` dans la console MinIO http://74.248.17.27:9001.
3. Simuler la perte :
   ```bash
   curl -X DELETE http://20.215.177.162/api/patients/<id>
   curl -s http://20.215.177.162/api/patients | grep DEMO_PRA || echo "perdu"
   ```
4. GitHub → **Actions → Backup → Run workflow → `restore`** (attendre le vert).
5. Vérifier la reprise :
   ```bash
   curl -s http://20.215.177.162/api/patients | grep DEMO_PRA   # de retour ✅
   ```

## H. Architecture hybride (on-premise)
- Console MinIO http://74.248.17.27:9001 : la VM (VNet `10.20.0.0/16`, séparé du
  cluster) héberge les sauvegardes chiffrées → « données sensibles on-premise ».

## I. FinOps (M2)
- Montrer `docs/finops-gestion-couts.md` (estimation + garde-fous budget).
- Portail Azure → Cost Management → budget + alertes.

## J. Extinction (à la fin — stoppe la facturation)
GitHub → **Actions → Deploy (Azure tout-en-un) → Run workflow → `destroy`**.
(Reproductible : un `deploy` recrée tout en un clic.)

---

### Ordre conseillé pour la vidéo
A (pipeline) → C (app) → E (monitoring) → D (résilience) → F (sécurité) →
G (PRA) → H (hybride) → I (FinOps) → J (teardown).
