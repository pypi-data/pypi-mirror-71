from Perceptron.functions.function import Function
from typing import Tuple


class QuadraticLoss(Function):
    """
    Class representing the Quadrtic loss function
    """

    def __init__(self):
        """
        The constructor of the Quadratic loss function
        """
        super(QuadraticLoss, self).__init__()
        self.is_diff = True

    def compute(self, y: Tuple[float, float]) -> float:
        """
        Compute the quadratic loss function on the given tuple

        :param y: tuple of 2 float numbers, the first is the expected value while the second
                  is the predicted value
        """
        return ((y[0] - y[1]) ** 2) / 2

    def compute_derivative(self, y: Tuple[float, float]):
        """
        Compute the derivative quadratic loss function on the given tuple

        :param y: tuple of 2 float numbers, the first is the expected value while the second
                  is the predicted value
        """
        return y[0] - y[1]
