# src/physics/integrators/verlet.py
import numpy as np
from typing import List
from .base import Integrator
from ...core.body import CelestialBody

class VerletIntegrator(Integrator):
    """
    Velocity Verlet integrator.
    Symplectic and energy-conserving for Hamiltonian systems.
    Order: 2
    """
    
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
        """
        Perform one Velocity Verlet step.
        
        Algorithm:
        1. x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt²
        2. Compute a(t+dt) (outside this method)
        3. v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
        """
        # Store old accelerations for velocity update
        old_accs = [a.copy() for a in accelerations]
        
        # Update positions
        for i, body in enumerate(bodies):
            body.position = (
                body.position
                + body.velocity * dt
                + 0.5 * accelerations[i] * dt * dt
            )
        
        # Store current accelerations for each body
        # This is needed for the velocity update
        for i, body in enumerate(bodies):
            # The new accelerations will be computed outside
            # We store old ones for now
            pass