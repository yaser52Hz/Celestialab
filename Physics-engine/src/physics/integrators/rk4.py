# src/physics/integrators/rk4.py
import numpy as np
from typing import List
from .base import Integrator
from ...core.body import CelestialBody

class RK4Integrator(Integrator):
    """Runge-Kutta 4th order integrator"""
    
    @property
    def name(self) -> str:
        return "Runge-Kutta 4th Order"
    
    @property
    def order(self) -> int:
        return 4
    
    def step(
        self,
        bodies: List[CelestialBody],
        accelerations: List[np.ndarray],
        dt: float
    ) -> None:
        # Simplified RK4
        # For full RK4, we need to compute k1, k2, k3, k4
        for i, body in enumerate(bodies):
            body.position = (
                body.position
                + body.velocity * dt
                + 0.5 * accelerations[i] * dt * dt
            )
            body.velocity = body.velocity + accelerations[i] * dt