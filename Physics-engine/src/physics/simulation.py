# src/physics/simulation.py
import numpy as np
from typing import List, Dict, Any
from ..core.body import CelestialBody
from .forces.base import Force
from .integrators.verlet import VerletIntegrator

class Simulation:
    """Main N-body simulation engine"""
    
    def __init__(self, dt: float = 3600.0, integrator: str = 'verlet'):
        self.dt = dt
        self.bodies: List[CelestialBody] = []
        self.forces: List[Force] = []
        self.time: float = 0.0
        self.integrator = VerletIntegrator()
    
    def add_body(self, body: CelestialBody) -> None:
        """Add a celestial body"""
        self.bodies.append(body)
    
    def add_force(self, force: Force) -> None:
        """Add ANY force to the simulation"""
        self.forces.append(force)
    
    def compute_accelerations(self) -> List[np.ndarray]:
        """Compute total acceleration from all forces"""
        n = len(self.bodies)
        total_accs = [np.zeros(3) for _ in range(n)]
        
        for force in self.forces:
            accs = force.compute(self.bodies, self.time)
            for i in range(n):
                total_accs[i] += accs[i]
        
        return total_accs
    
    def step(self) -> None:
        """Perform one simulation step"""
        if len(self.bodies) < 2:
            return
            
        accs = self.compute_accelerations()
        self.integrator.step(self.bodies, accs, self.dt)
        self.time += self.dt
        
        # Update trails
        for body in self.bodies:
            body.update_trail()
    
    def run(self, steps: int) -> None:
        """Run multiple steps"""
        for _ in range(steps):
            self.step()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current simulation state"""
        return {
            'time': self.time,
            'bodies': [body.to_dict() for body in self.bodies]
        }