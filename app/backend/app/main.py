"""Point d'entrée de l'API Audioprothèse (FastAPI)."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.observability import (
    PrometheusMiddleware,
    configure_logging,
    metrics_endpoint,
)
from app.routers import health, patients, rendezvous

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    # En MVP, on crée le schéma au démarrage. En production, on utilise
    # les migrations Alembic (voir app/migrations).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API de gestion d'un cabinet d'audioprothèse (patients, appareils, rendez-vous).",
    lifespan=lifespan,
    # Doc exposée sous /api/* car l'Ingress ne route que /api et /metrics
    # vers le backend (le reste va au frontend).
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware)

app.include_router(health.router)
app.include_router(patients.router)
app.include_router(rendezvous.router)


@app.get("/metrics", include_in_schema=False)
def metrics():
    return metrics_endpoint()


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "version": "0.1.0",
        "docs": "/api/docs",
        "metrics": "/metrics",
    }
