# tests/unit/test_integrators/test_verlet.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.integrators.verlet import VerletIntegrator

class TestVerletIntegrator:
    """Test Verlet integrator"""
    
    def test_constant_acceleration(self):
        """Test constant acceleration: x = 0.5 * a * t²"""
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
        
        # x = 0.5 * a * t² = 0.5 * 1.0 * 1.0 = 0.5
        assert np.allclose(body.position[0], 0.5, atol=0.01)
        assert np.allclose(body.velocity[0], 1.0, atol=0.01)
    
    def test_energy_conservation(self):
        """Test Verlet conserves energy for harmonic oscillator"""
        integrator = VerletIntegrator()
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[1.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        dt = 0.01
        k = 1.0  # Spring constant
        
        # Simple harmonic oscillator force: a = -k * x
        def acceleration(bodies):
            return [-k * bodies[0].position]
        
        # Run many steps
        initial_energy = 0.5 * k * np.dot(body.position, body.position)
        energies = []
        
        for _ in range(1000):
            a = acceleration([body])
            integrator.step([body], a, dt)
            energy = 0.5 * k * np.dot(body.position, body.position) + 0.5 * np.dot(body.velocity, body.velocity)
            energies.append(energy)
        
        # Energy should be conserved (within 1%)
        energy_std = np.std(energies)
        assert energy_std / initial_energy < 0.01