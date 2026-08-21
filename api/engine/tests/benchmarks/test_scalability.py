# tests/benchmarks/test_scalability.py
import pytest
import time
import numpy as np
from api.engine.core.body import CelestialBody
from api.engine.physics.simulation import Simulation

class TestScalability:
    """Test scalability of the simulation"""
    
    def test_scaling_with_body_count(self):
        """Test how runtime scales with number of bodies"""
        body_counts = [10, 20, 50, 100]
        times = []
        
        for n in body_counts:
            sim = Simulation(dt=3600.0, integrator='verlet')
            
            # Create n random bodies
            for i in range(n):
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
            times.append(elapsed)
        
        # O(N²) scaling should hold approximately
        # Time for N bodies should be roughly (N/10)² * time_10
        for i in range(1, len(body_counts)):
            ratio = times[i] / times[0]
            expected_ratio = (body_counts[i] / body_counts[0])**2
            # Allow 50% deviation due to overhead
            assert ratio < 2.0 * expected_ratio
    
    def test_memory_usage(self):
        """Test memory usage with trails"""
        sim = Simulation(dt=3600.0)
        
        # Add 100 bodies with trails
        for i in range(100):
            body = CelestialBody(
                name=f"Body_{i}",
                mass=1.0,
                position=np.random.randn(3) * 1e9,
                velocity=np.random.randn(3) * 1e3,
                radius=1e6,
                max_trail_length=1000
            )
            sim.add_body(body)
        
        # Run some steps to generate trails
        sim.run(100)
        
        # Check that trails are created
        for body in sim.bodies:
            assert len(body.trail) > 0
    
    def test_force_scaling(self):
        """Test performance with many forces"""
        sim = Simulation(dt=0.01, integrator='verlet', use_gravity=False)
        
        # Add many custom forces
        for i in range(10):
            def force_func(bodies, time, a=i):
                return [a * np.array([1.0, 0.0, 0.0]) for _ in bodies]
            
            from api.engine.physics.forces.custom import AnyForce
            sim.add_force(AnyForce(force_func, params={'a': i}))
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        sim.add_body(body)
        
        # Should still run quickly
        start = time.perf_counter()
        sim.run(1000)
        elapsed = time.perf_counter() - start
        
        assert elapsed < 2.0  # Should complete in under 2 seconds