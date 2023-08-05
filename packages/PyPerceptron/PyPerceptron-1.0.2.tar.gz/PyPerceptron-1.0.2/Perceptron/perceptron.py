import random
from Perceptron.functions.function import Function
import numpy as np


class Perceptron(object):
    """
    Class representing the Percepton
    """

    def __init__(self, no_input: int, lr: float, act_fn: Function, loss_fn: Function):
        """
        Perceptron constructor

        :param no_input the number of the input of the percepton
        :param act_fn the activation function of the percepton
        :param lr: the learning rate of the perceptron
        """
        self.no_input = no_input
        self.bias = random.random()
        np.random.random_sample(10)
        self.weights = [random.random() for _ in range(no_input)]
        self.act_fn = act_fn  # the activation function
        self.loss_fn = loss_fn
        self.lr = lr  # the learning rate

    def evaluate(self, inputs):
        """
        Return the prediction of the perceptron

        :param inputs: the inputs feature
        :return: the evaluation made by the percepton
        """
        weighted_sum = np.dot(self.weights, inputs)

        weighted_sum += self.bias

        return self.act_fn.compute(weighted_sum)

    def update_weights(self, x, error, n):
        """
        Update the perceptron weight based on the inputs and the error

        :param x: The inputs
        :param error: the estimated error
        :param n: the batch size
        """
        # Check if the activation function is differentiable
        if self.act_fn.is_diff:
            x1 = x[0:self.no_input]
            self.weights = [
                i + ((self.lr / n) * error * self.act_fn.compute_derivative(np.dot(self.weights, x[0:self.no_input])) * j)
                for i, j in zip(self.weights, x[0:self.no_input+1])]
        else:
            self.weights = [i + (self.lr / n) * error * j for i, j in zip(self.weights, x[0:self.no_input])]

    def update_mini_batch(self, mini_batch):
        """
        Update the perceptron's weights and bias by applying gradient descent
        using the delta rule to a single mini batch

        :param mini_batch the mini batch
        """
        for x in mini_batch:
            prediction = self.evaluate(x[0: len(self.weights)])
            error = self.loss_fn.compute_derivative((x[-1], prediction))
            self.bias = self.bias + self.lr / len(mini_batch) * error  # update the bias
            self.update_weights(x, error, len(mini_batch))  # update the weights

    def train(self, training_data, mini_batches_size, n_epoch=30):
        """
        Train the perceptron using mini batch stocastic gradient descend

        :param training_data the data used to train the preceptron that will be divide in mini batches
        :param mini_batches_size the size of the mini batch
        :param n_epoch: number of iteration
        """

        n = len(training_data)
        for epoch in range(n_epoch):

            # randomize the training data and create mini_batches
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k + mini_batches_size]
                for k in range(0, n, mini_batches_size)
            ]

            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch)
