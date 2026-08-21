# src/physics/forces/custom.py
import numpy as np
from typing import List, Callable, Dict, Any, Optional
from .base import Force
from ...core.body import CelestialBody

class AnyForce(Force):
    """Completely custom force defined by user function."""
    
    def __init__(
        self,
        force_function: Callable,
        name: str = "Custom Force",
        params: Optional[Dict[str, Any]] = None,
        description: str = ""
    ):
        self._name = name
        self.force_function = force_function
        self.params = params or {}
        self.description = description
    
    @property
    def name(self) -> str:
        return self._name
    
    def compute(self, bodies: List[CelestialBody], time: float = 0.0) -> List[np.ndarray]:
        return self.force_function(bodies, time, **self.params)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'AnyForce',
            'name': self._name,
            'params': self.params,
            'description': self.description
        }