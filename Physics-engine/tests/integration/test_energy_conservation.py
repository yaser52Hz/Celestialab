# tests/integration/test_energy_conservation.py
import pytest
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation
from src.physics.forces.custom import AnyForce
from src.physics.forces.potential import PotentialForce

class TestEnergyConservation:
    """Test energy conservation in various scenarios"""
    
    def test_two_body_energy_conservation(self, two_body_system):
        """Test energy conservation in two-body system"""
        sim = two_body_system
        
        initial_energy = sim.compute_total_energy()['total']
        energies = [initial_energy]
        
        # Run for one orbit
        steps = int(365.25 * 24 * 3600 / sim.dt)
        
        for i in range(steps):
            sim.step()
            if i % 100 == 0:  # Sample every 100 steps
                energies.append(sim.compute_total_energy()['total'])
        
        # Energy should be conserved within 2%
        energy_std = np.std(energies)
        assert energy_std / abs(initial_energy) < 0.02
    
    def test_three_body_energy_conservation(self, three_body_system):
        """Test energy conservation in three-body system"""
        sim = three_body_system
        
        initial_energy = sim.compute_total_energy()['total']
        energies = [initial_energy]
        
        # Run for 1000 steps
        for i in range(1000):
            sim.step()
            if i % 100 == 0:
                energies.append(sim.compute_total_energy()['total'])
        
        # Energy should be conserved within 5%
        energy_std = np.std(energies)
        assert energy_std / abs(initial_energy) < 0.05
    
    def test_energy_conservation_with_custom_force(self):
        """Test energy with custom conservative force"""
        def conservative_force(bodies, time, k=1.0):
            """F = -k * x (harmonic oscillator)"""
            return [-k * body.position for body in bodies]
        
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=False)
        sim.add_force(AnyForce(conservative_force, name="Harmonic", params={'k': 1.0}))
        
        body = CelestialBody(
            name="Oscillator",
            mass=1.0,
            position=[1.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        initial_energy = sim.compute_total_energy()['total']
        
        # Run many steps
        for _ in range(10000):
            sim.step()
        
        final_energy = sim.compute_total_energy()['total']
        
        # Should be conserved within 1%
        relative_change = abs((final_energy - initial_energy) / initial_energy)
        assert relative_change < 0.01
    
    def test_energy_dissipation_with_drag(self):
        """Test energy decreases with drag force"""
        def drag_force(bodies, time, k=0.01):
            return [-k * body.velocity for body in bodies]
        
        sim = Simulation(dt=0.01, integrator='euler', use_gravity=False)
        sim.add_force(AnyForce(drag_force, name="Drag", params={'k': 0.01}))
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[1.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        initial_energy = sim.compute_total_energy()['total']
        
        # Run steps
        for _ in range(100):
            sim.step()
        
        final_energy = sim.compute_total_energy()['total']
        
        # Energy should decrease (dissipation)
        assert final_energy < initial_energy
    
    def test_potential_energy_conservation(self):
        """Test energy conservation with potential-derived force"""
        def harmonic_potential(pos, k=1.0):
            return 0.5 * k * np.dot(pos, pos)
        
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=False)
        sim.add_force(PotentialForce(harmonic_potential, name="Harmonic", params={'k': 1.0}))
        
        body = CelestialBody(
            name="Oscillator",
            mass=1.0,
            position=[1.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        initial_energy = sim.compute_total_energy()['total']
        energies = []
        
        # Run many steps
        for i in range(10000):
            sim.step()
            if i % 100 == 0:
                energies.append(sim.compute_total_energy()['total'])
        
        # Energy should be conserved within 1%
        energy_std = np.std(energies)
        assert energy_std / abs(initial_energy) < 0.01