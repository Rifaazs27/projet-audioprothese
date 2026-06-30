#!/usr/bin/env bash
# Déploiement complet de bout en bout sur Azure (à lancer depuis un poste
# disposant d'az, kubectl, helm et terraform).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> 1/5 Provisionnement de l'infrastructure (Terraform)"
cd infra/terraform
terraform init
terraform apply -auto-approve
RG=$(terraform output -raw resource_group)
AKS=$(terraform output -raw aks_name)
ACR=$(terraform output -raw acr_login_server)
cd ../..

echo "==> 2/5 Configuration de kubectl"
az aks get-credentials --resource-group "$RG" --name "$AKS" --overwrite-existing

echo "==> 3/5 Installation des briques cluster (ingress, cert-manager, monitoring)"
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx >/dev/null
helm repo add jetstack https://charts.jetstack.io >/dev/null
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts >/dev/null
helm repo add grafana https://grafana.github.io/helm-charts >/dev/null
helm repo update >/dev/null

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace
helm upgrade --install cert-manager jetstack/cert-manager \
  -n cert-manager --create-namespace --set crds.enabled=true
kubectl label namespace monitoring kubernetes.io/metadata.name=monitoring --overwrite >/dev/null 2>&1 || true
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f monitoring/k8s/kube-prometheus-stack-values.yaml
helm upgrade --install loki grafana/loki-stack \
  -n monitoring -f monitoring/k8s/loki-stack-values.yaml

echo "==> 4/5 Déploiement de l'application"
TAG="${IMAGE_TAG:-latest}"
helm upgrade --install audioprothese k8s/helm/audioprothese \
  --namespace audioprothese --create-namespace \
  --set image.registry="$ACR" --set image.tag="$TAG"

echo "==> 5/5 Terminé. Ressources : $RG / $AKS / $ACR"
kubectl get pods -n audioprothese
