# tests/integration/test_custom_scenarios.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
import numpy as np
from api.engine.core.body import CelestialBody
from api.engine.physics.simulation import Simulation
from api.engine.physics.forces.custom import AnyForce

@pytest.mark.skip(reason="Skipping - needs verification")
class TestCustomScenarios:
    
    def test_figure_eight_orbit(self, three_body_system):
        pass
    
    def test_chaotic_three_body(self):
        pass
    
    def test_multiple_forces_scenario(self):
        pass