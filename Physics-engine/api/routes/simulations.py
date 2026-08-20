# api/routes/simulations.py
from fastapi import APIRouter, HTTPException
from typing import List

from ..models.schemas import (
    SimulationCreate,
    SimulationState,
    SimulationSummary,
    BodyCreate,
    BodyResponse,
    ForceCreate,
    ForceResponse
)
from ..services.simulation_manager import SimulationManager

router = APIRouter(prefix="/api/v1/simulations", tags=["simulations"])
manager = SimulationManager()


@router.post("/", response_model=dict)
async def create_simulation(config: SimulationCreate):
    """Create a new simulation"""
    sim_id = manager.create_simulation(config.model_dump())
    return {"id": sim_id, "message": "Simulation created successfully"}


@router.get("/", response_model=List[SimulationSummary])
async def list_simulations():
    """List all simulations"""
    return manager.get_simulations()


@router.delete("/{sim_id}")
async def delete_simulation(sim_id: str):
    """Delete a simulation"""
    success = manager.delete_simulation(sim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return {"message": "Simulation deleted"}


@router.get("/{sim_id}", response_model=SimulationState)
async def get_simulation_state(sim_id: str):
    """Get simulation state"""
    state = manager.get_state(sim_id)
    if not state:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return state


@router.post("/{sim_id}/bodies", response_model=dict)
async def add_body(sim_id: str, body: BodyCreate):
    """Add a body to simulation"""
    success = manager.add_body(sim_id, body.model_dump())
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return {"message": "Body added successfully"}


@router.delete("/{sim_id}/bodies/{body_id}")
async def remove_body(sim_id: str, body_id: str):
    """Remove a body from simulation"""
    success = manager.remove_body(sim_id, body_id)
    if not success:
        raise HTTPException(status_code=404, detail="Body or simulation not found")
    return {"message": "Body removed"}


@router.post("/{sim_id}/forces", response_model=dict)
async def add_force(sim_id: str, force: ForceCreate):
    """Add a custom force to simulation"""
    success = manager.add_force(sim_id, force.model_dump())
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return {"message": f"Force '{force.name}' added successfully"}


@router.post("/{sim_id}/start")
async def start_simulation(sim_id: str):
    """Start the simulation"""
    success = manager.start_simulation(sim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return {"message": "Simulation started"}


@router.post("/{sim_id}/stop")
async def stop_simulation(sim_id: str):
    """Stop the simulation"""
    success = manager.stop_simulation(sim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return {"message": "Simulation stopped"}


@router.post("/{sim_id}/step")
async def step_simulation(sim_id: str, steps: int = 1):
    """Execute steps manually"""
    success = manager.step_simulation(sim_id, steps)
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return {"message": f"Executed {steps} steps"}


@router.post("/{sim_id}/clear")
async def clear_simulation(sim_id: str):
    """Clear all bodies from simulation"""
    success = manager.clear_simulation(sim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return {"message": "Simulation cleared"}