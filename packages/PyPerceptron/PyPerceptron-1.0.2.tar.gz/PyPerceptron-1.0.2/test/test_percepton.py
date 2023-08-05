import nose
from Perceptron.perceptron import Perceptron
from Perceptron.functions.activationFunctions.sgn import Sign
from Perceptron.functions.activationFunctions.heaviside import Heaviside
from Perceptron.functions.lossFunctions.quadratic_loss import QuadraticLoss
from Perceptron.functions.function import Function

def test_precepton_101():
    """Test percepton istantiation"""
    p = Perceptron(3, 0.1, Sign(), QuadraticLoss())
    nose.tools.assert_is_instance(p, Perceptron)
    nose.tools.assert_is_instance(p.lr, float)
    nose.tools.assert_is_instance(p.act_fn, Function)
    nose.tools.assert_is_instance(p.weights, list)
    nose.tools.assert_is_instance(p.bias, float)


def test_preceptron_102():
    """
    Test perceptron with a simple data set using Heaviside as a activation function
    """
    dataset = [[2.7810836, 2.550537003, 0],
               [1.465489372, 2.362125076, 0],
               [3.396561688, 4.400293529, 0],
               [1.38807019, 1.850220317, 0],
               [3.06407232, 3.005305973, 0],
               [7.627531214, 2.759262235, 1],
               [5.332441248, 2.088626775, 1],
               [6.922596716, 1.77106367, 1],
               [8.675418651, -0.242068655, 1],
               [7.673756466, 3.508563011, 1]]
    p = Perceptron(2, 0.1, Heaviside(), QuadraticLoss())
    p.train(dataset, 3, 30)

    for d in dataset:
        nose.tools.assert_equal(p.evaluate([d[0], d[1]]), d[2])

