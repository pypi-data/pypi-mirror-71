from Perceptron.functions.function import Function


class Heaviside(Function):
    """
    Class representing the Heaviside function
    """

    def __init__(self):
        self.is_diff = False

    def compute(self, a):
        """
        Compute the Heaviside function on the given value

        :argument a: argument of the function
        """
        return 1 if a >= 0 else 0

    def compute_derivative(self):
        pass
