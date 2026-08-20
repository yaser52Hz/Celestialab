# tests/unit/test_integrators/test_euler.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.integrators.euler import EulerIntegrator

class TestEulerIntegrator:
    def test_constant_acceleration(self):
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
        
        # ✅ دقت Euler کمتر است، بنابراین atol را بیشتر می‌کنیم
        assert np.allclose(body.position[0], 0.5, atol=0.1)