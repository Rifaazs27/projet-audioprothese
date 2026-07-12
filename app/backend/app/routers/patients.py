"""Endpoints REST pour les patients et leurs ressources liées."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[schemas.PatientRead])
def lister_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_patients(db, skip=skip, limit=limit)


@router.post("", response_model=schemas.PatientRead, status_code=status.HTTP_201_CREATED)
def creer_patient(data: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, data)


@router.get("/{patient_id}", response_model=schemas.PatientRead)
def obtenir_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient introuvable")
    return patient


@router.patch("/{patient_id}", response_model=schemas.PatientRead)
def modifier_patient(
    patient_id: int, data: schemas.PatientUpdate, db: Session = Depends(get_db)
):
    patient = crud.get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient introuvable")
    return crud.update_patient(db, patient, data)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient introuvable")
    crud.delete_patient(db, patient)


@router.post(
    "/{patient_id}/appareils",
    response_model=schemas.AppareilRead,
    status_code=status.HTTP_201_CREATED,
)
def ajouter_appareil(
    patient_id: int, data: schemas.AppareilCreate, db: Session = Depends(get_db)
):
    if crud.get_patient(db, patient_id) is None:
        raise HTTPException(status_code=404, detail="Patient introuvable")
    return crud.add_appareil(db, patient_id, data)


@router.post(
    "/{patient_id}/rendez-vous",
    response_model=schemas.RendezVousRead,
    status_code=status.HTTP_201_CREATED,
)
def ajouter_rendez_vous(
    patient_id: int, data: schemas.RendezVousCreate, db: Session = Depends(get_db)
):
    if crud.get_patient(db, patient_id) is None:
        raise HTTPException(status_code=404, detail="Patient introuvable")
    return crud.add_rendez_vous(db, patient_id, data)
