from Perceptron.functions.function import Function
import math
from typing import Tuple


class CrossEntropy(Function):
    """
    Class representing the cross entropy cost function
    """

    def __init__(self):
        """
        Constructor the the cross entropy function
        """
        super(CrossEntropy, self).__init__()
        self.is_diff = True

    def compute(self, y: Tuple[float, float]) -> float:
        """
        Compute the cross entropy loss function on the given tuple

        :param y: tuple of 2 float numbers, the first is the expected value while the second
                  is the predicted value
        """
        res = 0 - (y[0] * math.log1p(y[1]) + (1 - y[0]) * math.log1p(1 - y[1]))
        return res

    def compute_derivative(self, y: Tuple[float, float]) -> float:
        """
        Compute the cross entropy function on the given tuple

        :param y: tuple of 2 float numbers, the first is the expected value while the second
                  is the predicted value
        """
        return (y[1] - y[0]) / ((1 - y[1]) * y[1])
