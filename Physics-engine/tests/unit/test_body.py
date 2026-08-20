# tests/unit/test_body.py
import pytest
import numpy as np
from src.core.body import CelestialBody

class TestCelestialBody:
    """Test CelestialBody class"""
    
    def test_body_creation(self):
        """Test creating a body"""
        body = CelestialBody(
            name="Test",
            mass=100.0,
            position=[1.0, 2.0, 3.0],
            velocity=[0.1, 0.2, 0.3]
        )
        
        assert body.name == "Test"
        assert body.mass == 100.0
        assert np.allclose(body.position, [1.0, 2.0, 3.0])
        assert np.allclose(body.velocity, [0.1, 0.2, 0.3])
        assert body.id is not None
    
    def test_body_kinetic_energy(self):
        """Test kinetic energy calculation"""
        body = CelestialBody(
            name="Test",
            mass=2.0,
            position=[0, 0, 0],
            velocity=[3.0, 4.0, 0.0]  # speed = 5.0
        )
        
        # KE = 0.5 * m * v² = 0.5 * 2 * 25 = 25
        assert body.kinetic_energy() == 25.0
    
    def test_body_momentum(self):
        """Test momentum calculation"""
        body = CelestialBody(
            name="Test",
            mass=3.0,
            position=[0, 0, 0],
            velocity=[1.0, 2.0, 3.0]
        )
        
        momentum = body.momentum()
        assert np.allclose(momentum, [3.0, 6.0, 9.0])
    
    def test_body_serialization(self):
        """Test to_dict and from_dict"""
        body = CelestialBody(
            name="Test",
            mass=100.0,
            position=[1.0, 2.0, 3.0],
            velocity=[0.1, 0.2, 0.3],
            radius=5.0,
            color="#FF0000"
        )
        
        # Serialize
        data = body.to_dict()
        assert data['name'] == "Test"
        assert data['mass'] == 100.0
        assert data['position'] == [1.0, 2.0, 3.0]
        
        # Deserialize
        new_body = CelestialBody.from_dict(data)
        assert new_body.name == "Test"
        assert np.allclose(new_body.position, [1.0, 2.0, 3.0])
    
    def test_trail_update(self):
        """Test trail updating"""
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0, 0, 0],
            velocity=[1, 0, 0]
        )
        
        body.update_trail()
        assert len(body.trail) == 1
        assert np.allclose(body.trail[0], [0, 0, 0])
        
        body.position = np.array([1.0, 0, 0])
        body.update_trail()
        assert len(body.trail) == 2
        assert np.allclose(body.trail[1], [1.0, 0, 0])