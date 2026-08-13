class Experiment:

    def __init__(
        self,
        bodies,
        forces,
        integrator,
        duration,
        timestep,
    ):
        self.bodies = bodies
        self.forces = forces
        self.integrator = integrator
        self.duration = duration
        self.timestep = timestep