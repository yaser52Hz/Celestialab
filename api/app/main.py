# api/app/main.py
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'physics-engine'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import simulations, websocket
from .config import settings

app = FastAPI(
    title="Celestial Mechanics API",
    description="N-body simulation with custom forces",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulations.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {
        "service": "Celestial Mechanics API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}