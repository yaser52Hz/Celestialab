# tests/unit/test_constants.py
import pytest
from src.core.constants import (
    G, SOLAR_MASS, EARTH_MASS, AU, DAY, YEAR,
    MU_SUN, MU_EARTH, C
)

class TestConstants:
    """Test physical constants"""
    
    def test_gravitational_constant(self):
        """Test gravitational constant value"""
        assert G == 6.67430e-11
        assert isinstance(G, float)
    
    def test_solar_mass(self):
        """Test solar mass value"""
        assert SOLAR_MASS == 1.98847e30
        assert SOLAR_MASS > 0
    
    def test_earth_mass(self):
        """Test Earth mass value"""
        assert EARTH_MASS == 5.9722e24
        assert EARTH_MASS > 0
    
    def test_astronomical_unit(self):
        """Test AU value"""
        assert AU == 1.495978707e11
        assert AU > 0
    
    def test_day_and_year(self):
        """Test time constants"""
        assert DAY == 86400.0
        assert YEAR == 365.25 * DAY
        assert YEAR > DAY
    
    def test_mu_values(self):
        """Test gravitational parameters"""
        assert MU_SUN == G * SOLAR_MASS
        assert MU_EARTH == G * EARTH_MASS
        assert MU_SUN > MU_EARTH
    
    def test_speed_of_light(self):
        """Test speed of light"""
        assert C == 299792458.0
        assert C > 0