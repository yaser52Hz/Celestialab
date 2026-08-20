# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import simulations, websocket
from .config import settings

app = FastAPI(
    title="Celestial Mechanics Engine API",
    description="N-body simulation with custom forces",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(simulations.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {
        "service": "Celestial Mechanics Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}