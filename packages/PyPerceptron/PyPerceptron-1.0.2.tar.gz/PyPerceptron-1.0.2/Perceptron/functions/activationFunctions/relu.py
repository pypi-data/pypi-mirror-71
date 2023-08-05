from Perceptron.functions.function import Function


class ReLU(Function):
    """
    Class representing the ReLU function
    """

    def __init__(self):
        """Construct of the ReLU"""
        super().__init__()
        self.is_diff = True

    def compute(self, a):
        """
        Compute the ReLU function on the given value

        :return the computed value given of the constructor
        """
        return a if a > 0 else 0

    def compute_derivative(self, a):
        """
        Compute the derivative of the ReLU function on the given value

        :return: the value calculated on the derivative of the sigmoid
        """
        return 1 if a > 0 else 0
