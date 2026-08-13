import numpy as np

from backend.physics.body import Body


G = 6.67430e-11


def total_kinetic_energy(
    bodies: list[Body],
) -> float:

    energy = 0.0

    for body in bodies:

        velocity = body.state.velocity

        energy += (
            0.5
            * body.mass
            * np.dot(velocity, velocity)
        )

    return energy


def total_potential_energy(
    bodies: list[Body],
) -> float:

    energy = 0.0

    for i, body_i in enumerate(bodies):

        for body_j in bodies[i + 1:]:

            displacement = (
                body_j.state.position
                - body_i.state.position
            )

            distance = np.linalg.norm(
                displacement
            )

            energy -= (
                G
                * body_i.mass
                * body_j.mass
                / distance
            )

    return energy


def total_energy(
    bodies: list[Body],
) -> float:

    kinetic = total_kinetic_energy(bodies)
    potential = total_potential_energy(bodies)

    return kinetic + potential


def total_momentum(bodies: list[Body]) -> np.ndarray:

    momentum = np.zeros(3)

    for body in bodies:
        momentum += body.mass * body.state.velocity

    return momentum


def total_angular_momentum(
    bodies: list[Body],
) -> np.ndarray:

    angular_momentum = np.zeros(3)

    for body in bodies:

        angular_momentum += np.cross(
            body.state.position,
            body.mass * body.state.velocity,
        )

    return angular_momentum
