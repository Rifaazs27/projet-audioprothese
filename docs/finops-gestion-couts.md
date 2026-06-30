# FinOps — Gestion des coûts (M2)

> Le compte Azure Student dispose de **85 $** de crédit, sans carte bancaire et
> sans renouvellement. La maîtrise des coûts est donc une contrainte de
> conception, pas une option. Ce document présente l'estimation, les leviers
> d'optimisation et les garde-fous mis en place.

## 1. Estimation des coûts mensuels

Région Poland Central, dimensionnement MVP. Tarifs indicatifs (USD, 2025).

| Ressource | SKU | Coût si allumé 24/7 | Levier |
|---|---|---|---|
| AKS — plan de contrôle | Free tier | **0 $** | Toujours gratuit |
| AKS — 1 nœud | Standard_B2s_v2 (2 vCPU / 8 Go) | ~30-35 $/mois | Burstable, éteignable |
| PostgreSQL Flexible | B_Standard_B1ms | ~13 $/mois | Burstable, le moins cher |
| Stockage PostgreSQL | 32 Go | ~4 $/mois | Minimum |
| Azure Container Registry | Basic | ~5 $/mois | SKU le plus bas |
| Storage Account (état Terraform) | Standard_LRS | ~0–1 $ | Négligeable |
| Load Balancer (Ingress) | Standard | ~3–4 $/mois | Mutualisé |
| Adresse IP publique | Standard | ~3 $/mois | 1 seule |
| **Total estimé 24/7** | | **~60-65 $/mois** | |

Avec extinction hors démonstration (voir §2), le coût réel tombe à
**quelques dollars par mois**, laissant largement de la marge sur les 85 $.

## 2. Leviers d'optimisation appliqués

1. **Plan de contrôle AKS gratuit** (`sku_tier = "Free"`) — pas de SLA payant.
2. **Un seul nœud B2s burstable** — facturation réduite, suffisant pour un MVP.
3. **SKU minimaux partout** : PostgreSQL B1ms, ACR Basic, Storage LRS.
4. **Loki au lieu d'ELK** : Elasticsearch nécessiterait plusieurs Go de RAM et
   du stockage indexé coûteux ; Loki n'indexe que les labels (économie majeure).
5. **Rétention courte** : métriques Prometheus 3 jours, logs Loki 72 h,
   sauvegardes DB 7 jours.
6. **Pas de haute disponibilité multi-zone** pour le MVP (HA = coût × 2).
7. **HPA borné** (`maxReplicas: 4`) : la scalabilité est plafonnée pour éviter
   toute dérive de coût.
8. **Destruction à la demande** : `scripts/teardown.sh` (`terraform destroy`)
   pour ne payer que pendant les démonstrations.
9. **Étiquetage (tags)** de toutes les ressources (`projet`, `cours`,
   `managed_by`) pour le suivi analytique dans Azure Cost Management.

## 3. Garde-fous automatiques

Un **budget Azure** (`infra/terraform/budget.tf`) déclenche des **alertes
e-mail** :

| Seuil | Type | Action attendue |
|---|---|---|
| 50 % | Coût réel | Vigilance |
| 80 % | Coût réel | Éteindre les ressources non nécessaires |
| 100 % | Prévision | Lancer `teardown.sh` immédiatement |

```hcl
# infra/terraform/variables.tf
variable "monthly_budget_amount" { default = 50 }   # plafond < crédit total
```

## 4. Procédure d'allumage / extinction

```bash
# Avant une démonstration
./scripts/deploy.sh

# Après la démonstration (réflexe FinOps)
./scripts/teardown.sh
```

Alternative sans tout détruire (conserver l'état, arrêter la facturation
compute) :

```bash
az aks stop  --name <aks> --resource-group <rg>   # stoppe les nœuds
az aks start --name <aks> --resource-group <rg>   # redémarre
```

## 5. Suivi dans Azure

- **Cost Management + Billing → Cost analysis** : filtrer par tag `projet`.
- Exporter le détail mensuel pour le rendu technique final.
- Vérifier le crédit restant : *Subscriptions → Azure for Students*.

## 6. Synthèse FinOps

| Principe FinOps | Mise en œuvre dans le projet |
|---|---|
| Visibilité | Tags + Cost Analysis + budget |
| Optimisation | SKU minimaux, Loki, rétention courte |
| Responsabilité | Alertes e-mail, teardown documenté |
| Élasticité maîtrisée | HPA borné, start/stop AKS |
