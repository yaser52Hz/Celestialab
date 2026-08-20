# src/physics/forces/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import numpy as np
from ...core.body import CelestialBody

class Force(ABC):
    """Base class for any force in the simulation."""
    
    @abstractmethod
    def compute(
        self,
        bodies: List[CelestialBody],
        time: float = 0.0
    ) -> List[np.ndarray]:
        """Compute acceleration for each body."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the force"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.__class__.__name__,
            'name': self.name
        }