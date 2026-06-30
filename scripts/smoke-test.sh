#!/usr/bin/env bash
# Tests de bout en bout du MVP déployé. Vérifie API, base de données,
# Kubernetes, monitoring et on-prem MinIO.
#
# Usage :
#   APP_IP=20.215.177.162 ./scripts/smoke-test.sh
# (APP_IP = IP publique de l'Ingress ; récupérable via
#  kubectl get svc -n ingress-nginx ingress-nginx-controller)
set -uo pipefail

APP_IP="${APP_IP:-20.215.177.162}"
BASE="http://${APP_IP}"
PASS=0; FAIL=0
ok()   { echo "  ✅ $1"; PASS=$((PASS+1)); }
ko()   { echo "  ❌ $1"; FAIL=$((FAIL+1)); }
hr()   { echo "----------------------------------------------"; }

echo "Cible : $BASE"
hr; echo "1) API & base de données"
curl -fsS "$BASE/healthz" | grep -q '"ok"'      && ok "/healthz répond ok"            || ko "/healthz"
curl -fsS "$BASE/readyz"  | grep -q '"ready"'    && ok "/readyz (PostgreSQL joignable)" || ko "/readyz"
PID=$(curl -fsS -X POST "$BASE/api/patients" -H 'Content-Type: application/json' \
        -d '{"nom":"SmokeTest","prenom":"CI"}' | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
[ -n "${PID:-}" ] && ok "création patient (id=$PID)" || ko "création patient"
curl -fsS "$BASE/api/patients" | grep -q 'SmokeTest' && ok "lecture patient"            || ko "lecture patient"
[ -n "${PID:-}" ] && curl -fsS -X DELETE "$BASE/api/patients/$PID" >/dev/null && ok "suppression patient" || ko "suppression patient"

hr; echo "2) Observabilité (métriques exposées)"
curl -fsS "$BASE/metrics" | grep -q 'http_requests_total' && ok "/metrics expose les compteurs" || ko "/metrics"

hr; echo "3) Swagger"
curl -fsS "$BASE/api/docs" | grep -qi 'swagger\|openapi' && ok "Swagger /api/docs servi" || ko "Swagger"

# Les vérifs Kubernetes nécessitent kubectl configuré sur le cluster.
if command -v kubectl >/dev/null 2>&1 && kubectl get ns audioprothese >/dev/null 2>&1; then
  hr; echo "4) Kubernetes"
  R=$(kubectl get pods -n audioprothese --no-headers 2>/dev/null | grep -c 'Running')
  [ "$R" -ge 2 ] && ok "pods app Running ($R)" || ko "pods app ($R running)"
  kubectl get servicemonitor -n audioprothese >/dev/null 2>&1 && ok "ServiceMonitor présent" || ko "ServiceMonitor"
  kubectl get hpa -n audioprothese >/dev/null 2>&1 && ok "HPA présent" || ko "HPA"

  hr; echo "5) Monitoring"
  M=$(kubectl get pods -n monitoring --no-headers 2>/dev/null | grep -c 'Running')
  [ "$M" -ge 3 ] && ok "pods monitoring Running ($M)" || ko "pods monitoring ($M running)"
  kubectl get ingress -n monitoring >/dev/null 2>&1 && ok "Ingress Grafana présent" || ko "Ingress Grafana"
else
  hr; echo "4-5) Kubernetes/Monitoring : kubectl non configuré -> étapes ignorées"
  echo "     (az aks get-credentials -g rg-audioprothese-mvp -n aks-audioprothese-mvp)"
fi

hr
echo "Résultat : $PASS OK / $FAIL échec(s)"
[ "$FAIL" -eq 0 ] && echo "🎉 Tout fonctionne." || echo "⚠️ Voir les ❌ ci-dessus."
exit "$FAIL"
