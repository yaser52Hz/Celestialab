# tests/unit/test_forces/test_composite.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

import pytest
import numpy as np
from api.engine.core.body import CelestialBody
from api.engine.physics.forces.custom import AnyForce
from api.engine.physics.forces.composite import CompositeForce

class TestCompositeForce:
    def test_composite_basic(self):
        def force1(bodies, time, a=1.0):
            return [a * np.array([1.0, 0.0, 0.0]) for _ in bodies]
        
        def force2(bodies, time, b=2.0):
            return [b * np.array([0.0, 1.0, 0.0]) for _ in bodies]
        
        f1 = AnyForce(force1, name="Force1", params={'a': 1.0})
        f2 = AnyForce(force2, name="Force2", params={'b': 2.0})
        
        composite = CompositeForce([f1, f2], name="Combined")
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0, 0, 0],
            velocity=[0, 0, 0]
        )
        
        accs = composite.compute([body])
        assert np.allclose(accs[0], [1.0, 2.0, 0.0])