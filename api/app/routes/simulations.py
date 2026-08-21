# api/app/routes/simulations.py
from fastapi import APIRouter, HTTPException
from typing import List

from ..models.schemas import (
    SimulationCreate, SimulationState, SimulationSummary,
    BodyCreate, BodyResponse, ForceCreate, ForceResponse
)
from ..services.simulation_manager import SimulationManager

router = APIRouter(prefix="/api/v1/simulations", tags=["simulations"])
manager = SimulationManager()


@router.post("/", response_model=dict)
async def create_simulation(config: SimulationCreate):
    sim_id = manager.create(config.model_dump())
    return {"id": sim_id, "message": "Simulation created"}


@router.get("/", response_model=List[SimulationSummary])
async def list_simulations():
    return manager.list()


@router.delete("/{sim_id}")
async def delete_simulation(sim_id: str):
    if not manager.delete(sim_id):
        raise HTTPException(404, "Simulation not found")
    return {"message": "Simulation deleted"}


@router.get("/{sim_id}", response_model=SimulationState)
async def get_state(sim_id: str):
    state = manager.get_state(sim_id)
    if not state:
        raise HTTPException(404, "Simulation not found")
    return state


@router.post("/{sim_id}/bodies")
async def add_body(sim_id: str, body: BodyCreate):
    if not manager.add_body(sim_id, body.model_dump()):
        raise HTTPException(404, "Simulation not found")
    return {"message": "Body added"}


@router.delete("/{sim_id}/bodies/{body_id}")
async def remove_body(sim_id: str, body_id: str):
    if not manager.remove_body(sim_id, body_id):
        raise HTTPException(404, "Body or simulation not found")
    return {"message": "Body removed"}


@router.post("/{sim_id}/forces")
async def add_force(sim_id: str, force: ForceCreate):
    if not manager.add_force(sim_id, force.model_dump()):
        raise HTTPException(404, "Simulation not found")
    return {"message": f"Force '{force.name}' added"}


@router.post("/{sim_id}/start")
async def start_simulation(sim_id: str):
    if not manager.start(sim_id):
        raise HTTPException(404, "Simulation not found")
    return {"message": "Simulation started"}


@router.post("/{sim_id}/stop")
async def stop_simulation(sim_id: str):
    if not manager.stop(sim_id):
        raise HTTPException(404, "Simulation not found")
    return {"message": "Simulation stopped"}


@router.post("/{sim_id}/step")
async def step_simulation(sim_id: str, steps: int = 1):
    if not manager.step(sim_id, steps):
        raise HTTPException(404, "Simulation not found or not running")
    return {"message": f"Executed {steps} steps"}


@router.post("/{sim_id}/clear")
async def clear_simulation(sim_id: str):
    if not manager.clear(sim_id):
        raise HTTPException(404, "Simulation not found")
    return {"message": "Simulation cleared"}