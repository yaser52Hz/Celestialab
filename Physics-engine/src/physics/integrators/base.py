# src/physics/integrators/base.py
from abc import ABC, abstractmethod
from typing import List
import numpy as np
from ...core.body import CelestialBody

class Integrator(ABC):
    """Base class for numerical integrators"""
    
    @abstractmethod
    def step(
        self,
        bodies: List[CelestialBody],
        accelerations: List[np.ndarray],
        dt: float
    ) -> None:
        """
        Perform one integration step.
        
        Args:
            bodies: List of celestial bodies
            accelerations: Current accelerations for each body
            dt: Time step
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the integration method"""
        pass
    
    @property
    @abstractmethod
    def order(self) -> int:
        """Order of accuracy"""
        pass