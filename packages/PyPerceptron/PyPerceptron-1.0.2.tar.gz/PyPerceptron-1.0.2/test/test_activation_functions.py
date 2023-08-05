import nose
from Perceptron.functions.activationFunctions.sgn import Sign
from Perceptron.functions.activationFunctions.heaviside import Heaviside
from Perceptron.functions.activationFunctions.indentity import Identity
from Perceptron.functions.activationFunctions.sigmoid import Sigmoid
from Perceptron.functions.activationFunctions.relu import ReLU
from Perceptron.functions.activationFunctions.softmax import SoftMax
from Perceptron.functions.function import Function
import numpy as np


def test_sing_fn():
    """Test sign function"""
    fn = Sign()
    nose.tools.assert_is_instance(fn, Function)
    nose.tools.assert_is_instance(fn, Sign)
    nose.tools.assert_false(fn.is_diff)
    nose.tools.assert_equal(fn.compute(10), 1)
    nose.tools.assert_equal(fn.compute(0), 0)
    nose.tools.assert_equal(fn.compute(-10), -1)


def test_heavside_fn():
    """Test Heaviside function"""
    fn = Heaviside()
    nose.tools.assert_is_instance(fn, Function)
    nose.tools.assert_is_instance(fn, Heaviside)
    nose.tools.assert_false(fn.is_diff)
    nose.tools.assert_equal(fn.compute(10), 1)
    nose.tools.assert_equal(fn.compute(0), 1)
    nose.tools.assert_equal(fn.compute(-10), 0)


def test_identity_fn():
    """Test Identity function"""
    fn = Identity()
    nose.tools.assert_is_instance(fn, Function)
    nose.tools.assert_is_instance(fn, Identity)
    nose.tools.assert_true(fn.is_diff)
    nose.tools.assert_equal(fn.compute(10), 10)
    nose.tools.assert_equal(fn.compute(0), 0)
    nose.tools.assert_equal(fn.compute(-10), -10)
    nose.tools.assert_equal(fn.compute_derivative(), 1)


def test_sigmoid_fn():
    """Test the sigmoid function"""
    fn = Sigmoid()
    nose.tools.assert_is_instance(fn, Function)
    nose.tools.assert_is_instance(fn, Sigmoid)
    nose.tools.assert_equal(fn.compute(0), 0.5)
    nose.tools.assert_equal(fn.compute_derivative(0), 0.25)


def test_relu():
    """Test ReLU function"""
    fn = ReLU()
    nose.tools.assert_is_instance(fn, Function)
    nose.tools.assert_is_instance(fn, ReLU)
    nose.tools.assert_equal(fn.compute(sum([1, 2, 3, 4, 5])), 15)
    nose.tools.assert_equal(fn.compute(-1), 0)
    nose.tools.assert_equal(fn.compute_derivative(sum([1, 2, 3, 4, 5])), 1)
    nose.tools.assert_equal(fn.compute_derivative(-1), 0)


def test_softmax():
    fn = SoftMax()
    nose.tools.assert_is_instance(fn, Function)
    nose.tools.assert_is_instance(fn, SoftMax)
    np.allclose(fn.compute(np.array([1, 2, 3, 4, 1, 2, 3])),
                np.array([0.024, 0.064, 0.175, 0.475, 0.024, 0.064, 0.175]))
