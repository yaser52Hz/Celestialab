# tests/unit/test_forces/test_custom.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.forces.custom import AnyForce

class TestCustomForce:
    def test_custom_force_basic(self):
        def force_function(bodies, time, a=1.0):
            return [a * body.position for body in bodies]
        
        force = AnyForce(force_function, name="Test", params={'a': 2.0})
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[3.0, 4.0, 5.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        accs = force.compute([body])
        assert np.allclose(accs[0], [6.0, 8.0, 10.0])