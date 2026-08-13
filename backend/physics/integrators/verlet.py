from .integrator import Integrator


class VelocityVerlet(Integrator):

    def step(self, simulation, dt: float):

        bodies = simulation.bodies

        # 1. Update all positions
        for body in bodies:

            body.state.position += (
                body.state.velocity * dt
                + 0.5
                * body.state.acceleration
                * dt**2
            )

        # 2. Calculate accelerations at the new positions
        new_accelerations = (
            simulation.calculate_accelerations()
        )

        # 3. Update all velocities
        for body, new_acceleration in zip(
            bodies,
            new_accelerations,
        ):

            body.state.velocity += (
                0.5
                * (
                    body.state.acceleration
                    + new_acceleration
                )
                * dt
            )

            body.state.acceleration = new_acceleration