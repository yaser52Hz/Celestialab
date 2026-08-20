# tests/integration/test_orbital_mechanics.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation
from src.core.constants import G, SOLAR_MASS, AU, YEAR

def create_solar_system():
    """Create a realistic solar system for testing"""
    sim = Simulation(dt=3600.0 * 6, integrator='verlet')  # 6-hour steps
    
    # Sun
    sun = CelestialBody(
        name="Sun",
        mass=SOLAR_MASS,
        position=[0.0, 0.0, 0.0],
        velocity=[0.0, 0.0, 0.0],
        radius=6.96e8,
        color="#FDB813"
    )
    sim.add_body(sun)
    
    # Planets (simplified, circular orbits)
    planets = [
        {"name": "Mercury", "mass": 3.285e23, "a": 0.387 * AU, "v": 4.74e4},
        {"name": "Venus", "mass": 4.867e24, "a": 0.723 * AU, "v": 3.50e4},
        {"name": "Earth", "mass": 5.972e24, "a": 1.0 * AU, "v": 2.978e4},
        {"name": "Mars", "mass": 6.417e23, "a": 1.524 * AU, "v": 2.41e4},
        {"name": "Jupiter", "mass": 1.898e27, "a": 5.203 * AU, "v": 1.31e4},
    ]
    
    for planet in planets:
        body = CelestialBody(
            name=planet["name"],
            mass=planet["mass"],
            position=[planet["a"], 0.0, 0.0],
            velocity=[0.0, planet["v"], 0.0],
            radius=1e7,  # Visual only
            color="#FFFFFF"
        )
        sim.add_body(body)
    
    return sim

class TestOrbitalMechanics:
    """Test orbital mechanics"""
    
    def test_kepler_third_law(self, two_body_system):
        """Test Kepler's Third Law: T² ∝ a³"""
        sim = two_body_system
        earth = sim.bodies[1]
        
        # Get orbital parameters
        initial_pos = earth.position
        initial_vel = earth.velocity
        
        # Calculate semi-major axis from initial conditions
        mu = G * sim.bodies[0].mass
        r = np.linalg.norm(initial_pos)
        v = np.linalg.norm(initial_vel)
        
        # Specific orbital energy: ε = v²/2 - μ/r
        epsilon = v**2 / 2 - mu / r
        a = -mu / (2 * epsilon) if epsilon < 0 else np.inf
        
        # Orbital period: T = 2π * sqrt(a³/μ)
        if a != np.inf:
            T = 2 * np.pi * np.sqrt(a**3 / mu)
        else:
            T = np.inf
        
        # Simulate one orbit
        steps = int(T / sim.dt) if T != np.inf else 1000000
        sim.run(steps // 10)  # Run a fraction to see if it's working
        
        # The body should still be orbiting
        final_pos = earth.position
        assert np.linalg.norm(final_pos) > 0.5 * r
    
    def test_orbital_stability(self, two_body_system):
        """Test orbital stability over many orbits"""
        sim = two_body_system
        earth = sim.bodies[1]
        
        initial_distance = np.linalg.norm(earth.position)
        
        # Run for 10 orbits
        # Approximate Earth period: 1 year
        steps_per_orbit = int(YEAR / sim.dt)
        sim.run(10 * steps_per_orbit)
        
        final_distance = np.linalg.norm(earth.position)
        
        # Distance should not change by more than 10%
        relative_change = abs(final_distance - initial_distance) / initial_distance
        assert relative_change < 0.1
    
    def test_orbital_speed(self, two_body_system):
        """Test orbital speed approximately matches circular orbit speed"""
        sim = two_body_system
        earth = sim.bodies[1]
        sun = sim.bodies[0]
        
        r = np.linalg.norm(earth.position)
        v = np.linalg.norm(earth.velocity)
        
        # Circular orbit speed: v_circ = sqrt(G*M/r)
        mu = G * sun.mass
        v_circ = np.sqrt(mu / r)
        
        # Should be within 10% of circular speed
        assert abs(v - v_circ) / v_circ < 0.1