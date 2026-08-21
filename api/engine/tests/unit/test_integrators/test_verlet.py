# tests/unit/test_integrators/test_verlet.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

import pytest
import numpy as np
from api.engine.core.body import CelestialBody
from api.engine.physics.integrators.verlet import VerletIntegrator

class TestVerletIntegrator:
    def test_constant_acceleration(self):
        integrator = VerletIntegrator()
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        dt = 0.1
        a = np.array([1.0, 0.0, 0.0])
        accelerations = [a]
        
        # Run 10 steps
        for _ in range(10):
            integrator.step([body], accelerations, dt)
        
        assert np.allclose(body.position[0], 0.5, atol=0.5)
    
    def test_energy_conservation(self):
        integrator = VerletIntegrator()
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[1.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        dt = 0.01
        k = 1.0
        
        def acceleration(bodies):
            return [-k * bodies[0].position]
        
        initial_energy = 0.5 * k * np.dot(body.position, body.position)
        energies = []
        
        for _ in range(1000):
            a = acceleration([body])
            integrator.step([body], a, dt)
            energy = 0.5 * k * np.dot(body.position, body.position) + 0.5 * np.dot(body.velocity, body.velocity)
            energies.append(energy)
        
        energy_std = np.std(energies)
        assert energy_std / initial_energy < 0.05