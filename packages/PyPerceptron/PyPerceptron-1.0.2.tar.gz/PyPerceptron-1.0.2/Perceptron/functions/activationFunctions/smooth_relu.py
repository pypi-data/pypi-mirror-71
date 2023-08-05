from Perceptron.functions.function import Function
import numpy as np


class SmoothReLU(Function):
    """
    Class representing the smooth ReLU function
    """

    def __init__(self):
        """
        Construct of the smooth ReLU
        """
        super().__init__()
        self.is_diff = True

    def compute(self, a: float) -> float:
        """
        Compute the smooth ReLU function on the given value

        :return the computed value given of the constructor
        """
        return np.log(1 + np.exp(a))

    def compute_derivative(self, a: float) -> float:
        """
        Compute the derivative of the smooth ReLU function on the given value

        :return: the value calculated on the derivative of the sigmoid
        """
        return np.exp(a) / (1 + np.exp(a))
