# Runbooks — procédures d'exploitation

Procédures opérationnelles courantes. Toutes supposent `kubectl` configuré sur
le cluster AKS (`az aks get-credentials ...`).

## Diagnostic général

```bash
kubectl get pods -n audioprothese
kubectl get events -n audioprothese --sort-by=.lastTimestamp
kubectl logs -n audioprothese -l component=backend --tail=100
```

## L'application ne répond pas (502/503)

1. Vérifier les pods backend : `kubectl get pods -n audioprothese`.
2. Inspecter un pod en échec : `kubectl describe pod <pod> -n audioprothese`.
3. Vérifier la readiness DB : `kubectl exec <pod> -n audioprothese -- \
   wget -qO- localhost:8000/readyz`.
4. Vérifier l'Ingress : `kubectl describe ingress audioprothese -n audioprothese`.

## La base de données est injoignable

1. Vérifier le secret : `kubectl get secret audioprothese-db -n audioprothese`.
2. Vérifier le serveur : `az postgres flexible-server show -g <rg> -n <srv>`.
3. Vérifier la résolution DNS privée et le sous-réseau délégué.

## Déployer une nouvelle version

```bash
# Via CI : pousser un tag v* ou lancer le workflow "CD — Build & Deploy".
# Manuellement :
helm upgrade --install audioprothese k8s/helm/audioprothese \
  -n audioprothese --set image.registry=<acr> --set image.tag=<sha> --wait
```

## Revenir en arrière (rollback)

```bash
helm history audioprothese -n audioprothese
helm rollback audioprothese <revision> -n audioprothese
```

## Mettre à l'échelle

```bash
# Automatique via HPA (CPU 70%). Manuel :
kubectl scale deployment/backend -n audioprothese --replicas=3
```

## Accéder aux tableaux de bord

```bash
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3000:80
# http://localhost:3000
```

## Arrêt / reprise (FinOps)

```bash
az aks stop  -g <rg> -n <aks>     # stoppe la facturation compute
az aks start -g <rg> -n <aks>     # reprise
./scripts/teardown.sh             # destruction complète
```

## Rotation d'un secret

```bash
az keyvault secret set --vault-name <kv> --name database-url --value "<nouvelle valeur>"
kubectl rollout restart deployment/backend -n audioprothese
```
