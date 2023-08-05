__version__ = "1.0.0"
__name__ = "Perceptron"
from .perceptron import Perceptron
# Importing all the activation functions
from . import functions
from .functions.activationFunctions import *
from .functions.lossFunctions import *