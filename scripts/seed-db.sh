#!/usr/bin/env bash
# Injecte le jeu de données de démonstration dans un pod backend du cluster.
set -euo pipefail
NS="${NAMESPACE:-audioprothese}"
POD=$(kubectl get pod -n "$NS" -l component=backend -o jsonpath='{.items[0].metadata.name}')
echo "Seed via le pod $POD ..."
kubectl exec -n "$NS" "$POD" -- python -m app.seed
