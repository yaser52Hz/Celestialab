# tests/unit/test_forces/test_potential.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.forces.potential import PotentialForce

class TestPotentialForce:
    """Test potential-derived forces"""
    
    def test_harmonic_potential(self):
        """Test harmonic oscillator potential"""
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
        
        # F = -∇Φ = -k * x = -2.0
        assert np.allclose(accs[0], [-2.0, 0.0, 0.0], atol=1e-6)
    
    def test_kepler_potential(self):
        """Test Kepler (1/r) potential"""
        def kepler_potential(pos, mu=1.0):
            r = np.linalg.norm(pos)
            if r < 1e-10:
                return -1e10
            return -mu / r
        
        force = PotentialForce(
            kepler_potential,
            name="Kepler",
            params={'mu': 1.0}
        )
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[2.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        accs = force.compute([body])
        
        # F = -∇(-1/r) = -1/r² * r_hat = -1/4
        assert np.allclose(accs[0], [-0.25, 0.0, 0.0], atol=1e-6)
    
    def test_plummer_potential(self):
        """Test Plummer potential"""
        def plummer_potential(pos, M=1.0, a=1.0):
            r = np.linalg.norm(pos)
            return -M / np.sqrt(r**2 + a**2)
        
        force = PotentialForce(
            plummer_potential,
            name="Plummer",
            params={'M': 1.0, 'a': 1.0}
        )
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        accs = force.compute([body])
        
        # At r=0, force should be zero (softened)
        assert np.allclose(accs[0], [0.0, 0.0, 0.0], atol=1e-6)
    
    def test_potential_name(self):
        """Test potential force name"""
        def dummy_potential(pos):
            return 0.0
        
        force = PotentialForce(dummy_potential, name="My Potential")
        assert force.name == "My Potential"