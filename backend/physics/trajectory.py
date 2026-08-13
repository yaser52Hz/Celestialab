import numpy as np


class Trajectory:

    def __init__(self):
        self.time = []
        self.position = []
        self.velocity = []

    def record(
        self,
        time: float,
        position,
        velocity,
    ):
        self.time.append(time)

        self.position.append(
            np.asarray(position, dtype=float).copy()
        )

        self.velocity.append(
            np.asarray(velocity, dtype=float).copy()
        )