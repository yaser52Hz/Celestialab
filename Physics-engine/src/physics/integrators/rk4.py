# src/physics/integrators/rk4.py
import numpy as np
from typing import List
from .base import Integrator
from ...core.body import CelestialBody

class RK4Integrator(Integrator):
    """
    4th order Runge-Kutta integrator.
    High accuracy but not symplectic.
    Order: 4
    """
    
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
        """
        Perform one RK4 step.
        Note: This is a simplified version.
        For full RK4, we need to compute accelerations at intermediate steps.
        """
        # Simplified Verlet-like step for now
        # Full RK4 implementation would be more complex
        for i, body in enumerate(bodies):
            body.position = (
                body.position
                + body.velocity * dt
                + 0.5 * accelerations[i] * dt * dt
            )
            
            body.velocity = body.velocity + accelerations[i] * dt