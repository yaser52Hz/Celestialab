# src/core/types.py
"""
Type aliases for better code readability
"""
from typing import Tuple, List, Union, Callable, Optional, Dict, Any
import numpy as np

# 3D vector
Vector3 = np.ndarray  # shape (3,)

# 3x3 matrix
Matrix3x3 = np.ndarray  # shape (3, 3)

# Position or velocity
StateVector = Vector3

# Force function type
ForceFunction = Callable[..., List[Vector3]]

# Body list type
BodyList = List['CelestialBody']  # Forward reference

# Energy dictionary
EnergyDict = Dict[str, float]

# Simulation state
SimulationState = Dict[str, Any]