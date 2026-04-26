"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import farms
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hooks. Currently a no-op; place to wire up Redis, etc. later."""
    yield


app = FastAPI(
    title="GetRawFoods API",
    description=(
        "Community knowledge base for primal/raw food sourcing. "
        "Public read endpoints; write endpoints arrive with auth in Phase 3."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health() -> dict:
    """Liveness probe."""
    return {"status": "ok", "environment": settings.environment}


app.include_router(farms.router)
