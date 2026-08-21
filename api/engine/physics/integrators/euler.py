# src/physics/integrators/euler.py
import numpy as np
from typing import List
from .base import Integrator
from ...core.body import CelestialBody

class EulerIntegrator(Integrator):
    """Euler integrator - 1st order"""
    
    @property
    def name(self) -> str:
        return "Euler"
    
    @property
    def order(self) -> int:
        return 1
    
    def step(
        self,
        bodies: List[CelestialBody],
        accelerations: List[np.ndarray],
        dt: float
    ) -> None:
        for i, body in enumerate(bodies):
            # Update velocity first
            body.velocity = body.velocity + accelerations[i] * dt
            # Then update position with new velocity
            body.position = body.position + body.velocity * dt