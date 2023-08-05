__name__ = "activationFunction"

from .function import Function
# loss functions
from .lossFunctions.mean_abs_error import MeanAbsErr
from .lossFunctions.quadratic_loss import QuadraticLoss
from .lossFunctions.cross_entropy import CrossEntropy

