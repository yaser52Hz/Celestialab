# tests/integration/test_custom_scenarios.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation
from src.physics.forces.custom import AnyForce
from src.physics.forces.composite import CompositeForce

class TestCustomScenarios:
    """Test custom simulation scenarios"""
    
    def test_figure_eight_orbit(self, three_body_system):
        """Test the famous figure-8 three-body orbit"""
        sim = three_body_system
        
        # This is a known periodic orbit
        # Run for one period (approximately)
        sim.run(10000)
        
        # Check that bodies are still in the system
        positions = [np.linalg.norm(body.position) for body in sim.bodies]
        assert all(p < 2.0 for p in positions)  # Should stay bounded
    
    def test_chaotic_three_body(self):
        """Test chaotic three-body system"""
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=True)
        
        # Three bodies with random initial conditions
        bodies = [
            CelestialBody("A", 1.0, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
            CelestialBody("B", 1.0, [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]),
            CelestialBody("C", 1.0, [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0])
        ]
        
        for body in bodies:
            sim.add_body(body)
        
        # Run simulation
        sim.run(10000)
        
        # System should still be in roughly the same region
        positions = [np.linalg.norm(body.position) for body in sim.bodies]
        assert max(positions) < 10.0
    
    def test_custom_potential_scenario(self):
        """Test scenario with custom potential"""
        def custom_potential(pos, a=1.0):
            """Double-well potential"""
            x, y, z = pos
            return (x**2 - a**2)**2 + y**2 + z**2
        
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=False)
        
        from src.physics.forces.potential import PotentialForce
        sim.add_force(PotentialForce(custom_potential, params={'a': 1.0}))
        
        # Body starting in one well
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.5, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        # Run simulation
        sim.run(10000)
        
        # Body should oscillate in the well
        assert abs(body.position[0]) < 2.0
    
    def test_multiple_forces_scenario(self):
        """Test scenario with multiple forces acting"""
        def drag_force(bodies, time, k=0.01):
            return [-k * body.velocity for body in bodies]
        
        def external_force(bodies, time, F=1.0):
            return [F * np.array([1.0, 0.0, 0.0]) for _ in bodies]
        
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=False)
        
        # Add multiple forces
        sim.add_force(AnyForce(drag_force, params={'k': 0.01}))
        sim.add_force(AnyForce(external_force, params={'F': 1.0}))
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        # Run simulation
        sim.run(1000)
        
        # With constant force + drag, should reach terminal velocity
        v = body.velocity[0]
        terminal_velocity = 1.0 / 0.01  # F / k
        assert abs(v - terminal_velocity) < 0.1 * terminal_velocity