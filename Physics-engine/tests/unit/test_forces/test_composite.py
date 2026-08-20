# src/physics/forces/composite.py
import numpy as np
from typing import List
from ....src.physics.forces.base import Force
from ....src.core.body import CelestialBody

class CompositeForce(Force):
    """
    Combine multiple forces into one.
    Total force = sum of all forces.
    """
    
    def __init__(self, forces: List[Force], name: str = "Composite Force"):
        self.forces = forces
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def compute(self, bodies: List[CelestialBody], time: float = 0.0) -> List[np.ndarray]:
        n = len(bodies)
        total_accs = [np.zeros(3) for _ in range(n)]
        
        for force in self.forces:
            accs = force.compute(bodies, time)
            for i in range(n):
                total_accs[i] += accs[i]
        
        return total_accs
    
    def add_force(self, force: Force) -> None:
        """Add another force to the composite"""
        self.forces.append(force)
    
    def to_dict(self) -> dict:
        return {
            'type': 'CompositeForce',
            'name': self._name,
            'forces': [f.to_dict() for f in self.forces]
        }