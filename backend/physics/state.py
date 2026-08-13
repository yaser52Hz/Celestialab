import numpy as np


class State:

    def __init__(
        self,
        position,
        velocity,
        acceleration=None,
    ):
        self.position = np.asarray(
            position,
            dtype=float,
        )

        self.velocity = np.asarray(
            velocity,
            dtype=float,
        )

        if acceleration is None:
            acceleration = np.zeros(3)

        self.acceleration = np.asarray(
            acceleration,
            dtype=float,
        )