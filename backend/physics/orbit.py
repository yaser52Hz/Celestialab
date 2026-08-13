from dataclasses import dataclass

import numpy as np

from backend.physics.body import Body


G = 6.67430e-11


@dataclass
class Orbit:

    semi_major_axis: float
    eccentricity: float

    inclination: float
    longitude_of_ascending_node: float
    argument_of_periapsis: float
    true_anomaly: float

    period: float | None = None


def calculate_orbit(
    primary: Body,
    secondary: Body,
) -> Orbit:

    r_vector = (
        secondary.state.position
        - primary.state.position
    )

    v_vector = (
        secondary.state.velocity
        - primary.state.velocity
    )

    r = np.linalg.norm(r_vector)
    v = np.linalg.norm(v_vector)

    mu = G * (
        primary.mass
        + secondary.mass
    )

    specific_energy = (
        0.5 * v**2
        - mu / r
    )

    semi_major_axis = -mu / (
        2 * specific_energy
    )

    h_vector = np.cross(
        r_vector,
        v_vector,
    )


    node_vector = np.cross(
        np.array([0.0, 0.0, 1.0]),
        h_vector,
    )

    node_norm = np.linalg.norm(node_vector)

    if node_norm > 0:

        longitude_of_ascending_node = np.arctan2(
            node_vector[1],
            node_vector[0],
        )

        if longitude_of_ascending_node < 0:
            longitude_of_ascending_node += 2 * np.pi

    else:

        longitude_of_ascending_node = 0.0
    

    inclination = np.arccos(
        h_vector[2]
        / np.linalg.norm(h_vector)
    )

    eccentricity_vector = (
        np.cross(v_vector, h_vector) / mu
        - r_vector / r
    )

    eccentricity = np.linalg.norm(
        eccentricity_vector
    )


    if (
        node_norm > 0
        and eccentricity > 1e-12
    ):
        argument_of_periapsis = np.arctan2(
            np.dot(
                np.cross(
                    node_vector,
                    eccentricity_vector,
                ),
                h_vector,
            ),
            np.dot(
                node_vector,
                eccentricity_vector,
            )
            * np.linalg.norm(h_vector),
        )

        if argument_of_periapsis < 0:
            argument_of_periapsis += 2 * np.pi

    else:
        argument_of_periapsis = 0.0



    if eccentricity > 1e-12:

        true_anomaly = np.arctan2(
            np.dot(
                np.cross(
                    eccentricity_vector,
                    r_vector,
                ),
                h_vector,
            ),
            np.dot(
                eccentricity_vector,
                r_vector,
            )
            * np.linalg.norm(h_vector),
        )

        if true_anomaly < 0:
            true_anomaly += 2 * np.pi

    else:
        true_anomaly = 0.0




    return Orbit(
        semi_major_axis=semi_major_axis,
        eccentricity=eccentricity,
        inclination=inclination,
        longitude_of_ascending_node=longitude_of_ascending_node,
        argument_of_periapsis=argument_of_periapsis,
        true_anomaly=true_anomaly,
    )