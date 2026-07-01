# Guide de démonstration — Cabinet d'audioprothèse (M2 DO C)

Projet DevOps hybride sur Azure — Équipe : **Zaafir Mougammadou Zaccaria**,
**Elyess Rjafellah**, **Adame Nianghane**, **Anis Douadi**.

---

## 1. Récapitulatif de ce qui a été réalisé

| Domaine | Contenu livré | Responsable |
|---|---|---|
| **Infrastructure as Code** | Terraform : groupe de ressources, AKS (2× Standard_B2s_v2), ACR, PostgreSQL Flexible, réseau, budget FinOps, VM on-premise. État distant auto-créé. | Zaafir |
| **Application** | API FastAPI (patients, **appareils auditifs**, **rendez-vous**) + frontend React. Sondes /healthz /readyz, métriques /metrics, doc /api/docs. | Zaafir |
| **CI/CD** | GitHub Actions : intégration, sécurité, déploiement tout-en-un, sauvegarde planifiée. Pipeline **auto-réparant** (verrou d'état, release Helm, ordonnancement). | Elyess |
| **Kubernetes / Helm** | Chart paramétrable (Deployments, Service, Ingress, Secret, HPA, ServiceMonitor, NetworkPolicy). Autoscaling borné, sondes, rolling update. | Anis |
| **Observabilité** | Prometheus + Grafana (dashboard auto-importé) + Loki + Alertmanager (→ Slack/Teams). Exposé via Ingress nip.io (0 IP publique en plus). | Adame |
| **Sécurité (DevSecOps)** | Trivy, CodeQL, Gitleaks dans la CI (bloquants). Conteneurs non-root, RBAC, TLS, secrets chiffrés (GitHub Secrets → Secret K8s, sans Key Vault). | Adame |
| **On-premise / PRA** | VM dans un VNet séparé (aucun peering) + MinIO chiffré (SSE). Playbooks Ansible de sauvegarde/restauration. Restauration **idempotente**, validée. | Anis |
| **FinOps** | Budget + alertes 50/80/100 %, rightsizing burstable, Loki au lieu d'ELK, destruction à la demande (≈ 10-20 $ sur le semestre au lieu de 650 $+). | Groupe |
| **Livrables** | 1 PDF de groupe + 4 PDF individuels (comparatifs techno, schémas, capture réelle de l'app). | Groupe |

---

## 2. Pré-requis avant la démo

- Récupérer l'IP publique de l'Ingress après déploiement :
  ```bash
  az aks get-credentials -g rg-audioprothese-mvp -n aks-audioprothese-mvp
  kubectl get ingress -A            # colonne ADDRESS = <IP>
  ```
- URLs utiles (remplacer `<IP>`) :
  - Application : `http://<IP>/`
  - API / Swagger : `http://<IP>/api/docs`
  - Grafana : `http://grafana.<IP>.nip.io` (admin / mot de passe défini)
  - MinIO (on-prem) : `http://<IP_VM>:9001`

---

## 3. Scénario de démonstration (dans l'ordre)

> Durée cible ≈ 12-15 min. Chaque étape indique **qui présente**, **quoi montrer**,
> **la commande / action**, et **le résultat attendu**.

### Étape 0 — Introduction (≈ 1 min) — *Groupe (ouverture par Zaafir)*
- Présenter le cabinet, la problématique (données de santé, disponibilité, budget 85 $) et le schéma d'architecture hybride (voir PDF de groupe).

### Étape 1 — Infrastructure as Code (≈ 2 min) — *Zaafir*
- **Montrer** : les fichiers Terraform (`infra/terraform/`), les ressources sur le portail Azure.
- **Action** : rappeler que tout est provisionné automatiquement par la CI (rien à la main).
- **Résultat attendu** : groupe de ressources `rg-audioprothese-mvp` avec AKS, ACR, PostgreSQL, VM on-prem.

### Étape 2 — CI/CD (≈ 2 min) — *Elyess*
- **Montrer** : onglet **Actions**, le workflow **Deploy**, ses étapes enchaînées.
- **Action** : ouvrir un run vert et pointer l'auto-réparation (verrou d'état, ordre CRD→app).
- **Résultat attendu** : run ✅ de bout en bout, IP affichée en fin de pipeline.

### Étape 3 — Application & nouvelles rubriques (≈ 2 min) — *Zaafir*
- **Action 3a** — ouvrir `http://<IP>/`, créer un patient.
- **Action 3b** — cliquer **Gérer** → **Enregistrer un appareil auditif** (marque, modèle, oreille, date).
- **Action 3c** — **Prendre un rendez-vous** (date & heure, motif) → apparaît dans « Rendez-vous à venir ».
- **Action 3d** — ouvrir `http://<IP>/api/docs` (Swagger) pour montrer l'API.
- **Résultat attendu** : patient, appareil et RDV créés et visibles immédiatement.
- **Vérif santé** :
  ```bash
  curl http://<IP>/healthz    # {"status":"ok"}
  curl http://<IP>/readyz     # base joignable
  ```

### Étape 4 — Kubernetes / Helm & résilience PCA (≈ 2 min) — *Anis*
- **Montrer** :
  ```bash
  kubectl get pods,svc,ingress -n audioprothese
  kubectl get hpa -n audioprothese
  ```
- **Action (PCA)** : supprimer un pod backend et observer sa recréation.
  ```bash
  kubectl delete pod -l app=backend -n audioprothese
  kubectl get pods -n audioprothese -w
  ```
- **Résultat attendu** : le pod est recréé automatiquement en quelques secondes, service jamais interrompu.

### Étape 5 — Observabilité (≈ 2 min) — *Adame*
- **Action 5a** — ouvrir Grafana `http://grafana.<IP>.nip.io`, dashboard « Vue d'ensemble ».
- **Action 5b** — générer du trafic pour animer les courbes :
  ```bash
  for i in $(seq 1 200); do curl -s http://<IP>/api/patients >/dev/null; done
  ```
- **Action 5c** — montrer les logs dans Grafana → Explore → source **Loki**.
- **Résultat attendu** : débit, latence p95, taux d'erreurs mis à jour ; logs consultables.

### Étape 6 — Sécurité DevSecOps (≈ 1 min) — *Adame*
- **Montrer** : onglet **Security** du dépôt (rapports Trivy / CodeQL / Gitleaks, format SARIF).
- **Rappeler** : conteneurs non-root, TLS PostgreSQL, secrets jamais en clair.
- **Résultat attendu** : analyses exécutées à chaque livraison, déploiement bloqué si faille critique.

### Étape 7 — On-premise & PRA (≈ 2 min) — *Anis*
- **Action 7a** — dans l'app, créer une **donnée témoin** (ex. patient « PRA_TEMOIN »).
- **Action 7b** — lancer la **sauvegarde** : Actions → **Backup** (mode `backup`) — ou :
  ```bash
  cd ansible && ansible-playbook playbooks/backup.yml
  ```
- **Action 7c** — supprimer la donnée témoin dans l'app (perte simulée).
- **Action 7d** — lancer la **restauration** : Actions → Backup (mode `restore`) — ou :
  ```bash
  ansible-playbook playbooks/restore.yml
  ```
- **Montrer** : console MinIO (`:9001`) avec la sauvegarde chiffrée horodatée.
- **Résultat attendu** : la donnée témoin **réapparaît** à l'identique → PRA validé.

### Étape 8 — FinOps & clôture (≈ 1 min) — *Zaafir / Groupe*
- **Montrer** : budget Azure + alertes, tableau des coûts (PDF de groupe).
- **Action** : détruire l'infra pour stopper la facturation : Actions → Deploy → action `destroy`.
- **Résultat attendu** : ressources supprimées, dépense réelle ≈ 10-20 $ sur le semestre.

---

## 4. Répartition des prises de parole (synthèse)

| Étape | Sujet | Présentateur |
|---|---|---|
| 0 | Introduction / contexte | Groupe (Zaafir) |
| 1 | Infrastructure Terraform | **Zaafir** |
| 2 | CI/CD GitHub Actions | **Elyess** |
| 3 | Application (patients, appareils, RDV) | **Zaafir** |
| 4 | Kubernetes / Helm + résilience (PCA) | **Anis** |
| 5 | Observabilité (Grafana / Loki) | **Adame** |
| 6 | Sécurité (DevSecOps) | **Adame** |
| 7 | On-premise + PRA (backup/restore) | **Anis** |
| 8 | FinOps + destruction | **Zaafir / Groupe** |

---

## 5. Checklist rapide de validation (à cocher avant la démo)

- [ ] `curl http://<IP>/healthz` → `{"status":"ok"}`
- [ ] `curl http://<IP>/readyz` → base joignable
- [ ] Application accessible, création patient OK
- [ ] Enregistrement d'un appareil OK
- [ ] Prise de rendez-vous OK + visible dans « RDV à venir »
- [ ] Swagger `http://<IP>/api/docs` accessible
- [ ] `kubectl get pods -n audioprothese` → tous Running
- [ ] Suppression d'un pod → recréation automatique (PCA)
- [ ] Grafana accessible, courbes alimentées après trafic
- [ ] Logs visibles dans Loki
- [ ] Onglet Security : rapports présents
- [ ] Cycle PRA : donnée témoin sauvegardée → supprimée → restaurée ✅
- [ ] Infra détruite après la démo (budget)
