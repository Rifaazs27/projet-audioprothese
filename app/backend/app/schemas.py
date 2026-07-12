"""Schémas Pydantic (validation entrée/sortie API)."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import StatutRendezVous


# ----- Appareil auditif -----
class AppareilBase(BaseModel):
    marque: str
    modele: str
    numero_serie: str | None = None
    oreille: str = "gauche"
    date_pose: date | None = None


class AppareilCreate(AppareilBase):
    pass


class AppareilRead(AppareilBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int


# ----- Rendez-vous -----
class RendezVousBase(BaseModel):
    date_heure: datetime
    motif: str
    statut: StatutRendezVous = StatutRendezVous.PLANIFIE


class RendezVousCreate(RendezVousBase):
    pass


class RendezVousRead(RendezVousBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int


# ----- Patient -----
class PatientBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr | None = None
    telephone: str | None = None
    date_naissance: date | None = None
    notes: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None
    date_naissance: date | None = None
    notes: str | None = None


class PatientRead(PatientBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cree_le: datetime
    appareils: list[AppareilRead] = []
    rendez_vous: list[RendezVousRead] = []
