import numpy as np

from backend.physics.body import Body
from backend.physics.forces.force import Force
from backend.physics.integrators.integrator import Integrator
from backend.physics.trajectory import Trajectory

from backend.analysis.system import (
    total_energy,
    total_momentum,
    total_angular_momentum,
)


class Simulation:

    def __init__(
        self,
        bodies: list[Body],
        forces: list[Force],
        integrator: Integrator,
    ):
        self.bodies = bodies
        self.forces = forces
        self.integrator = integrator

        self.time = 0.0

        # -------------------------
        # Trajectories
        # -------------------------

        self.trajectory = {
            body.name: Trajectory()
            for body in self.bodies
        }

        # -------------------------
        # Conservation histories
        # -------------------------

        self.energy_history = []
        self.momentum_history = []
        self.angular_momentum_history = []

        # -------------------------
        # Initial accelerations
        # -------------------------

        accelerations = self.calculate_accelerations()

        for body, acceleration in zip(
            self.bodies,
            accelerations,
        ):
            body.state.acceleration = acceleration

        # -------------------------
        # Record initial state
        # -------------------------

        self.record_state()
        self.record_conservation_quantities()

    # ==================================================
    # Forces
    # ==================================================

    def calculate_accelerations(self):

        accelerations = [
            np.zeros(3, dtype=float)
            for _ in self.bodies
        ]

        for force in self.forces:

            for i, body in enumerate(self.bodies):

                accelerations[i] += force.acceleration(
                    body,
                    self.bodies,
                )

        return accelerations

    # ==================================================
    # Recording
    # ==================================================

    def record_state(self):

        for body in self.bodies:

            self.trajectory[body.name].record(
                time=self.time,
                position=body.state.position,
                velocity=body.state.velocity,
            )

    def record_conservation_quantities(self):

        self.energy_history.append(
            total_energy(self.bodies)
        )

        self.momentum_history.append(
            total_momentum(self.bodies)
        )

        self.angular_momentum_history.append(
            total_angular_momentum(self.bodies)
        )

    # ==================================================
    # Time integration
    # ==================================================

    def step(self, dt: float):

        self.integrator.step(
            self,
            dt,
        )

        self.time += dt

        self.record_state()
        self.record_conservation_quantities()