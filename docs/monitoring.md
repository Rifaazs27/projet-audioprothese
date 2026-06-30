# Supervision & observabilité

La supervision repose sur les trois piliers du cahier des charges :
**métriques**, **logs** et **alerting**.

## 1. Métriques (Prometheus + Grafana)

Le backend FastAPI expose `/metrics` (middleware `app/observability.py`) :

| Métrique | Type | Usage |
|---|---|---|
| `http_requests_total{method,path,status}` | Counter | Débit, taux d'erreurs |
| `http_request_duration_seconds` | Histogram | Latence (p50/p95/p99) |
| `up{job="audioprothese-backend"}` | Gauge | Disponibilité |

- **En local** : Prometheus scrape `backend:8000` (cf. `docker-compose.yml`).
- **Sur le cluster** : un **ServiceMonitor** (`servicemonitor.yaml`) est
  découvert automatiquement par `kube-prometheus-stack`.

## 2. Dashboard Grafana

Un dashboard est provisionné automatiquement
(`monitoring/grafana/dashboards/audioprothese-overview.json`) :

- Débit de requêtes par route (req/s)
- Latence p95
- Taux d'erreurs 5xx
- Disponibilité du backend
- Logs applicatifs (panneau Loki)

> Pour le rendu technique final, exporter une capture d'écran du dashboard
> (exigence « Screenshot dashboard »).

## 3. Logs (Loki + Promtail)

- L'application émet des **logs structurés JSON** sur stdout.
- **Promtail** collecte les logs des conteneurs et les pousse vers **Loki**.
- Recherche/corrélation depuis Grafana (datasource Loki).

### Pourquoi Loki et non ELK ?
Le cahier des charges cite ELK (Elasticsearch/Logstash/Kibana). ELK est
puissant mais très gourmand (plusieurs Go de RAM, stockage indexé). Sur un
budget Student, **Loki** offre les mêmes usages (centralisation, recherche,
visualisation dans Grafana) pour une fraction du coût car il n'indexe que les
labels. Ce choix est un arbitrage **FinOps** assumé et documenté.

## 4. Alerting

Règles Prometheus (`monitoring/prometheus/alerts.yml`) :

| Alerte | Condition | Sévérité |
|---|---|---|
| `BackendDown` | `up == 0` pendant 1 min | critique |
| `TauxErreur5xxEleve` | > 5 % d'erreurs 5xx sur 5 min | warning |
| `LatenceElevee` | p95 > 1 s sur 5 min | warning |

Sur le cluster, Alertmanager (fourni par kube-prometheus-stack) route les
alertes ; un récepteur Slack/Teams/e-mail peut être branché (cf. cahier des
charges « alertes envoyées à l'équipe via Slack/Teams »).

## 5. Installation sur le cluster

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f monitoring/k8s/kube-prometheus-stack-values.yaml
helm install loki grafana/loki-stack \
  -n monitoring -f monitoring/k8s/loki-stack-values.yaml
```

Accès Grafana :

```bash
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3000:80
```

## 6. Traces (perspective)

Le cahier des charges mentionne Jaeger (traçage distribué). L'application étant
un monolithe API + SPA, le traçage distribué n'apporte pas de valeur immédiate
au MVP. L'instrumentation **OpenTelemetry** est identifiée comme axe d'évolution
(cf. `docs/backlog.md`).
