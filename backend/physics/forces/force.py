from abc import ABC, abstractmethod
from ..body import Body


class Force(ABC):

    @abstractmethod
    def acceleration(self, body: Body, bodies: list[Body]):
        pass