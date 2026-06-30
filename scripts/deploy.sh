#!/usr/bin/env bash
# Déploiement de bout en bout (équivalent local du workflow CI deploy.yml).
# Le moyen recommandé reste la CI ; ce script sert au debug / démo locale.
# Prérequis : az (connecté), terraform, kubectl, helm, docker.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> 1/4 Provisionnement de l'infrastructure (Terraform)"
cd infra/terraform
terraform init
terraform apply -auto-approve
RG=$(terraform output -raw resource_group)
AKS=$(terraform output -raw aks_name)
ACR_NAME=$(terraform output -raw acr_name)
ACR=$(terraform output -raw acr_login_server)
DBURL=$(terraform output -raw database_url)
cd ../..

echo "==> 2/4 Build & push des images"
TAG="${IMAGE_TAG:-local}"
az acr login --name "$ACR_NAME"
docker build -t "$ACR/audioprothese-backend:$TAG" app/backend
docker build -t "$ACR/audioprothese-frontend:$TAG" app/frontend
docker push "$ACR/audioprothese-backend:$TAG"
docker push "$ACR/audioprothese-frontend:$TAG"

echo "==> 3/4 Configuration du cluster + Ingress NGINX"
az aks get-credentials --resource-group "$RG" --name "$AKS" --overwrite-existing
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx >/dev/null
helm repo update >/dev/null
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace --set controller.replicaCount=1 --wait

echo "==> 4/4 Déploiement de l'application"
helm upgrade --install audioprothese k8s/helm/audioprothese \
  --namespace audioprothese --create-namespace \
  --set image.registry="$ACR" --set image.tag="$TAG" \
  --set-string databaseUrl="$DBURL" --wait

echo "Terminé. Ressources : $RG / $AKS / $ACR"
kubectl get pods -n audioprothese
echo "IP de l'Ingress :"
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'; echo

# Monitoring (optionnel, plus lourd) — décommenter pour la démo dashboards :
# helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# helm repo add grafana https://grafana.github.io/helm-charts
# helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
#   -n monitoring --create-namespace -f monitoring/k8s/kube-prometheus-stack-values.yaml
# helm install loki grafana/loki-stack -n monitoring -f monitoring/k8s/loki-stack-values.yaml
