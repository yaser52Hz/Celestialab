# api/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# ============================================
# BODY MODELS
# ============================================

class BodyCreate(BaseModel):
    """Request model for creating a body"""
    name: str
    mass: float = Field(gt=0, description="Mass in kg")
    position: List[float] = Field(..., min_items=3, max_items=3)
    velocity: List[float] = Field(..., min_items=3, max_items=3)
    radius: float = 1.0
    color: str = "#ffffff"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Earth",
                "mass": 5.972e24,
                "position": [1.496e11, 0, 0],
                "velocity": [0, 2.978e4, 0],
                "radius": 6.371e6,
                "color": "#4B9CD3"
            }
        }

class BodyResponse(BaseModel):
    """Response model for a body"""
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
    """Request model for creating a custom force"""
    name: str
    force_function: str = Field(
        ..., 
        description="Python expression using position, velocity, mass, time, np"
    )
    params: Dict[str, Any] = {}
    description: str = ""
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Drag Force",
                "force_function": "-0.01 * velocity",
                "params": {},
                "description": "Linear drag force"
            }
        }

class ForceResponse(BaseModel):
    """Response model for a force"""
    name: str
    type: str
    params: Dict[str, Any] = {}
    description: str = ""

# ============================================
# SIMULATION MODELS
# ============================================

class SimulationCreate(BaseModel):
    """Request model for creating a simulation"""
    name: str = "My Simulation"
    dt: float = 3600.0
    integrator: str = "verlet"
    use_gravity: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Solar System",
                "dt": 3600.0,
                "integrator": "verlet",
                "use_gravity": True
            }
        }

class SimulationState(BaseModel):
    """Response model for simulation state"""
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
    """Summary for listing simulations"""
    id: str
    name: str
    created_at: datetime
    body_count: int
    time: float
    is_running: bool