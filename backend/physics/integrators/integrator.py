from abc import ABC, abstractmethod


class Integrator(ABC):

    @abstractmethod
    def step(self, simulation, dt: float):
        pass
