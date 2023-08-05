# Python-Perceptron

![language](https://img.shields.io/badge/language-python-blue)
![license](https://img.shields.io/badge/license-MIT-orange)

An Basic implementation of the perceptron, the build block a neural net.

![perceptron](./assets/img/perceptron_350_328.png)

## Table of contents

- [Installation](#installation)
- [Example](#example)
- [Docs](#documentation)
- [Contributing](#contributing)

## Installation

    pip install PyPerceptron
    
    
## Example

Here's how to instanitate the Perceptron

```python
from Perceptron.perceptron import Perceptron

p = Perceptron(number_inputs, learning_rate, Activation_fn, Loss_fn)
```
    
```python
from Perceptron.perceptron import Perceptron
from Perceptron.functions.activationFunctions.heaviside import Heaviside
from Perceptron.functions.lossFunctions.quadratic_loss import QuadraticLoss

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


p = Perceptron(2, 0.1, Heaviside(), QuadraticLoss()) # number of inputs, learning rate, activation function, loss funciton
p.train(dataset, 3, 30)

for d in dataset:
    assert p.evaluate(d[0], d[1]) == d[2]

```

To find out more about the math behind the perceptron, check out the [notebook](./demo/What_is_a_perceptron.ipynb) with the fully explanation.

If you wanna see more about how to use the perceptron checkout the [demos](./demo).

## Documentation

- [Perceptron](#perceptron) 
- [Function](#function)
- [Activation Function](#activation-function)
- [Loss Function](#loss-function)

### Perceptron

Here's how to create a perceptron instance

```python

from Perceptron.perceptron import Perceptron

p = Perceptron(no_inputs: int, lr: float, act_fn:Function, loss_fn:Function)

```
- **no_inputs**: are the number of inputs of the perceptron
- **lr**: the learning rate of the preceptron
- **act_fn**: the activation function of the perceptron
- **loss_fn**: the loss function of the perceptron

> Note both **act_fn** and **loss_fn** must be instance of the class **Function**

#### Attributes

- **no_input** (*int*) : the number of inputs of the perceptron
- **bias** (*float*): the bias of the perceptron
- **weights** (*list*): the weights of the perceptron
- **act_fn** (*Function*): the activation function of the perceptron
- **loss_fn** (*Function*): the loss function of the perceptron
- **lr** (*float*): the learning rate of the perceptron

---

```python
p.evaluate(inputs: list)
```

Return the prediction of the perceptron
- **inputs**: the inputs list that the vector have to evaluate, and the last element must be the prediced value

> Note: the length of the **inputs** must be *len*(p.no_inputs) + 1  
---

```python
p.train(training_data: list, mini_batches_size: int, n_epoch=30: int)
```

Train the perceptron using mini batch stocastic gradient descend

- **training_data**: the data used to train the preceptron that will be divide in mini batches
- **mini_batches_size**: the size of the mini batch
- **n_epoch**: number of iteration


> Note: the length of the **training_data** must be *len*(p.no_inputs) 
---

### Function

The class function is just a abstract class that represent a mathematical function

The only attribute that it has is:

- **is_diff**: True if the function is differentiable false otherwise

---

```python

fn.compute(a) -> float

```

Abstract method that every child of the Function class implement, and it return the computed value of the given function

- **a**: the input of the function, the type can vary on the function (most of the time is an int or a tuple)

---


```python

fn.compute_derivative(a) -> float

```

Abstract method that every child of the Function class implement, and it return the computed value of the derivative of the given function

- **a**: the input of the function, the type can vary on the function (most of the time is an int or a tuple)

---

### Activation Function

The activation function already included in the package are:

- Heaviside (1/0 step function)
- Identity (the identity function)
- Sign
- ReLU
- Leaky ReLU
- Smooth ReLU
- Sigmoid
- Tanh (Hyperbolic tangent)
- Softmax

```python

from Perceptron.functions.activationFunctions.sigmoid import Sigmoid

fn = Sigmoid()

print(fn.compute(0)) # 0.5

```

### Loss Function

The loss functions already included in the package are:

- Quadratic Loss
- Cross Entropy Loss

## Contributing

Feel free report issues and contribute to the project, making it better.

## Author

Paolo D'Elia

## License 

MIT
