# Test de bout en bout de l'infrastructure (suite logique)

Scénario complet à dérouler dans l'ordre. `IP` = IP publique de l'Ingress
(`kubectl get svc -n ingress-nginx ingress-nginx-controller`).
Pré-requis cluster : `az aks get-credentials -g rg-audioprothese-mvp -n aks-audioprothese-mvp`.

---

## Étape 1 — L'infra est provisionnée et déployée (CI)
- Actions → **Deploy (Azure tout-en-un)** : dernier run **vert** (toutes les
  étapes : Terraform, build/scan, Ingress, monitoring, app, Ansible MinIO).
➡️ Prouve : IaC + conteneurs + orchestration + CI/CD.

## Étape 2 — Application & base de données
```bash
curl http://$IP/healthz      # {"status":"ok"}
curl http://$IP/readyz       # {"status":"ready"}  (PostgreSQL OK)
curl http://$IP/api/patients # liste (peut être vide)
```
Navigateur : `http://$IP/` (UI) et `http://$IP/api/docs` (Swagger).
➡️ Prouve : app fonctionnelle + base joignable.

## Étape 3 — Observabilité
1. Génère du trafic :
   ```bash
   for i in $(seq 1 60); do curl -s http://$IP/api/patients >/dev/null; done
   ```
2. Grafana `http://grafana.$IP.nip.io/` (admin / AudioGrafana2026!) →
   dashboard « Audioprothèse — Vue d'ensemble » : le débit/latence montent.
3. Logs : Grafana → Explore → datasource **Loki** → `{namespace="audioprothese"}`.
➡️ Prouve : métriques (Prometheus/Grafana) + logs (Loki).

## Étape 4 — Résilience Kubernetes (PCA)
```bash
kubectl get pods -n audioprothese
kubectl delete pod -n audioprothese -l component=backend
kubectl get pods -n audioprothese -w   # le pod est recréé automatiquement
```
➡️ Prouve : auto-réparation / continuité de service.

## Étape 5 — Sécurité
```bash
# Conteneur non-root
kubectl get pod -n audioprothese -l component=backend \
  -o jsonpath='{.items[0].spec.securityContext}'; echo
# RBAC
kubectl get serviceaccount,role -n audioprothese
```
- Onglet **Security** du dépôt : résultats Trivy / CodeQL / Gitleaks.
➡️ Prouve : durcissement, RBAC, DevSecOps.

## Étape 6 — PRA : sauvegarde → perte → restauration (le test clé)

**6.1 Créer une donnée témoin**
```bash
curl -X POST http://$IP/api/patients -H 'Content-Type: application/json' \
  -d '{"nom":"PRA_TEMOIN","prenom":"Avant_Sauvegarde"}'
curl -s http://$IP/api/patients | grep PRA_TEMOIN   # présent
```

**6.2 Sauvegarder** : Actions → **Backup** → Run workflow → `backup` → run vert.
(Le `pg_dump --clean` est poussé, chiffré, dans MinIO.)

**6.3 Simuler une perte** : supprime le témoin (récupère son id puis) :
```bash
curl -X DELETE http://$IP/api/patients/<id_du_temoin>
curl -s http://$IP/api/patients | grep PRA_TEMOIN   # ABSENT (perte simulée)
```

**6.4 Restaurer** : Actions → **Backup** → Run workflow → `restore` → run vert.

**6.5 Vérifier la reprise**
```bash
curl -s http://$IP/api/patients | grep PRA_TEMOIN   # DE RETOUR ✅
```
➡️ Prouve : sauvegarde chiffrée MinIO + restauration automatisée via Ansible
(réplication on-prem ↔ cloud).

> Note : la restauration ramène l'état **du moment de la sauvegarde** ; les
> données créées après le backup sont volontairement écartées (sémantique PRA).

## Étape 7 — Alerting (optionnel, si SLACK_WEBHOOK_URL défini)
```bash
kubectl scale deploy/backend -n audioprothese --replicas=0   # provoque l'incident
# attendre ~1-2 min : alerte BackendDown (visible Alertmanager / Slack)
kubectl scale deploy/backend -n audioprothese --replicas=1   # rétablir
```

## Étape 8 — FinOps : extinction
- Actions → **Deploy** → Run workflow → `destroy` → toutes les ressources Azure
  sont supprimées (facturation stoppée). Reproductible en un clic.
➡️ Prouve : maîtrise des coûts.

---

### Résumé : ce que la suite démontre
Provisioning IaC → app + DB → observabilité → résilience (PCA) →
sécurité → **PRA (backup/restore)** → alerting → FinOps. Soit l'intégralité
de la chaîne DevOps attendue.
