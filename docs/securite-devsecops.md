# Sécurité & DevSecOps

La sécurité est intégrée à toutes les étapes de la chaîne (« shift-left »),
depuis le code jusqu'à l'exécution en production.

## 1. Sécurité de la chaîne CI/CD

| Contrôle | Outil | Workflow |
|---|---|---|
| Vulnérabilités dépendances & IaC | **Trivy** (fs, misconfig) | `security.yml` |
| Vulnérabilités des images | **Trivy** (image, bloquant si CRITICAL) | `cd-deploy.yml` |
| Analyse statique du code | **CodeQL** (Python + JS) | `security.yml` |
| Fuite de secrets | **Gitleaks** | `security.yml` |
| Scan hebdomadaire programmé | cron lundi 6h | `security.yml` |
| Mises à jour automatiques | **Dependabot** | `dependabot.yml` |

Les rapports SARIF sont publiés dans l'onglet **Security** du dépôt GitHub.

## 2. Gestion des secrets

- **Aucun secret en clair** dans le code ni dans Git (vérifié par Gitleaks).
- **Azure Key Vault** stocke la chaîne de connexion à la base de données.
  Le secret est généré aléatoirement par Terraform (`random_password`) et
  jamais affiché.
- Injection dans les pods via le **CSI Secrets Store driver** + **Workload
  Identity** (cf. `k8s/helm/.../secretproviderclass.yaml`) : le secret n'existe
  qu'en mémoire du pod, pas dans un manifeste.
- **OIDC GitHub → Azure** : la CI/CD s'authentifie sans mot de passe stocké
  (federated credentials), supprimant le risque de secret long terme exfiltré.

## 3. Sécurité Kubernetes (RBAC & durcissement)

- **RBAC activé** sur le cluster (`role_based_access_control_enabled = true`).
- **Compte de service dédié** à l'application, **sans** montage automatique du
  token API (`automountServiceAccountToken: false`) — moindre privilège.
- **Rôle `viewer`** en lecture seule pour la consultation en démonstration.
- **Contexte de sécurité durci** sur chaque conteneur :
  - `runAsNonRoot: true`, utilisateur non-root explicite ;
  - `readOnlyRootFilesystem: true` (backend) ;
  - `allowPrivilegeEscalation: false` ;
  - `capabilities: drop [ALL]` ;
  - `seccompProfile: RuntimeDefault`.
- **Images non-root** : backend (uid 10001), frontend (nginx-unprivileged).

## 4. Cloisonnement réseau

- **Network Policies** (`networkpolicy.yaml`) :
  - `default-deny-ingress` : tout est refusé par défaut dans le namespace ;
  - le backend n'accepte que l'ingress-nginx, le frontend et Prometheus ;
  - le frontend n'accepte que l'ingress-nginx.
- **PostgreSQL en réseau privé** : sous-réseau délégué, pas d'IP publique,
  zone DNS privée.
- **network_policy = "azure"** activée au niveau du cluster AKS.

## 5. Chiffrement (TLS)

- **TLS de bout en bout** côté utilisateur : Ingress NGINX + **cert-manager**
  (certificats Let's Encrypt automatiques, redirection HTTPS forcée).
- **`sslmode=require`** sur la connexion à PostgreSQL.

## 6. Conformité (données de santé)

- Hébergement en **France Central** (RGPD).
- Architecture compatible **HDS** (Hébergeur de Données de Santé) : Azure
  dispose de la certification HDS ; les données restent en France, chiffrées
  au repos (chiffrement de plateforme Azure) et en transit (TLS).
- **Sauvegardes chiffrées** (PostgreSQL, 7 jours de rétention) — cf. PRA/PCA.
- **Journalisation** centralisée (Loki) pour la traçabilité des accès.

## 7. Modèle de menaces (synthèse)

| Menace | Mitigation |
|---|---|
| Vol d'identifiants CI | OIDC sans secret stocké |
| Image vulnérable déployée | Scan Trivy bloquant (CRITICAL) avant déploiement |
| Exposition de la base | Réseau privé, pas d'IP publique |
| Mouvement latéral dans le cluster | Network policies default-deny + RBAC |
| Fuite de secret dans Git | Gitleaks + Key Vault |
| Élévation de privilèges conteneur | securityContext durci, non-root |
