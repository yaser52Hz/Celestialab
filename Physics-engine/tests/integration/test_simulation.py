# tests/integration/test_simulation.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation

class TestSimulation:
    """Test simulation engine"""
    
    def test_two_body_orbit(self, two_body_system):
        """Test two-body orbital motion"""
        sim = two_body_system
        sun = sim.bodies[0]
        earth = sim.bodies[1]
        
        # Run for one year
        steps_per_year = int(365.25 * 24 * 3600 / sim.dt)
        sim.run(steps_per_year)
        
        # Earth should be back near starting position
        final_pos = earth.position
        expected_pos = np.array([1.496e11, 0.0, 0.0])
        
        # Allow 10% error
        relative_error = np.linalg.norm(final_pos - expected_pos) / np.linalg.norm(expected_pos)
        assert relative_error < 0.1
    
    def test_energy_conservation(self, two_body_system):
        """Test energy conservation in two-body system"""
        sim = two_body_system
        
        initial_energy = sim.compute_total_energy()['total']
        energies = [initial_energy]
        
        # Run 1000 steps
        for _ in range(1000):
            sim.step()
            energies.append(sim.compute_total_energy()['total'])
        
        # Energy should be conserved within 1%
        relative_change = abs((energies[-1] - initial_energy) / initial_energy)
        assert relative_change < 0.01
    
    def test_momentum_conservation(self, two_body_system):
        """Test momentum conservation"""
        sim = two_body_system
        
        initial_momentum = sim.compute_total_momentum()
        
        # Run 1000 steps
        for _ in range(1000):
            sim.step()
        
        final_momentum = sim.compute_total_momentum()
        
        # Momentum should be conserved
        assert np.allclose(initial_momentum, final_momentum, rtol=1e-6)
    
    def test_center_of_mass(self, two_body_system):
        """Test center of mass is conserved"""
        sim = two_body_system
        
        initial_com = sim.compute_center_of_mass()
        
        # Run 1000 steps
        for _ in range(1000):
            sim.step()
        
        final_com = sim.compute_center_of_mass()
        
        # Center of mass should be constant
        assert np.allclose(initial_com, final_com, rtol=1e-6)
    
    def test_add_remove_bodies(self):
        """Test adding and removing bodies"""
        sim = Simulation()
        
        body1 = CelestialBody(
            name="A",
            mass=1.0,
            position=[0, 0, 0],
            velocity=[0, 0, 0]
        )
        
        body2 = CelestialBody(
            name="B",
            mass=1.0,
            position=[1, 0, 0],
            velocity=[0, 0, 0]
        )
        
        sim.add_body(body1)
        sim.add_body(body2)
        assert len(sim.bodies) == 2
        
        sim.remove_body(body1.id)
        assert len(sim.bodies) == 1
        assert sim.bodies[0].name == "B"
        
        sim.clear_bodies()
        assert len(sim.bodies) == 0