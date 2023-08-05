from Perceptron.functions.function import Function


class Sign(Function):
    """
        Class representing the Sign function
    """

    def __init__(self):
        self.is_diff = False

    def compute(self, a):
        """
        Compute the sign function on the given value

        :argument a: argument of the function
        """
        if a < 0:
            return -1
        elif a == 0:
            return 0
        else:
            return 1

    def compute_derivative(self):
        pass
