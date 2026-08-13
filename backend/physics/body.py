from backend.physics.state import State


class Body:

    def __init__(
        self,
        name: str,
        mass: float,
        position,
        velocity,
    ):
        self.name = name
        self.mass = mass

        self.state = State(
            position=position,
            velocity=velocity,
        )