def test_liveness(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_readiness(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"


def test_metrics_exposed(client):
    # Une requête d'abord pour générer une métrique.
    client.get("/healthz")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "http_requests_total" in resp.text


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "service" in resp.json()
