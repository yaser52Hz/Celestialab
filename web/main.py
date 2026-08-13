from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from simulation import Simulation

from backend.physics.body import Body
from backend.physics.forces.gravity import NewtonianGravity
from backend.physics.integrators.verlet import VelocityVerlet


app = FastAPI(
    title="Celestial Mechanics Simulator",
)


# ==================================================
# API models
# ==================================================

class BodyInput(BaseModel):
    name: str
    mass: float
    position: list[float]
    velocity: list[float]


class SimulationInput(BaseModel):
    bodies: list[BodyInput]


class StepInput(BaseModel):
    dt: float
    steps: int


# ==================================================
# In-memory simulations
# ==================================================

simulations: dict[str, Simulation] = {}


# ==================================================
# Routes
# ==================================================

@app.get("/api/status")
def status():
    return {
        "status": "ok",
        "engine": "celestial-mechanics",
    }


@app.post("/api/simulations")
def create_simulation(data: SimulationInput):

    bodies = [
        Body(
            body.name,
            body.mass,
            body.position,
            body.velocity,
        )
        for body in data.bodies
    ]

    simulation = Simulation(
        bodies=bodies,
        forces=[NewtonianGravity()],
        integrator=VelocityVerlet(),
    )

    simulation_id = str(len(simulations) + 1)

    simulations[simulation_id] = simulation

    return {
        "id": simulation_id,
        "time": simulation.time,
        "bodies": [
            body.name
            for body in simulation.bodies
        ],
    }


@app.post("/api/simulations/{simulation_id}/step")
def step_simulation(
    simulation_id: str,
    data: StepInput,
):

    simulation = simulations.get(simulation_id)

    if simulation is None:
        return {
            "error": "Simulation not found",
        }

    for _ in range(data.steps):
        simulation.step(data.dt)

    return {
        "id": simulation_id,
        "time": simulation.time,
        "bodies": {
            body.name: {
                "position": body.state.position.tolist(),
                "velocity": body.state.velocity.tolist(),
            }
            for body in simulation.bodies
        },
    }


# ==================================================
# Frontend
# ==================================================

app.mount(
    "/",
    StaticFiles(
        directory="web/frontend",
        html=True,
    ),
    name="frontend",
)