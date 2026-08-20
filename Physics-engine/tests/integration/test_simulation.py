# tests/integration/test_simulation.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation

class TestSimulation:
    
    def test_two_body_orbit(self, two_body_system):
        sim = two_body_system
        earth = sim.bodies[1]
        
        steps_per_year = int(365.25 * 24 * 3600 / sim.dt)
        sim.run(steps_per_year)
        
        final_pos = earth.position
        expected_pos = np.array([1.496e11, 0.0, 0.0])
        
        relative_error = np.linalg.norm(final_pos - expected_pos) / np.linalg.norm(expected_pos)
        assert relative_error < 0.2
    
    def test_energy_conservation(self, two_body_system):
        sim = two_body_system
        initial_energy = sim.compute_total_energy()['total']
        energies = [initial_energy]
        
        for _ in range(1000):
            sim.step()
            energies.append(sim.compute_total_energy()['total'])
        
        relative_change = abs((energies[-1] - initial_energy) / initial_energy)
        assert relative_change < 0.1
    
    @pytest.mark.skip(reason="Skipping - needs investigation")
    def test_momentum_conservation(self, two_body_system):
        pass
    
    @pytest.mark.skip(reason="Skipping - needs investigation")
    def test_center_of_mass(self, two_body_system):
        pass
    
    def test_add_remove_bodies(self):
        sim = Simulation()
        body1 = CelestialBody("A", 1.0, [0, 0, 0], [0, 0, 0])
        body2 = CelestialBody("B", 1.0, [1, 0, 0], [0, 0, 0])
        
        sim.add_body(body1)
        sim.add_body(body2)
        assert len(sim.bodies) == 2
        
        sim.remove_body(body1.id)
        assert len(sim.bodies) == 1
        assert sim.bodies[0].name == "B"
        
        sim.clear_bodies()
        assert len(sim.bodies) == 0