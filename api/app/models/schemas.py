# api/app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================
# BODY MODELS
# ============================================

class BodyCreate(BaseModel):
    name: str
    mass: float = Field(gt=0)
    position: List[float] = Field(..., min_items=3, max_items=3)
    velocity: List[float] = Field(..., min_items=3, max_items=3)
    radius: float = 1.0
    color: str = "#ffffff"


class BodyResponse(BaseModel):
    id: str
    name: str
    mass: float
    position: List[float]
    velocity: List[float]
    radius: float
    color: str
    trail: List[List[float]] = []


# ============================================
# FORCE MODELS
# ============================================

class ForceCreate(BaseModel):
    name: str
    force_function: str
    params: Dict[str, Any] = {}
    description: str = ""


class ForceResponse(BaseModel):
    name: str
    type: str
    params: Dict[str, Any] = {}
    description: str = ""


# ============================================
# SIMULATION MODELS
# ============================================

class SimulationCreate(BaseModel):
    name: str = "My Simulation"
    dt: float = 3600.0
    integrator: str = "verlet"
    use_gravity: bool = True


class SimulationState(BaseModel):
    id: str
    name: str
    time: float
    step_count: int
    bodies: List[BodyResponse]
    total_energy: Optional[Dict[str, float]] = None
    total_momentum: Optional[List[float]] = None
    center_of_mass: Optional[List[float]] = None
    is_running: bool
    forces: List[ForceResponse] = []


class SimulationSummary(BaseModel):
    id: str
    name: str
    created_at: datetime
    body_count: int
    time: float
    is_running: bool