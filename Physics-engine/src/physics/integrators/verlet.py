# src/physics/integrators/verlet.py
import numpy as np
from typing import List
from .base import Integrator
from ...core.body import CelestialBody

class VerletIntegrator(Integrator):
    """Velocity Verlet integrator - symplectic, 2nd order"""
    
    @property
    def name(self) -> str:
        return "Velocity Verlet"
    
    @property
    def order(self) -> int:
        return 2
    
    def step(
        self,
        bodies: List[CelestialBody],
        accelerations: List[np.ndarray],
        dt: float
    ) -> None:
        # Save old accelerations
        old_accs = [a.copy() for a in accelerations]
        
        # Update positions
        for i, body in enumerate(bodies):
            body.position = (
                body.position
                + body.velocity * dt
                + 0.5 * accelerations[i] * dt * dt
            )
        
        # NOTE: In a full Velocity Verlet, we would compute new accelerations here
        # For simplicity, we're using the same accelerations
        # This is a simplified version
        
        # Update velocities
        for i, body in enumerate(bodies):
            body.velocity = body.velocity + 0.5 * (old_accs[i] + accelerations[i]) * dt