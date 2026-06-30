# Validation & conformité — comment tester chaque exigence

Ce document explique **comment tester** chaque brique et **prouve la
correspondance** avec le cahier des charges (annexe technique DevOps) et le
cadre pédagogique M2.

> Pré-requis pour les tests cluster : `az aks get-credentials -g
> rg-audioprothese-mvp -n aks-audioprothese-mvp`. IP de l'app = IP publique de
> l'Ingress (`kubectl get svc -n ingress-nginx ingress-nginx-controller`).

## 0. Test automatique global

```bash
APP_IP=<IP_INGRESS> ./scripts/smoke-test.sh
```
Vérifie en une commande : API, base de données, Swagger, métriques, pods
applicatifs, ServiceMonitor, HPA, pods monitoring, Ingress Grafana. Objectif :
**0 échec**.

---

## 1. Application (Dev) — patients / appareils / rendez-vous

| Test | Commande / action | Attendu |
|---|---|---|
| Santé | `curl http://$IP/healthz` | `{"status":"ok"}` |
| Base joignable | `curl http://$IP/readyz` | `{"status":"ready"}` |
| Créer patient | `curl -X POST http://$IP/api/patients -H 'Content-Type: application/json' -d '{"nom":"X","prenom":"Y"}'` | JSON avec `id` |
| Lister | `curl http://$IP/api/patients` | liste contenant le patient |
| Appareil auditif | `POST http://$IP/api/patients/<id>/appareils` | appareil créé |
| Rendez-vous | `POST http://$IP/api/patients/<id>/rendez-vous` | RDV créé |
| UI | navigateur `http://$IP/` | interface de gestion |
| Doc API | `http://$IP/api/docs` | Swagger interactif |
| Tests unitaires | onglet Actions → CI (pytest + vitest) | verts |

## 2. Infrastructure as Code (Terraform) + Ansible

| Test | Action | Attendu |
|---|---|---|
| IaC valide | Actions → CI → job `Terraform` | `fmt` + `validate` verts |
| Provisioning | Actions → Deploy → `Terraform apply` | AKS, ACR, PostgreSQL, VM on-prem créés |
| Ansible (config) | Actions → Deploy → étape Ansible MinIO | playbook OK |
| Ansible (syntaxe) | Actions → CI → job `ansible-lint` | vert |

## 3. Conteneurs & orchestration Kubernetes

| Test | Commande | Attendu |
|---|---|---|
| Images non-root | `kubectl get pod -n audioprothese -o jsonpath='{.items[0].spec.securityContext}'` | `runAsNonRoot:true` |
| Pods up | `kubectl get pods -n audioprothese` | backend + frontend `Running` |
| Auto-réparation | `kubectl delete pod -n audioprothese -l component=backend` | pod recréé automatiquement |
| Scalabilité | `kubectl get hpa -n audioprothese` | HPA actif (min/max) |
| Registry | Actions → Deploy → Build & push | images poussées sur ACR |

## 4. CI/CD & DevSecOps

| Exigence cahier | Test | Attendu |
|---|---|---|
| Pipeline build→test→scan→deploy | Actions → Deploy | run vert de bout en bout |
| Scan vulnérabilités (Trivy/Clair) | Actions → DevSecOps (Trivy fs) + Deploy (Trivy image) | pas de CRITICAL |
| Analyse statique | Actions → DevSecOps → CodeQL | vert |
| Fuite de secrets | Actions → DevSecOps → Gitleaks | vert |
| Rapports | onglet **Security** du dépôt | résultats SARIF visibles |

## 5. Supervision & observabilité

| Pilier (cahier) | Test | Attendu |
|---|---|---|
| Métriques (Prometheus/Grafana) | `http://grafana.$IP.nip.io/` → dashboard « Audioprothèse » | courbes débit/latence/erreurs |
| Générer du trafic | `for i in $(seq 1 50); do curl -s http://$IP/api/patients >/dev/null; done` | les courbes montent |
| Logs (Loki) | Grafana → Explore → datasource Loki → `{namespace="audioprothese"}` | logs applicatifs |
| Alerting (Slack/Teams) | `kubectl scale deploy/backend -n audioprothese --replicas=0` puis attendre | alerte `BackendDown` (→ Slack si webhook) ; remettre `--replicas=1` |

## 6. Sécurité

| Exigence | Test | Attendu |
|---|---|---|
| RBAC Kubernetes | `kubectl get role,serviceaccount -n audioprothese` | ServiceAccount dédié, Role viewer |
| TLS base de données | inspecter `DATABASE_URL` (`sslmode=require`) | TLS imposé |
| Secrets hors Git | Gitleaks vert + secret DB en Secret K8s | aucun secret versionné |
| Conteneurs durcis | securityContext (cf. §3) | non-root, capabilities drop |
| Conformité RGPD | région `polandcentral` (UE) | données en UE |

## 7. Architecture hybride (on-premise) & PRA/PCA

| Exigence | Test | Attendu |
|---|---|---|
| Site on-prem (réseau séparé) | `terraform output onprem_public_ip` ; VNet `10.20.0.0/16` non peeré | VM joignable, réseau distinct |
| MinIO chiffré | `http://<onprem_ip>:9001` (console) | bucket `audioprothese-backups`, SSE activé |
| Sauvegarde | Actions → Backup → `backup` | objet `.sql.gz` dans MinIO |
| Restauration (Ansible) | Actions → Backup → `restore` | base restaurée |
| Redémarrage auto | cf. auto-réparation K8s (§3) | services relancés seuls |

## 8. FinOps (spécifique M2)

| Exigence | Test | Attendu |
|---|---|---|
| Dimensionnement maîtrisé | `infra/terraform/variables.tf` | SKU minimaux documentés |
| Garde-fou budget | Portail Azure → Cost Management → Budgets | budget + alertes e-mail |
| Extinction | Actions → Deploy → `destroy` | toutes les ressources supprimées |
| Suivi | Portail Azure → filtrer par tag `projet` | coûts traçables |

## 9. Matrice de conformité (synthèse cahier des charges)

| Exigence cahier des charges | Couvert | Où / comment tester |
|---|---|---|
| Cloud public (Azure) | ✅ | §2, §3 |
| Serveurs on-premise (hybride) | ✅ (simulé) | §7 |
| Cluster Kubernetes | ✅ | §3 |
| CI/CD (build/test/scan/deploy) | ✅ | §4 |
| Registry Docker | ✅ | §3 (ACR) |
| Scan vulnérabilités Trivy | ✅ | §4 |
| Monitoring Prometheus/Grafana | ✅ | §5 |
| Logs centralisés | ✅ (Loki) | §5 |
| Traces (Jaeger) | ❌ évolution | docs/monitoring.md §6 |
| Secrets centralisés | ✅ (GitHub Secrets + Secret K8s) | §6 |
| RBAC | ✅ | §6 |
| TLS | ✅ (DB) | §6 |
| RGPD/HDS | ✅ RGPD / HDS = évolution | §6 |
| Sauvegardes chiffrées | ✅ (MinIO SSE) | §7 |
| Réplication on-prem ↔ cloud | ✅ (pg_dump→MinIO) | §7 |
| Restauration automatisée (Ansible) | ✅ | §7 |
| Runbooks | ✅ | docs/runbooks.md |
| Alertes Slack/Teams | ✅ | §5 |
| Gestion des coûts (FinOps M2) | ✅ | §8 |
| Documentation complète | ✅ | docs/ |

Écarts assumés et documentés (arbitrages budget / périmètre) : **ELK → Loki**,
**Vault → GitHub Secrets**, **GitLab CI → GitHub Actions**, **Jaeger** et
**ArgoCD** en perspectives. Voir `docs/livrables.md`.
