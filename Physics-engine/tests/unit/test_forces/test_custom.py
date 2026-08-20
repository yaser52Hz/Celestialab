# tests/unit/test_forces/test_custom.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.forces.custom import AnyForce

class TestCustomForce:
    """Test custom force"""
    
    def test_custom_force_basic(self):
        """Test basic custom force"""
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
    
    def test_custom_force_with_time(self):
        """Test custom force with time dependency"""
        def force_function(bodies, time):
            return [time * np.array([1.0, 0.0, 0.0]) for _ in bodies]
        
        force = AnyForce(force_function, name="Time Force")
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        # At time = 5.0
        accs = force.compute([body], time=5.0)
        assert np.allclose(accs[0], [5.0, 0.0, 0.0])