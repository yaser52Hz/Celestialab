# tests/unit/test_forces/test_potential.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

import pytest
import numpy as np
from api.engine.core.body import CelestialBody
from api.engine.physics.forces.potential import PotentialForce

class TestPotentialForce:
    def test_harmonic_potential(self):
        def harmonic_potential(pos, k=1.0):
            return 0.5 * k * np.dot(pos, pos)
        
        force = PotentialForce(
            harmonic_potential,
            name="Harmonic",
            params={'k': 1.0}
        )
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[2.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        accs = force.compute([body])
        assert np.allclose(accs[0], [-2.0, 0.0, 0.0], atol=1e-6)