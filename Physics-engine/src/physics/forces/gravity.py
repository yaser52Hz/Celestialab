# src/physics/forces/gravity.py
import numpy as np
from typing import List
from .base import Force
from ...core.body import CelestialBody
from ...core.constants import G

class GravityForce(Force):
    """Newtonian gravitational force."""
    
    def __init__(self, gravitational_constant: float = G, softening: float = 1e-6):
        self.G = gravitational_constant
        self.softening = softening
    
    @property
    def name(self) -> str:
        return f"Newtonian Gravity (G={self.G})"
    
    def compute(self, bodies: List[CelestialBody], time: float = 0.0) -> List[np.ndarray]:
        n = len(bodies)
        accelerations = [np.zeros(3, dtype=np.float64) for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                
                diff = bodies[j].position - bodies[i].position
                dist_sq = np.dot(diff, diff) + self.softening**2
                dist = np.sqrt(dist_sq)
                
                acc_mag = self.G * bodies[j].mass / (dist_sq * dist)
                accelerations[i] += acc_mag * diff
        
        return accelerations