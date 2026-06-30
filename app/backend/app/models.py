"""Modèles ORM SQLAlchemy.

Domaine métier : un cabinet d'audioprothèse gère des patients, leurs
appareils auditifs et les rendez-vous de suivi.
"""

from __future__ import annotations

import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StatutRendezVous(enum.StrEnum):
    PLANIFIE = "planifie"
    HONORE = "honore"
    ANNULE = "annule"


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(120), index=True)
    prenom: Mapped[str] = mapped_column(String(120))
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    telephone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    date_naissance: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    cree_le: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    appareils: Mapped[list[AppareilAuditif]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    rendez_vous: Mapped[list[RendezVous]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )


class AppareilAuditif(Base):
    __tablename__ = "appareils_auditifs"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"), index=True
    )
    marque: Mapped[str] = mapped_column(String(120))
    modele: Mapped[str] = mapped_column(String(120))
    numero_serie: Mapped[str | None] = mapped_column(String(120), nullable=True)
    # oreille : gauche / droite / bilateral
    oreille: Mapped[str] = mapped_column(String(10), default="gauche")
    date_pose: Mapped[date | None] = mapped_column(Date, nullable=True)

    patient: Mapped[Patient] = relationship(back_populates="appareils")


class RendezVous(Base):
    __tablename__ = "rendez_vous"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"), index=True
    )
    date_heure: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    motif: Mapped[str] = mapped_column(String(255))
    statut: Mapped[StatutRendezVous] = mapped_column(
        Enum(StatutRendezVous), default=StatutRendezVous.PLANIFIE
    )

    patient: Mapped[Patient] = relationship(back_populates="rendez_vous")
