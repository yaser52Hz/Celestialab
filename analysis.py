import numpy as np


def specific_energy(body, central_body):
    r = np.linalg.norm(
        body.state.position - central_body.state.position
    )

    v = np.linalg.norm(
        body.state.velocity - central_body.state.velocity
    )

    mu = 6.67430e-11 * central_body.mass

    return 0.5 * v**2 - mu / r