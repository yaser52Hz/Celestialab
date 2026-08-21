# tests/integration/test_energy_conservation.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
import numpy as np
from api.engine.core.body import CelestialBody
from api.engine.physics.simulation import Simulation
from api.engine.physics.forces.custom import AnyForce
from api.engine.physics.forces.potential import PotentialForce

class TestEnergyConservation:
    
    def test_two_body_energy_conservation(self, two_body_system):
        sim = two_body_system
        initial_energy = sim.compute_total_energy()['total']
        energies = [initial_energy]
        
        steps = int(365.25 * 24 * 3600 / sim.dt)
        
        for i in range(steps):
            sim.step()
            if i % 100 == 0:
                energies.append(sim.compute_total_energy()['total'])
        
        energy_std = np.std(energies)
        assert energy_std / abs(initial_energy) < 0.02
    
    def test_three_body_energy_conservation(self, three_body_system):
        sim = three_body_system
        initial_energy = sim.compute_total_energy()['total']
        energies = [initial_energy]
        
        for i in range(1000):
            sim.step()
            if i % 100 == 0:
                energies.append(sim.compute_total_energy()['total'])
        
        energy_std = np.std(energies)
        assert energy_std / abs(initial_energy) < 0.05
    
    @pytest.mark.skip(reason="Skipping - needs investigation")
    def test_energy_conservation_with_custom_force(self):
        pass
    
    @pytest.mark.skip(reason="Skipping - needs investigation")
    def test_energy_dissipation_with_drag(self):
        pass
    
    @pytest.mark.skip(reason="Skipping - needs investigation")
    def test_potential_energy_conservation(self):
        pass