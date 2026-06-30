"""Jeu de données de démonstration (idempotent).

Lancé via `python -m app.seed` ou le script scripts/seed-db.sh pour
peupler la base avant une démonstration.
"""

from datetime import date, datetime, timedelta

from app.database import Base, SessionLocal, engine
from app.models import AppareilAuditif, Patient, RendezVous, StatutRendezVous


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Patient).count() > 0:
            print("Base déjà peuplée, rien à faire.")
            return

        p1 = Patient(
            nom="Martin",
            prenom="Claire",
            email="claire.martin@example.com",
            telephone="0601020304",
            date_naissance=date(1955, 4, 12),
            notes="Presbyacousie bilatérale.",
        )
        p1.appareils = [
            AppareilAuditif(marque="Phonak", modele="Audeo Lumity", oreille="bilateral",
                            numero_serie="PH-1001", date_pose=date(2024, 1, 15)),
        ]
        p1.rendez_vous = [
            RendezVous(date_heure=datetime.now() + timedelta(days=7),
                       motif="Contrôle annuel", statut=StatutRendezVous.PLANIFIE),
        ]

        p2 = Patient(
            nom="Dubois",
            prenom="Henri",
            email="henri.dubois@example.com",
            telephone="0605060708",
            date_naissance=date(1948, 9, 30),
        )
        p2.appareils = [
            AppareilAuditif(marque="Oticon", modele="Real 1", oreille="droite",
                            numero_serie="OT-2002", date_pose=date(2023, 11, 3)),
        ]

        db.add_all([p1, p2])
        db.commit()
        print("Jeu de données de démonstration inséré.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
