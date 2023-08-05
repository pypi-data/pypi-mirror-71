from Perceptron.functions.function import Function
from typing import Tuple


class MeanAbsErr(Function):

    def __init__(self):
        super(MeanAbsErr, self).__init__()
        self.is_diff = True

    def compute(self, y: Tuple[float, float]):
        return abs(y[0] - y[1])

    def compute_derivative(self, a) -> int:
        return -1
