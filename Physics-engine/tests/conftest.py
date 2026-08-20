# tests/conftest.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation
from src.core.constants import G, AU

@pytest.fixture
def earth_body():
    """Create an Earth-like body"""
    return CelestialBody(
        name="Earth",
        mass=5.972e24,
        position=np.array([AU, 0.0, 0.0]),
        velocity=np.array([0.0, 2.978e4, 0.0]),
        radius=6.371e6,
        color="#4B9CD3"
    )

@pytest.fixture
def sun_body():
    """Create a Sun-like body"""
    return CelestialBody(
        name="Sun",
        mass=1.989e30,
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        radius=6.96e8,
        color="#FDB813"
    )

@pytest.fixture
def two_body_system(sun_body, earth_body):
    """Create a two-body system (Sun + Earth)"""
    sim = Simulation(dt=3600.0, integrator='verlet')
    sim.add_body(sun_body)
    sim.add_body(earth_body)
    return sim

@pytest.fixture
def three_body_system():
    """Create a three-body system (figure-8 configuration)"""
    sim = Simulation(dt=0.01, integrator='verlet', use_gravity=True)
    
    # Three equal masses in a figure-8 configuration
    bodies = [
        CelestialBody(
            name="A", 
            mass=1.0, 
            position=[-0.5, 0.0, 0.0], 
            velocity=[0.0, 0.5, 0.0]
        ),
        CelestialBody(
            name="B", 
            mass=1.0, 
            position=[0.5, 0.0, 0.0], 
            velocity=[0.0, -0.5, 0.0]
        ),
        CelestialBody(
            name="C", 
            mass=1.0, 
            position=[0.0, 0.0, 0.0], 
            velocity=[0.0, 0.0, 0.0]
        )
    ]
    
    for body in bodies:
        sim.add_body(body)
    
    return sim