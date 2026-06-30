# Plan de Reprise / Continuité d'Activité (PRA / PCA)

## 1. Objectifs

| Indicateur | Cible MVP |
|---|---|
| RPO (perte de données max) | ≤ 24 h (sauvegardes quotidiennes) |
| RTO (temps de reprise max) | ≤ 1 h (redéploiement automatisé) |

## 2. Sauvegardes

- **PostgreSQL Flexible Server** : sauvegardes automatiques managées, rétention
  **7 jours** (`backup_retention_days = 7`). Restauration *point-in-time* native.
- **Sauvegardes applicatives vers MinIO (on-prem)** : un playbook Ansible
  (`ansible/playbooks/backup.yml`) réalise un `pg_dump` et le pousse dans un
  bucket **MinIO chiffré** (SSE-S3) hébergé sur la VM on-premise simulée. Cela
  matérialise la **réplication cloud → on-premise** et le stockage MinIO
  chiffré du cahier des charges. Planifié quotidiennement par le workflow
  `.github/workflows/backup.yml`.
- **Infrastructure** : entièrement reproductible via Terraform (`infra/terraform`).
  L'état (`tfstate`) est stocké de façon distante et versionnée.
- **Images applicatives** : conservées et taguées dans Azure Container Registry.
- **Configuration** : versionnée dans Git (manifestes Helm, valeurs, workflows).

## 3. Scénarios et procédures de reprise

### Scénario A — Panne d'un pod / nœud
- **Automatique** : Kubernetes redémarre les pods (sondes liveness/readiness),
  le HPA et le ReplicaSet maintiennent le nombre de répliques.
- Aucune action manuelle requise (auto-réparation).

### Scénario B — Corruption / perte de données
```bash
# Restauration point-in-time PostgreSQL
az postgres flexible-server restore \
  --resource-group <rg> --name <nouveau-serveur> \
  --source-server <serveur> --restore-time "2026-06-30T10:00:00Z"
```
Puis relancer le workflow *Deploy* : la nouvelle chaîne de connexion est
régénérée par Terraform et réinjectée dans le Secret Kubernetes.

### Scénario C — Perte complète de l'environnement
```bash
./scripts/deploy.sh         # recrée toute l'infra + déploie (RTO ~30-45 min)
# Restauration des données depuis MinIO (on-prem) via Ansible :
cd ansible && ansible-playbook playbooks/restore.yml \
  -e database_dsn="<dsn psql>" -e minio_root_user=... -e minio_root_password=...
```
La restauration est aussi disponible en un clic via le workflow
*Backup* → `restore` (Actions GitHub).

### Scénario D — Mauvais déploiement applicatif
```bash
helm rollback audioprothese -n audioprothese     # retour à la révision précédente
```

## 4. Réplication cloud ↔ on-premise

La réplication des données du cloud vers l'on-premise est assurée par les
sauvegardes `pg_dump` poussées vers **MinIO** sur la VM on-prem (cf. §2). Pour
aller plus loin, une **géo-réplication** Azure (`geo_redundant_backup_enabled`)
et un second cluster en région secondaire sont identifiés comme évolutions
(coût × 2, hors budget Student).

## 5. Tests du PRA

| Test | Fréquence | Méthode |
|---|---|---|
| Rollback Helm | À chaque release | `helm rollback` en staging |
| Restauration DB | Trimestriel | Restauration point-in-time sur serveur jetable |
| Reconstruction totale | Avant la soutenance | `deploy.sh` sur un RG neuf |

## 6. Runbooks

Les procédures opérationnelles détaillées sont dans
[`runbooks.md`](runbooks.md).
