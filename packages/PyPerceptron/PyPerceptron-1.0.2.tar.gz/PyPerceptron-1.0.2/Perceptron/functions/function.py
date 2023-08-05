from abc import ABC, abstractmethod


class Function(ABC):

    def __init__(self):
        self.is_diff = None

    @abstractmethod
    def compute(self, a):
        pass

    @abstractmethod
    def compute_derivative(self, a):
        pass
