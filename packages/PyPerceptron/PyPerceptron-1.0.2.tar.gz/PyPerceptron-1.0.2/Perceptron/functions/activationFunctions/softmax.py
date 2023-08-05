from Perceptron.functions.function import Function
import numpy as np


class SoftMax(Function):
    """
    Class representing the softmax function
    """

    def __init__(self):
        """Construct of the softmax"""
        super().__init__()
        self.is_diff = True

    def compute(self, a):
        """
        Compute the softmax function on the given value

        :return the computed value given of the constructor
        """
        a -= np.max(a)
        sm = (np.exp(a).T / np.sum(np.exp(a), axis=0)).T
        return sm

    def compute_derivative(self, a):
        """
        Compute the derivative of the softmax function on the given value

        :return: the value calculated on the derivative of the softmax
        """
        # Reshape the 1-d softmax to 2-d so that np.dot will do the matrix multiplication
        s = self.compute().reshape(-1, 1)
        return np.diagflat(s) - np.dot(s, s.T)
