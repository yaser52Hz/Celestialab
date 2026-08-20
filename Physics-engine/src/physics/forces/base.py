# src/physics/forces/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import numpy as np
from ...core.body import CelestialBody

class Force(ABC):
    """
    Base class for any force in the simulation.
    Users can implement custom forces by subclassing this.
    """
    
    @abstractmethod
    def compute(
        self,
        bodies: List[CelestialBody],
        time: float = 0.0
    ) -> List[np.ndarray]:
        """
        Compute acceleration for each body.
        
        Args:
            bodies: List of celestial bodies
            time: Current simulation time
        
        Returns:
            List of acceleration vectors (m/s²) for each body
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the force"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize force to dictionary"""
        return {
            'type': self.__class__.__name__,
            'name': self.name
        }