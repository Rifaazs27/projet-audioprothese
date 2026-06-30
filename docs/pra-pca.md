# Plan de Reprise / Continuité d'Activité (PRA / PCA)

## 1. Objectifs

| Indicateur | Cible MVP |
|---|---|
| RPO (perte de données max) | ≤ 24 h (sauvegardes quotidiennes) |
| RTO (temps de reprise max) | ≤ 1 h (redéploiement automatisé) |

## 2. Sauvegardes

- **PostgreSQL Flexible Server** : sauvegardes automatiques chiffrées, rétention
  **7 jours** (`backup_retention_days = 7`). Restauration *point-in-time* native.
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
./scripts/seed-db.sh        # ou restauration de sauvegarde
```

### Scénario D — Mauvais déploiement applicatif
```bash
helm rollback audioprothese -n audioprothese     # retour à la révision précédente
```

## 4. Réplication (perspective)

Le cahier des charges évoque une réplication on-premise ↔ cloud. Pour le MVP
cloud, la résilience est assurée par les sauvegardes managées et l'IaC. Une
**géo-réplication** (`geo_redundant_backup_enabled = true`) et un second
cluster en région secondaire sont identifiés comme évolutions (coût × 2,
hors budget Student).

## 5. Tests du PRA

| Test | Fréquence | Méthode |
|---|---|---|
| Rollback Helm | À chaque release | `helm rollback` en staging |
| Restauration DB | Trimestriel | Restauration point-in-time sur serveur jetable |
| Reconstruction totale | Avant la soutenance | `deploy.sh` sur un RG neuf |

## 6. Runbooks

Les procédures opérationnelles détaillées sont dans
[`runbooks.md`](runbooks.md).
