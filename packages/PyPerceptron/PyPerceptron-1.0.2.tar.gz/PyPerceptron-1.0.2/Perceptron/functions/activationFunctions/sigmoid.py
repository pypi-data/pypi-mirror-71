import numpy as np
from Perceptron.functions.function import Function


class Sigmoid(Function):
    """Returns the sigmoid of x element-wise.
    """

    def __init__(self):
        """Construct of the sigmoid"""
        self.is_diff = True

    def compute(self, a):
        """
        Compute the sigmoid function on the given value

        :return the computed value given of the constructor
        """
        return 1 / (1 + np.exp(-a))

    def compute_derivative(self, a):
        """
        Compute the derivative of the sigmoid function on the given value

        :return: the value calculated on the derivative of the sigmoid
        """
        return self.compute(a) * (1 - self.compute(a))