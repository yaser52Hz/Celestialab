# src/physics/forces/potential.py
import numpy as np
from typing import List, Callable, Dict, Any, Optional  # ✅ Added Optional
from .base import Force
from ...core.body import CelestialBody

class PotentialForce(Force):
    """
    Force derived from a scalar potential.
    F = -∇Φ(r)
    """
    
    def __init__(
        self,
        potential_function: Callable,
        name: str = "Potential Force",
        params: Optional[Dict[str, Any]] = None,  # ✅ Now Optional is defined
        epsilon: float = 1e-8
    ):
        """
        Args:
            potential_function: Φ(r) where r is position vector
            name: Name of the force
            params: Parameters for the potential
            epsilon: Step size for numerical differentiation
        """
        self._name = name
        self.potential = potential_function
        self.params = params or {}
        self.epsilon = epsilon
    
    @property
    def name(self) -> str:
        return self._name
    
    def compute(self, bodies: List[CelestialBody], time: float = 0.0) -> List[np.ndarray]:
        forces = []
        
        for body in bodies:
            pos = body.position
            force = np.zeros(3)
            
            # Numerical gradient: F = -∇Φ
            for i in range(3):
                pos_plus = pos.copy()
                pos_minus = pos.copy()
                pos_plus[i] += self.epsilon
                pos_minus[i] -= self.epsilon
                
                phi_plus = self.potential(pos_plus, **self.params)
                phi_minus = self.potential(pos_minus, **self.params)
                
                force[i] = -(phi_plus - phi_minus) / (2 * self.epsilon)
            
            forces.append(force)
        
        return forces
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'PotentialForce',
            'name': self._name,
            'params': self.params
        }