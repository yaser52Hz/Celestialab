# tests/unit/test_forces/test_gravity.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.forces.gravity import GravityForce

class TestGravityForce:
    """Test gravity force"""
    
    def test_gravity_two_bodies(self):
        """Test gravity between two bodies"""
        gravity = GravityForce(G=1.0, softening=0.0)
        
        body1 = CelestialBody(
            name="A",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        body2 = CelestialBody(
            name="B",
            mass=1.0,
            position=[1.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        accs = gravity.compute([body1, body2])
        
        # F = G * m1 * m2 / r² = 1 * 1 * 1 / 1 = 1
        # a = F / m = 1
        assert np.allclose(accs[0], [1.0, 0.0, 0.0])  # Body1 pulled toward body2
        assert np.allclose(accs[1], [-1.0, 0.0, 0.0])  # Body2 pulled toward body1
    
    def test_gravity_softening(self):
        """Test softening prevents singularities"""
        gravity = GravityForce(G=1.0, softening=1e-6)
        
        body1 = CelestialBody(
            name="A",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        body2 = CelestialBody(
            name="B",
            mass=1.0,
            position=[0.0, 0.0, 0.0],  # Same position
            velocity=[0.0, 0.0, 0.0]
        )
        
        accs = gravity.compute([body1, body2])
        
        # Should not be infinite
        assert np.all(np.isfinite(accs[0]))
        assert np.all(np.isfinite(accs[1]))