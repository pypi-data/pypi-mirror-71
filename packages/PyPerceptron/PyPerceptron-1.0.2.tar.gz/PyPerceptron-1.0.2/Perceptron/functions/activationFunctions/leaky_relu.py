from Perceptron.functions.function import Function


class LeakyReLU(Function):
    """
    Class representing the leaky ReLU function
    """

    def __init__(self):
        """
        Construct of the leaky ReLU
        """
        super().__init__()
        self.is_diff = True

    def compute(self, a: float) -> float:
        """
        Compute the leaky ReLU function on the given value

        :return the computed value given of the constructor
        """
        return max(0.01 * a, a)

    def compute_derivative(self, a: float):
        """
        Compute the derivative of the leaky ReLU function on the given value

        :return: the value calculated on the derivative of the sigmoid
        """
        return 1 if a > 0 else 0.01
