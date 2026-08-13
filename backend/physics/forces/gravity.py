import numpy as np

from .force import Force
from ..body import Body


G = 6.67430e-11


class NewtonianGravity(Force):

    def acceleration(
        self,
        body: Body,
        bodies: list[Body]
    ) -> np.ndarray:
        
        acceleration = np.zeros(3)

        for other in bodies:

            if other is body:
                continue

            r = other.state.position - body.state.position
            distance = np.linalg.norm(r)

            acceleration += (
                G * other.mass * r / distance**3
            )
        
        return acceleration
    
    