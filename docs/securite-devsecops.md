# Sécurité & DevSecOps

La sécurité est intégrée à toutes les étapes de la chaîne (« shift-left »),
depuis le code jusqu'à l'exécution en production.

## 1. Sécurité de la chaîne CI/CD

| Contrôle | Outil | Workflow |
|---|---|---|
| Vulnérabilités dépendances & IaC | **Trivy** (fs, misconfig) | `security.yml` |
| Vulnérabilités des images | **Trivy** (image, bloquant si CRITICAL) | `deploy.yml` |
| Analyse statique du code | **CodeQL** (Python + JS) | `security.yml` |
| Fuite de secrets | **Gitleaks** | `security.yml` |
| Scan hebdomadaire programmé | cron lundi 6h | `security.yml` |
| Mises à jour automatiques | **Dependabot** | `dependabot.yml` |

Les rapports SARIF sont publiés dans l'onglet **Security** du dépôt GitHub.

## 2. Gestion des secrets

- **Aucun secret en clair** dans le code ni dans Git (vérifié par Gitleaks).
- **Identifiants Azure** stockés dans **GitHub Actions Secrets** (chiffrés au
  repos par GitHub, jamais exposés dans les logs).
- **Mot de passe PostgreSQL** généré aléatoirement par Terraform
  (`random_password`), marqué `sensitive`, jamais affiché. La chaîne de
  connexion est masquée dans les logs CI (`::add-mask::`) puis injectée dans un
  **Secret Kubernetes** par Helm — elle n'apparaît dans aucun manifeste versionné.
- **Évolution recommandée** : passer à un service principal + **OIDC**
  (federated credentials, sans mot de passe stocké) et centraliser les secrets
  applicatifs dans Azure Key Vault. Volontairement écarté ici pour garder un
  MVP léger.

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

- **Network Policies** fournies (`networkpolicy.yaml`, activables via
  `networkPolicy.enabled=true`) :
  - `default-deny-ingress` : tout est refusé par défaut dans le namespace ;
  - le backend n'accepte que l'ingress-nginx, le frontend et Prometheus ;
  - le frontend n'accepte que l'ingress-nginx.
  > Leur application nécessite un CNI compatible (Azure CNI / Calico). Le MVP
  > tourne en kubenet (léger) ; activer un CNI policy-enabled est l'évolution
  > prévue.
- **PostgreSQL** : accès public restreint au **pare-feu « services Azure »**
  (aucune connexion depuis l'Internet public) + **TLS obligatoire**
  (`sslmode=require`).

## 5. Chiffrement (TLS)

- **TLS de bout en bout** côté utilisateur : Ingress NGINX + **cert-manager**
  (certificats Let's Encrypt automatiques, redirection HTTPS forcée).
- **`sslmode=require`** sur la connexion à PostgreSQL.

## 6. Conformité (données de santé)

- Hébergement en **Poland Central** (Union européenne → RGPD).
- Données chiffrées **au repos** (chiffrement de plateforme Azure) et **en
  transit** (TLS, `sslmode=require`).
- **Sauvegardes** automatiques (PostgreSQL, 7 jours de rétention) — cf. PRA/PCA.
- **Journalisation** centralisée (Loki) pour la traçabilité des accès.
- *Note HDS* : pour un véritable hébergement de données de santé en production,
  basculer sur une région française et activer les services certifiés HDS
  d'Azure (identifié comme évolution).

## 7. Modèle de menaces (synthèse)

| Menace | Mitigation |
|---|---|
| Vol d'identifiants CI | Secrets chiffrés GitHub, masquage des logs (évolution : OIDC) |
| Image vulnérable déployée | Scan Trivy bloquant (CRITICAL) avant déploiement |
| Exposition de la base | Pare-feu « services Azure » + TLS obligatoire |
| Mouvement latéral dans le cluster | RBAC + NetworkPolicies (activables avec CNI compatible) |
| Fuite de secret dans Git | Gitleaks + secret DB jamais versionné |
| Élévation de privilèges conteneur | securityContext durci, non-root |
