from Perceptron.functions.function import Function
import numpy as np


class Tanh(Function):
    """
    Class representing the Hyperbolic tangent function
    """

    def __init__(self):
        """
        Construct of the Hyperbolic tangent
        """
        super().__init__()
        self.is_diff = True

    def compute(self, a):
        """
        Compute the Hyperbolic tangent function on the given value

        :param a the input of function
        :return the computed value given of the constructor
        """
        return (2 / (1 + np.exp(-2 * a))) - 1

    def compute_derivative(self, a):
        """
        Compute the derivative of the Hyperbolic tangent function on the given value

        :param a the input of function
        :return: the value calculated on the derivative of the sigmoid
        """
        return 1 - self.compute(a) ** 2
