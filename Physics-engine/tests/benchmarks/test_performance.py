# tests/benchmarks/test_performance.py
import pytest
import time
import numpy as np
from src.core.body import CelestialBody
from src.physics.simulation import Simulation

class TestPerformance:
    """Performance benchmarks"""
    
    def test_simulation_speed_10_bodies(self):
        """Test speed with 10 bodies"""
        sim = Simulation(dt=3600.0)
        
        # Create 10 random bodies
        for i in range(10):
            body = CelestialBody(
                name=f"Body_{i}",
                mass=np.random.uniform(1e10, 1e12),
                position=np.random.randn(3) * 1e9,
                velocity=np.random.randn(3) * 1e3,
                radius=1e6
            )
            sim.add_body(body)
        
        # Time 1000 steps
        start = time.perf_counter()
        sim.run(1000)
        elapsed = time.perf_counter() - start
        
        # Should complete in under 5 seconds
        assert elapsed < 5.0
        
    def test_simulation_speed_100_bodies(self):
        """Test speed with 100 bodies"""
        sim = Simulation(dt=3600.0)
        
        # Create 100 random bodies
        for i in range(100):
            body = CelestialBody(
                name=f"Body_{i}",
                mass=np.random.uniform(1e10, 1e12),
                position=np.random.randn(3) * 1e9,
                velocity=np.random.randn(3) * 1e3,
                radius=1e6
            )
            sim.add_body(body)
        
        # Time 100 steps
        start = time.perf_counter()
        sim.run(100)
        elapsed = time.perf_counter() - start
        
        # Should complete in under 10 seconds
        assert elapsed < 10.0
    
    @pytest.mark.slow
    def test_long_term_stability(self):
        """Test long-term stability of solar system"""
        # Create solar system directly here to avoid import issues
        from src.core.constants import G, SOLAR_MASS, AU
        
        sim = Simulation(dt=3600.0 * 6, integrator='verlet')
        
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
        
        # Earth (simplified)
        earth = CelestialBody(
            name="Earth",
            mass=5.972e24,
            position=[AU, 0.0, 0.0],
            velocity=[0.0, 2.978e4, 0.0],
            radius=6.37e6,
            color="#4B9CD3"
        )
        sim.add_body(earth)
        
        # Run for 100 years
        steps_per_year = 365 * 4  # 6-hour steps
        start = time.perf_counter()
        sim.run(steps_per_year * 100)
        elapsed = time.perf_counter() - start
        
        # System should still be stable
        energy = sim.compute_total_energy()
        assert energy['total'] < 0  # Bound system
        assert len(sim.bodies) == 2  # Both bodies still there
        
        print(f"100-year simulation completed in {elapsed:.2f} seconds")