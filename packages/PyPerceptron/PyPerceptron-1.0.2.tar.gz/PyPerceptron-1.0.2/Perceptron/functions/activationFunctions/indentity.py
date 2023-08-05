from Perceptron.functions.function import Function


class Identity(Function):
    """
        Class representing the Identity function
    """

    def __init__(self):
        self.is_diff = True

    def compute(self, a):
        """
        Compute the identity function on the given value

        :argument a: argument of the function
        """
        return a

    def compute_derivative(self):
        return 1
