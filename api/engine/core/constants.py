# src/core/constants.py
"""
Physical constants used in celestial mechanics
"""

# Gravitational constant (m³ kg⁻¹ s⁻²)
G = 6.67430e-11

# Solar mass (kg)
SOLAR_MASS = 1.98847e30

# Earth mass (kg)
EARTH_MASS = 5.9722e24

# Jupiter mass (kg)
JUPITER_MASS = 1.8986e27

# Astronomical Unit (m)
AU = 1.495978707e11

# Light year (m)
LY = 9.4607304725808e15

# Parsec (m)
PC = 3.085677581491367e16

# Solar radius (m)
SOLAR_RADIUS = 6.957e8

# Earth radius (m)
EARTH_RADIUS = 6.371e6

# Day in seconds
DAY = 86400.0

# Year in seconds (365.25 days)
YEAR = 365.25 * DAY

# Speed of light (m/s)
C = 299792458.0

# Gravitational parameter of Sun (m³/s²)
MU_SUN = G * SOLAR_MASS

# Gravitational parameter of Earth (m³/s²)
MU_EARTH = G * EARTH_MASS