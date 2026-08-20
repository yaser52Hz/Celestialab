# tests/unit/test_integrators/test_euler.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.integrators.euler import EulerIntegrator

class TestEulerIntegrator:
    """Test Euler integrator"""
    
    def test_constant_acceleration(self):
        """Test constant acceleration: x = 0.5 * a * t²"""
        integrator = EulerIntegrator()
        
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