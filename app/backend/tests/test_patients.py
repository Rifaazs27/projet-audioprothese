def _patient_payload(**overrides):
    base = {
        "nom": "Durand",
        "prenom": "Sophie",
        "email": "sophie.durand@example.com",
        "telephone": "0612345678",
    }
    base.update(overrides)
    return base


def test_creer_et_lister_patient(client):
    resp = client.post("/api/patients", json=_patient_payload())
    assert resp.status_code == 201
    patient = resp.json()
    assert patient["id"] > 0
    assert patient["nom"] == "Durand"

    resp = client.get("/api/patients")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_obtenir_patient_inexistant(client):
    resp = client.get("/api/patients/9999")
    assert resp.status_code == 404


def test_cycle_complet_patient(client):
    pid = client.post("/api/patients", json=_patient_payload()).json()["id"]

    # Mise à jour
    resp = client.patch(f"/api/patients/{pid}", json={"telephone": "0700000000"})
    assert resp.status_code == 200
    assert resp.json()["telephone"] == "0700000000"

    # Ajout d'un appareil
    resp = client.post(
        f"/api/patients/{pid}/appareils",
        json={"marque": "Signia", "modele": "Pure", "oreille": "gauche"},
    )
    assert resp.status_code == 201
    assert resp.json()["marque"] == "Signia"

    # Ajout d'un rendez-vous
    resp = client.post(
        f"/api/patients/{pid}/rendez-vous",
        json={"date_heure": "2026-09-01T10:00:00", "motif": "Réglage"},
    )
    assert resp.status_code == 201

    # Vérification des ressources liées
    resp = client.get(f"/api/patients/{pid}")
    body = resp.json()
    assert len(body["appareils"]) == 1
    assert len(body["rendez_vous"]) == 1

    # Liste globale des rendez-vous
    resp = client.get("/api/rendez-vous")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # Suppression
    resp = client.delete(f"/api/patients/{pid}")
    assert resp.status_code == 204
    assert client.get(f"/api/patients/{pid}").status_code == 404


def test_validation_email_invalide(client):
    resp = client.post("/api/patients", json=_patient_payload(email="pas-un-email"))
    assert resp.status_code == 422
