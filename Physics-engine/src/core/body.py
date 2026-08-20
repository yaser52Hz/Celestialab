# src/core/body.py
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4

@dataclass
class CelestialBody:
    """
    Represents a celestial body in the simulation.
    
    Attributes:
        name: Body name
        mass: Mass in kg
        position: 3D position vector [x, y, z] in meters
        velocity: 3D velocity vector [vx, vy, vz] in m/s
        radius: Visual radius in meters
        color: Color for rendering (hex format)
        id: Unique identifier (auto-generated)
        prev_position: Previous position for Verlet integration
        trail: List of historical positions
        max_trail_length: Maximum trail length
        charge: Electric charge (for Lorentz force, optional)
    """
    name: str
    mass: float
    position: np.ndarray
    velocity: np.ndarray
    radius: float = 1.0
    color: str = "#ffffff"
    id: str = field(default_factory=lambda: str(uuid4()))
    prev_position: Optional[np.ndarray] = None
    trail: List[np.ndarray] = field(default_factory=list)
    max_trail_length: int = 1000
    charge: float = 0.0  # Optional for electromagnetic forces
    custom_properties: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure position and velocity are numpy arrays"""
        self.position = np.array(self.position, dtype=np.float64)
        self.velocity = np.array(self.velocity, dtype=np.float64)
        
        if self.prev_position is None:
            self.prev_position = self.position.copy()
    
    def update_trail(self):
        """Add current position to trail"""
        self.trail.append(self.position.copy())
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'mass': self.mass,
            'position': self.position.tolist(),
            'velocity': self.velocity.tolist(),
            'radius': self.radius,
            'color': self.color,
            'charge': self.charge,
            'trail': [p.tolist() for p in self.trail[-100:]],  # Last 100 points
            'custom_properties': self.custom_properties
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CelestialBody':
        """Create body from dictionary"""
        return cls(
            name=data['name'],
            mass=data['mass'],
            position=np.array(data['position']),
            velocity=np.array(data['velocity']),
            radius=data.get('radius', 1.0),
            color=data.get('color', '#ffffff'),
            id=data.get('id', str(uuid4())),
            charge=data.get('charge', 0.0),
            custom_properties=data.get('custom_properties', {})
        )
    
    def kinetic_energy(self) -> float:
        """Calculate kinetic energy"""
        return 0.5 * self.mass * np.dot(self.velocity, self.velocity)
    
    def momentum(self) -> np.ndarray:
        """Calculate linear momentum"""
        return self.mass * self.velocity