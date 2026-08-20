# tests/integration/test_force_combinations.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation
from src.physics.forces.custom import AnyForce
from src.physics.forces.composite import CompositeForce
from src.physics.forces.gravity import GravityForce
from src.physics.forces.potential import PotentialForce

class TestForceCombinations:
    """Test combinations of different force types"""
    
    def test_gravity_plus_drag(self):
        """Test gravity with drag force"""
        sim = Simulation(dt=0.01, integrator='verlet')
        
        def drag_force(bodies, time, k=0.01):
            return [-k * body.velocity for body in bodies]
        
        sim.add_force(AnyForce(drag_force, params={'k': 0.01}))
        
        # Add two bodies
        body1 = CelestialBody(
            name="A",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        body2 = CelestialBody(
            name="B",
            mass=1.0,
            position=[1.0, 0.0, 0.0],
            velocity=[0.0, 1.0, 0.0]
        )
        
        sim.add_body(body1)
        sim.add_body(body2)
        
        # Run simulation
        initial_energy = sim.compute_total_energy()['total']
        sim.run(1000)
        final_energy = sim.compute_total_energy()['total']
        
        # Energy should decrease (drag dissipates energy)
        assert final_energy < initial_energy
    
    def test_gravity_plus_external_field(self):
        """Test gravity with external field"""
        sim = Simulation(dt=0.01, integrator='verlet')
        
        def external_field(bodies, time, F=1.0):
            return [F * np.array([1.0, 0.0, 0.0]) for _ in bodies]
        
        sim.add_force(AnyForce(external_field, params={'F': 1.0}))
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        # Run simulation
        sim.run(1000)
        
        # Should have moved in the direction of the field
        assert body.position[0] > 0
    
    def test_composite_force_combination(self):
        """Test composite force combining multiple forces"""
        def force_a(bodies, time):
            return [np.array([1.0, 0.0, 0.0]) for _ in bodies]
        
        def force_b(bodies, time):
            return [np.array([0.0, 1.0, 0.0]) for _ in bodies]
        
        f1 = AnyForce(force_a, name="A")
        f2 = AnyForce(force_b, name="B")
        
        composite = CompositeForce([f1, f2], name="Combined")
        
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=False)
        sim.add_force(composite)
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        # Run simulation
        sim.run(100)
        
        # Should move diagonally
        assert body.position[0] > 0
        assert body.position[1] > 0
    
    def test_potential_plus_gravity(self):
        """Test potential force with gravity"""
        def harmonic_potential(pos, k=1.0):
            return 0.5 * k * np.dot(pos, pos)
        
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=True)
        sim.add_force(PotentialForce(harmonic_potential, params={'k': 1.0}))
        
        body1 = CelestialBody(
            name="A",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        body2 = CelestialBody(
            name="B",
            mass=1.0,
            position=[1.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        sim.add_body(body1)
        sim.add_body(body2)
        
        # Run simulation
        sim.run(1000)
        
        # Bodies should still be in the system
        assert np.linalg.norm(body1.position) < 10.0
        assert np.linalg.norm(body2.position) < 10.0