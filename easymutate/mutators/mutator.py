from abc import ABC, abstractmethod


class Mutator(ABC):
    @classmethod
    @abstractmethod
    def generate(cls):
        pass
