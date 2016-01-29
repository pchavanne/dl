# -*- coding: UTF-8 -*-

from .init import *
from .utils import *
from .objectives import *

# from theano.tensor.shared_randomstreams import RandomStreams
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams

T_rng = RandomStreams(np_rng.randint(2 ** 30))


class Layer(object):
    def __init__(self, incoming, name=None):
        if isinstance(incoming, tuple):
            self.input_shape = incoming
            self.input_layer = None
        else:
            self.input_shape = incoming.output_shape
            self.input_layer = incoming

        self.name = name
        self.params = []
        self.reguls = 0

    @property
    def output_shape(self):
        return self.input_shape

    def get_output(self, **kwargs):
        raise NotImplementedError


class InputLayer(Layer):
    def __init__(self, shape, input_var=None, name='Input'):
        super(InputLayer, self).__init__(shape, name)
        self.input = input_var

    def get_output(self, **kwargs):
        return self.input


class DenseLayer(Layer):
    def __init__(self, incoming, nb_units, name=None,
                 W=glorot_uniform, b=(constant, {'value': 0.0}),
                 activation=tanh, l1=None, l2=None):
        super(DenseLayer, self).__init__(incoming, name)
        self.shape = (self.input_shape[1], nb_units)
        if isinstance(W, theano.compile.SharedVariable):
            self.W = W
        else:
            self.W = initializer(W, shape=self.shape, name='W')
        self.params.append(self.W)
        if isinstance(b, theano.compile.SharedVariable):
            self.b = b
        else:
            self.b = initializer(b, shape=(self.shape[1],), name='b')
        self.params.append(self.b)
        self.activation = activation
        if l1:
            self.reguls += l1 * T.mean(T.abs_(self.W))
        if l2:
            self.reguls += l2 * T.mean(T.sqr(self.W))

    @property
    def output_shape(self):
        return self.input_shape[0], self.shape[1]

    def get_reguls(self):
        return self.reguls

    def get_output(self, **kwargs):
        X = self.input_layer.get_output(**kwargs)
        return self.activation(T.dot(X, self.W) + self.b)


class UnsupervisedLayer(DenseLayer):
    def __init__(self, incoming, nb_units, hyperparameters, **kwargs):
        super(UnsupervisedLayer, self).__init__(incoming, nb_units, **kwargs)
        self.hp = hyperparameters
        self.unsupervised_params = list(self.params)

    def get_encoded_input(self, stochastic=False, **kwargs):
        raise NotImplementedError

    def get_unsupervised_cost(self, stochastic=False, **kwargs):
        raise NotImplementedError


class LogisticRegression(DenseLayer):
    def __init__(self, incoming, nb_class, W=constant, activation=softmax, **kwargs):
        super(LogisticRegression, self).__init__(incoming, nb_class, W=W,
                                                 activation=activation, **kwargs)


class Dropout(Layer):
    def __init__(self, incoming, corruption_level=0.5, **kwargs):
        super(Dropout, self).__init__(incoming, **kwargs)
        self.p = 1 - corruption_level

    def get_output(self, stochastic=False, **kwargs):
        X = self.input_layer.get_output(stochastic=stochastic, **kwargs)
        if self.p > 0 and stochastic:
            X = X * T_rng.binomial(self.input_shape, n=1, p=self.p, dtype=floatX)
        return X


class MaxPool(Layer):
    def __init__(self, incoming,  **kwargs):
        super(Dropout, self).__init__(incoming, **kwargs)
        # TODO implement MaxPool class

    def get_output(self, stochastic=False, **kwargs):
        raise NotImplementedError


class ConvLayer(DenseLayer):
    def __init__(self, incoming,  **kwargs):
        super(ConvLayer, self).__init__(incoming, **kwargs)
        # TODO implement ConvLayer class

    def get_output(self, stochastic=False, **kwargs):
        raise NotImplementedError


class Dropconnect(DenseLayer):
    def __init__(self, incoming, nb_units, corruption_level=0.5, **kwargs):
        super(Dropconnect, self).__init__(incoming, nb_units, **kwargs)
        self.p = 1 - corruption_level

    def get_output(self, stochastic=False, **kwargs):
        X = self.input_layer.get_output(stochastic=stochastic, **kwargs)
        if self.p > 0 and stochastic:
            self.W = self.W * T_rng.binomial(self.shape, n=1, p=self.p, dtype=floatX)
        return self.activation(T.dot(X, self.W) + self.b)


class AutoEncoder(UnsupervisedLayer):
    def __init__(self, incoming, nb_units, hyperparameters, corruption_level=0.5, W=glorot_uniform,
                 b_prime=(constant, {'value': 0.0}), activation=sigmoid, **kwargs):
        super(AutoEncoder, self).__init__(incoming, nb_units, hyperparameters, W=W,
                                          activation=activation, **kwargs)
        self.W_prime = self.W.T
        if isinstance(b_prime, theano.compile.SharedVariable):
            self.b_prime = b_prime
        else:
            self.b_prime = initializer(b_prime, shape=(self.shape[0],), name='b_prime')
        self.unsupervised_params.append(self.b_prime)
        self.p = 1 - corruption_level

    def get_encoded_input(self, stochastic=False, **kwargs):
        X = self.input_layer.get_output(stochastic=stochastic, **kwargs)
        if self.p > 0 and stochastic:
            X = X * T_rng.binomial(self.input_shape, n=1, p=self.p, dtype=floatX)
        Y = self.activation(T.dot(X, self.W) + self.b)
        Z = self.activation(T.dot(Y, self.W_prime) + self.b_prime)
        return Z

    def get_unsupervised_cost(self, stochastic=False, **kwargs):
        X = self.input_layer.get_output(stochastic=stochastic, **kwargs)
        Z = self.get_encoded_input(stochastic=stochastic, **kwargs)
        cost = T.mean(categorical_crossentropy(Z, X))
        return cost


class RBM(UnsupervisedLayer):
    def __init__(self, incoming, nb_units, corruption_level=0.5, **kwargs):
        super(RBM, self).__init__(incoming, nb_units, **kwargs)
        # TODO implement RBM class

    def get_encoded_input(self, stochastic=False, **kwargs):
        raise NotImplementedError

    def get_unsupervised_cost(self, stochastic=False, **kwargs):
        raise NotImplementedError


class LSTM(Layer):
    def __init__(self, incoming, **kwargs):
        super(LSTM, self).__init__(self, incoming, **kwargs)
        # TODO implement LSTM class

    def get_output(self, **kwargs):
        raise NotImplementedError

