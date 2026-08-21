# src/physics/simulation.py
import numpy as np
from typing import List, Dict, Any, Optional  # ✅ Added Optional
from ..core.body import CelestialBody
from ..core.constants import G
from .forces.base import Force
from .forces.gravity import GravityForce
from .forces.composite import CompositeForce
from .integrators.base import Integrator
from .integrators.verlet import VerletIntegrator
from .integrators.rk4 import RK4Integrator
from .integrators.euler import EulerIntegrator

class Simulation:
    """
    Main N-body simulation engine.
    Handles bodies, forces, and time evolution.
    """
    
    def __init__(
        self,
        dt: float = 3600.0,
        integrator: str = 'verlet',
        use_gravity: bool = True,
        G_constant: float = G,
        softening: float = 1e-6
    ):
        """
        Args:
            dt: Time step in seconds
            integrator: Integration method ('euler', 'verlet', 'rk4')
            use_gravity: Whether to include Newtonian gravity
            G_constant: Gravitational constant
            softening: Softening parameter to prevent singularities
        """
        self.dt = dt
        self.bodies: List[CelestialBody] = []
        self.forces: List[Force] = []
        self.time = 0.0
        self.step_count = 0
        
        # Initialize integrator
        self.integrator = self._create_integrator(integrator)
        
        # Add gravity by default
        if use_gravity:
            self.forces.append(GravityForce(G_constant, softening))
    
    def _create_integrator(self, method: str) -> Integrator:
        """Create integrator instance"""
        if method == 'verlet':
            return VerletIntegrator()
        elif method == 'rk4':
            return RK4Integrator()
        elif method == 'euler':
            return EulerIntegrator()
        else:
            raise ValueError(f"Unknown integrator: {method}")
    
    def add_body(self, body: CelestialBody) -> None:
        """Add a celestial body to the simulation"""
        self.bodies.append(body)
    
    def remove_body(self, body_id: str) -> bool:
        """Remove a body by ID"""
        for i, body in enumerate(self.bodies):
            if body.id == body_id:
                self.bodies.pop(i)
                return True
        return False
    
    def clear_bodies(self) -> None:
        """Remove all bodies"""
        self.bodies.clear()
    
    def add_force(self, force: Force) -> None:
        """Add a force to the simulation"""
        self.forces.append(force)
    
    def remove_force(self, force_name: str) -> bool:
        """Remove a force by name"""
        for i, force in enumerate(self.forces):
            if force.name == force_name:
                self.forces.pop(i)
                return True
        return False
    
    def clear_forces(self) -> None:
        """Remove all forces"""
        self.forces.clear()
    
    def compute_accelerations(self) -> List[np.ndarray]:
        """Compute total acceleration from all forces"""
        n = len(self.bodies)
        if n == 0:
            return []
        
        total_accs = [np.zeros(3, dtype=np.float64) for _ in range(n)]
        
        for force in self.forces:
            accs = force.compute(self.bodies, self.time)
            for i in range(n):
                total_accs[i] += accs[i]
        
        return total_accs
    
    def step(self) -> None:
        """Perform one simulation step"""
        if len(self.bodies) < 2:
            return
        
        # Compute accelerations
        accelerations = self.compute_accelerations()
        
        # Integrate
        self.integrator.step(self.bodies, accelerations, self.dt)
        
        # Update time and trails
        self.time += self.dt
        self.step_count += 1
        
        for body in self.bodies:
            body.update_trail()
    
    def run(self, steps: int) -> None:
        """Run multiple steps"""
        for _ in range(steps):
            self.step()
    
    def reset(self) -> None:
        """Reset the simulation"""
        self.time = 0.0
        self.step_count = 0
        for body in self.bodies:
            body.trail.clear()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current simulation state"""
        return {
            'time': self.time,
            'step_count': self.step_count,
            'bodies': [body.to_dict() for body in self.bodies],
            'total_energy': self.compute_total_energy(),
            'total_momentum': self.compute_total_momentum().tolist(),
            'center_of_mass': self.compute_center_of_mass().tolist()
        }
    
    def compute_total_energy(self) -> Dict[str, float]:
        """Compute total kinetic and potential energy"""
        kinetic = 0.0
        potential = 0.0
        
        # Kinetic energy
        for body in self.bodies:
            kinetic += 0.5 * body.mass * np.dot(body.velocity, body.velocity)
        
        # Potential energy (from gravity only)
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                diff = self.bodies[j].position - self.bodies[i].position
                dist = np.linalg.norm(diff)
                if dist > 1e-6:
                    # Find the gravity force
                    gravity = None
                    for force in self.forces:
                        if 'Gravity' in force.name:
                            gravity = force
                            break
                    
                    if gravity:
                        G_val = getattr(gravity, 'G', 6.67430e-11)
                        potential -= G_val * self.bodies[i].mass * self.bodies[j].mass / dist
        
        return {
            'kinetic': kinetic,
            'potential': potential,
            'total': kinetic + potential
        }
    
    def compute_total_momentum(self) -> np.ndarray:
        """Compute total linear momentum"""
        total = np.zeros(3)
        for body in self.bodies:
            total += body.mass * body.velocity
        return total
    
    def compute_center_of_mass(self) -> np.ndarray:
        """Compute center of mass"""
        total_mass = sum(body.mass for body in self.bodies)
        if total_mass == 0:
            return np.zeros(3)
        
        com = np.zeros(3)
        for body in self.bodies:
            com += body.mass * body.position
        return com / total_mass
    
    def get_body(self, body_id: str) -> Optional[CelestialBody]:
        """Get a body by ID"""
        for body in self.bodies:
            if body.id == body_id:
                return body
        return None
    
    def set_time_step(self, dt: float) -> None:
        """Change the time step"""
        self.dt = dt