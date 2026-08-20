# tests/unit/test_forces/test_gravity.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.forces.gravity import GravityForce

class TestGravityForce:
    def test_two_body_gravity(self):
        # ✅ از gravitational_constant استفاده کنید، نه G
        gravity = GravityForce(gravitational_constant=1.0, softening=0.0)
        
        body1 = CelestialBody("A", 1.0, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        body2 = CelestialBody("B", 1.0, [1.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        
        accs = gravity.compute([body1, body2])
        
        assert np.allclose(accs[0], [1.0, 0.0, 0.0])
        assert np.allclose(accs[1], [-1.0, 0.0, 0.0])