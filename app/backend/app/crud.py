"""Opérations CRUD (couche d'accès aux données)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app import models, schemas


# ----- Patients -----
def list_patients(db: Session, skip: int = 0, limit: int = 100) -> list[models.Patient]:
    stmt = (
        select(models.Patient)
        .options(selectinload(models.Patient.appareils), selectinload(models.Patient.rendez_vous))
        .offset(skip)
        .limit(limit)
        .order_by(models.Patient.id)
    )
    return list(db.scalars(stmt))


def get_patient(db: Session, patient_id: int) -> models.Patient | None:
    stmt = (
        select(models.Patient)
        .options(selectinload(models.Patient.appareils), selectinload(models.Patient.rendez_vous))
        .where(models.Patient.id == patient_id)
    )
    return db.scalars(stmt).first()


def create_patient(db: Session, data: schemas.PatientCreate) -> models.Patient:
    patient = models.Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update_patient(
    db: Session, patient: models.Patient, data: schemas.PatientUpdate
) -> models.Patient:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(db: Session, patient: models.Patient) -> None:
    db.delete(patient)
    db.commit()


# ----- Appareils -----
def add_appareil(
    db: Session, patient_id: int, data: schemas.AppareilCreate
) -> models.AppareilAuditif:
    appareil = models.AppareilAuditif(patient_id=patient_id, **data.model_dump())
    db.add(appareil)
    db.commit()
    db.refresh(appareil)
    return appareil


# ----- Rendez-vous -----
def add_rendez_vous(
    db: Session, patient_id: int, data: schemas.RendezVousCreate
) -> models.RendezVous:
    rdv = models.RendezVous(patient_id=patient_id, **data.model_dump())
    db.add(rdv)
    db.commit()
    db.refresh(rdv)
    return rdv


def list_rendez_vous(db: Session, skip: int = 0, limit: int = 100) -> list[models.RendezVous]:
    stmt = (
        select(models.RendezVous)
        .offset(skip)
        .limit(limit)
        .order_by(models.RendezVous.date_heure)
    )
    return list(db.scalars(stmt))
