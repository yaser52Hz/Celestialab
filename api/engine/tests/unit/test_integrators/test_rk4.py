# tests/unit/test_integrators/test_rk4.py
import pytest
import numpy as np
from api.engine.core.body import CelestialBody
from api.engine.physics.integrators.rk4 import RK4Integrator

class TestRK4Integrator:
    """Test RK4 integrator"""
    
    def test_constant_acceleration(self):
        """Test constant acceleration: x = 0.5 * a * t²"""
        integrator = RK4Integrator()
        
        body = CelestialBody(
            name="Test",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        dt = 0.1
        a = np.array([1.0, 0.0, 0.0])
        accelerations = [a]
        
        # Run 10 steps
        for _ in range(10):
            integrator.step([body], accelerations, dt)
        
        # x = 0.5 * a * t² = 0.5 * 1.0 * 1.0 = 0.5
        assert np.allclose(body.position[0], 0.5, atol=0.01)
        assert np.allclose(body.velocity[0], 1.0, atol=0.01)
    
    def test_higher_accuracy(self):
        """Test RK4 has higher accuracy than Euler"""
        integrator_rk4 = RK4Integrator()
        from api.engine.physics.integrators.euler import EulerIntegrator
        integrator_euler = EulerIntegrator()
        
        def acceleration(pos, a=1.0):
            return a * np.array([1.0, 0.0, 0.0])
        
        dt = 0.1
        steps = 100
        t_final = steps * dt
        
        # RK4
        body_rk4 = CelestialBody(
            name="RK4",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        # Euler
        body_euler = CelestialBody(
            name="Euler",
            mass=1.0,
            position=[0.0, 0.0, 0.0],
            velocity=[0.0, 0.0, 0.0]
        )
        
        for _ in range(steps):
            a_rk4 = acceleration(body_rk4.position)
            a_euler = acceleration(body_euler.position)
            integrator_rk4.step([body_rk4], [a_rk4], dt)
            integrator_euler.step([body_euler], [a_euler], dt)
        
        # Exact solution: x = 0.5 * a * t²
        exact_pos = 0.5 * 1.0 * t_final**2
        
        # RK4 should be more accurate than Euler
        error_rk4 = abs(body_rk4.position[0] - exact_pos)
        error_euler = abs(body_euler.position[0] - exact_pos)
        
        assert error_rk4 < error_euler
    
    def test_properties(self):
        """Test integrator properties"""
        integrator = RK4Integrator()
        assert integrator.name == "Runge-Kutta 4th Order"
        assert integrator.order == 4