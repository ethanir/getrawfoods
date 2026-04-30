"""FastAPI entry point.

CORS is configured for the Vite dev server (http://localhost:5173). The
allowed origins list will widen in production deployment, where the
frontend will live on a real hostname.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import categories, farms, health

app = FastAPI(
    title="GetRawFoods API",
    description="A community-driven sourcing directory for raw foods.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(farms.router, prefix="/api", tags=["farms"])
