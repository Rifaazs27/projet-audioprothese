"""Sondes de santé pour Kubernetes (liveness/readiness)."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(tags=["health"])


@router.get("/healthz")
def liveness() -> dict[str, str]:
    """Liveness : l'application répond."""
    return {"status": "ok"}


@router.get("/readyz")
def readiness(db: Session = Depends(get_db)) -> dict[str, str]:
    """Readiness : la base de données est joignable."""
    db.execute(text("SELECT 1"))
    return {"status": "ready"}
