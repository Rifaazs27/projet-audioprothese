"""Endpoint de consultation globale des rendez-vous."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/rendez-vous", tags=["rendez-vous"])


@router.get("", response_model=list[schemas.RendezVousRead])
def lister_rendez_vous(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_rendez_vous(db, skip=skip, limit=limit)
