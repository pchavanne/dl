# -*- coding: UTF-8 -*-

from dl.hyperparameters import *
from dl.model import *

__all__ = ['logistic_regression',
           'mlp',
           'dropout',
           'dropconnect',
           'convpool',
           'lenet5',
           'autoencoder',
           'denoising_autoencoder',
           'stacked_denoising_autoencoder',
           'rbm',
           'dbn',
           'lstm'
           ]


def logistic_regression(input_var=None):
    """Logistic Regression"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 600)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.13)
    hp('patience', 5000)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_in, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('logistic_regression')
    net.add(l_in)
    net.add(l_out)

    return net, hp


def mlp(input_var=None):
    """Multi Layer Perceptron"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.1)
    hp('l1_reg', 0.00)
    hp('l2_reg', 0.0001)
    hp('patience', 5000)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # Dense Layer
    l_hid1 = DenseLayer(incoming=l_in, nb_units=500, W=glorot_uniform, l1=hp.l1_reg,
                        l2=hp.l2_reg, activation=relu, name='Hidden layer 1')
    # Dense Layer
    l_hid2 = DenseLayer(incoming=l_hid1, nb_units=500, W=glorot_uniform, l1=hp.l1_reg,
                        l2=hp.l2_reg, activation=relu, name='Hidden layer 2')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_hid2, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('mlp')
    net.add(l_in)
    net.add(l_hid1)
    net.add(l_hid2)
    net.add(l_out)

    return net, hp


def dropout(input_var=None):
    """Dropout"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # Dropout Layer
    l_dro1 = Dropout(incoming=l_in, corruption_level=0.4, name='Dropout 1')
    # Dense Layer
    l_hid1 = DenseLayer(incoming=l_dro1, nb_units=500, W=glorot_uniform,
                        activation=relu, name='Hidden layer 1')
    # Dropout Layer
    l_dro2 = Dropout(incoming=l_hid1, corruption_level=0.2, name='Dropout 2')
    # Dense Layer
    l_hid2 = DenseLayer(incoming=l_dro2, nb_units=500, W=glorot_uniform,
                        activation=relu, name='Hidden layer 2')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_hid2, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('dropout')
    net.add(l_in)
    net.add(l_dro1)
    net.add(l_hid1)
    net.add(l_dro2)
    net.add(l_hid2)
    net.add(l_out)

    return net, hp


def dropconnect(input_var=None):
    """DropConnect"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # DropConnect Layer
    l_dc1 = Dropconnect(incoming=l_in, nb_units=500, corruption_level=0.4,
                        W=glorot_uniform, activation=relu, name='Dropconnect layer 1')
    # DropConnect Layer
    l_dc2 = Dropconnect(incoming=l_dc1, nb_units=500, corruption_level=0.2,
                        W=glorot_uniform, activation=relu, name='Dropconnect layer 2')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_dc2, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('dropconnect')
    net.add(l_in)
    net.add(l_dc1)
    net.add(l_dc2)
    net.add(l_out)

    return net, hp


def convpool(input_var=None):
    """Convolution and MaxPooling"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 500)
    hp('n_epochs', 200)
    hp('learning_rate', 0.1)
    hp('patience', 10000)

    # Create connected layers
    image_shape = (hp.batch_size, 1, 28, 28)
    filter_shape = (20, 1, 5, 5)
    poolsize = (2, 2)
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # ConvLayer needs 4D Tensor
    l_rs = ReshapeLayer(incoming=l_in, output_shape=image_shape)
    # ConvPool Layer
    l_cp = ConvPoolLayer(incoming=l_rs, poolsize=poolsize, image_shape=image_shape,
                         filter_shape=filter_shape, name='ConvPool layer')
    # flatten convpool output
    l_fl = FlattenLayer(incoming=l_cp, ndim=2)
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_fl, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('convpool')
    net.add(l_in)
    net.add(l_rs)
    net.add(l_cp)
    net.add(l_out)

    return net, hp


def lenet5(input_var=None):
    """LeNet-5"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 500)
    hp('n_epochs', 200)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Create connected layers
    image_shape = (hp.batch_size, 1, 28, 28)
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # ConvLayer needs 4D Tensor
    l_rs = ReshapeLayer(incoming=l_in, output_shape=image_shape)
    # first convpool
    image_shape = (hp.batch_size, 1, 28, 28)
    filter_shape = (20, 1, 5, 5)
    poolsize = (2, 2)
    fan_in = np.prod(filter_shape[1:])
    fan_out = filter_shape[0] * np.prod(filter_shape[2:]) / np.prod(poolsize)
    init = (glorot_uniform, {'shape': (fan_in, fan_out), 'gain': 1.})
    l_cp1 = ConvPoolLayer(incoming=l_rs, poolsize=poolsize, image_shape=image_shape,
                          filter_shape=filter_shape, W=init, activation=tanh, name='ConvPool layer 1')
    # second convpool
    image_shape = (hp.batch_size, 20, 12, 12)
    filter_shape = (50, 20, 5, 5)
    poolsize = (2, 2)
    fan_in = np.prod(filter_shape[1:])
    fan_out = filter_shape[0] * np.prod(filter_shape[2:]) / np.prod(poolsize)
    init = (glorot_uniform, {'shape': (fan_in, fan_out), 'gain': 1.})
    l_cp2 = ConvPoolLayer(incoming=l_cp1, poolsize=poolsize, image_shape=image_shape,
                          filter_shape=filter_shape, W=init, activation=tanh, name='ConvPool layer 2')
    # flatten convpool output
    l_fl = FlattenLayer(incoming=l_cp2, ndim=2)
    # Dense Layer
    l_hid1 = DenseLayer(incoming=l_fl, nb_units=500, W=glorot_uniform, activation=tanh, name='Hidden layer 1')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_hid1, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('convpool')
    net.add(l_in)
    net.add(l_rs)
    net.add(l_cp1)
    net.add(l_cp2)
    net.add(l_fl)
    net.add(l_hid1)
    net.add(l_out)

    return net, hp


def autoencoder(input_var=None):
    """Autoencoder"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Unsupervised hyperparameters
    hp_ae = Hyperparameters()
    hp_ae('batch_size', hp.batch_size)
    hp_ae('n_epochs', 15)
    hp_ae('learning_rate', 0.01)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # Auto Encoder Layer
    l_ae1 = AutoEncoder(incoming=l_in, nb_units=100, hyperparameters=hp_ae,
                        corruption_level=0.0, name='AutoEncoder')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_ae1, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('autoencoder')
    net.add(l_in)
    net.add(l_ae1)
    net.add(l_out)

    return net, hp


def denoising_autoencoder(input_var=None):
    """Denoising Autoencoder"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Unsupervised hyperparameters
    hp_ae = Hyperparameters()
    hp_ae('batch_size', hp.batch_size)
    hp_ae('n_epochs', 15)
    hp_ae('learning_rate', 0.01)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # Auto Encoder Layer
    l_ae1 = AutoEncoder(incoming=l_in, nb_units=500, hyperparameters=hp_ae,
                        corruption_level=0.3, activation=relu, name='Denoising AutoEncoder')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_ae1, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('denoising_autoencoder')
    net.add(l_in)
    net.add(l_ae1)
    net.add(l_out)

    return net, hp


def stacked_denoising_autoencoder(input_var=None):
    """Stacked Denoising Autoencoder"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Unsupervised hyperparameters
    hp_ae = Hyperparameters()
    hp_ae('batch_size', hp.batch_size)
    hp_ae('n_epochs', 15)
    hp_ae('learning_rate', 0.01)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # Auto Encoder Layer
    l_ae1 = AutoEncoder(incoming=l_in, nb_units=500, hyperparameters=hp_ae,
                        corruption_level=0.2, name='Denoising AutoEncoder 1')
    # Auto Encoder Layer
    l_ae2 = AutoEncoder(incoming=l_ae1, nb_units=500, hyperparameters=hp_ae,
                        corruption_level=0.4, name='Denoising AutoEncoder 2')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_ae2, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('stacked_denoising_autoencoder')
    net.add(l_in)
    net.add(l_ae1)
    net.add(l_ae2)
    net.add(l_out)

    return net, hp


def rbm(input_var=None):
    """Restricted Boltzmann Machine"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Unsupervised hyperparameters
    hp_ae = Hyperparameters()
    hp_ae('batch_size', hp.batch_size)
    hp_ae('n_epochs', 15)
    hp_ae('learning_rate', 0.01)

    # Create connected layers
    # Input layer
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    # Restricted Boltzmann Machine Layer
    l_rbm1 = RBM(incoming=l_in, nb_units=500, hyperparameters=hp_ae,
                 name='Restricted Boltzmann Machine')
    # Logistic regression Layer
    l_out = LogisticRegression(incoming=l_rbm1, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('rbm')
    net.add(l_in)
    net.add(l_rbm1)
    net.add(l_out)

    return net, hp


def dbn(input_var=None):
    """Deep Belief Network"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Unsupervised hyperparameters
    hp_ae = Hyperparameters()
    hp_ae('batch_size', hp.batch_size)
    hp_ae('n_epochs', 15)
    hp_ae('learning_rate', 0.01)

    # Create connected layers
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    l_rbm1 = RBM(incoming=l_in, nb_units=500, hyperparameters=hp_ae,
                 name='Restricted Boltzmann Machine 1')
    l_rbm2 = RBM(incoming=l_in, nb_units=500, hyperparameters=hp_ae,
                 name='Restricted Boltzmann Machine 2')
    l_out = LogisticRegression(incoming=l_rbm2, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('dbn')
    net.add(l_in)
    net.add(l_rbm1)
    net.add(l_out)

    return net, hp


def lstm(input_var=None):
    """Long Short Term Memory"""

    # Hyperparameters
    hp = Hyperparameters()
    hp('batch_size', 20)
    hp('n_epochs', 1000)
    hp('learning_rate', 0.01)
    hp('patience', 10000)

    # Create connected layers
    l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=input_var, name='Input')
    l_lstm = RBM(incoming=l_in, nb_units=500, name='Long Short Term Memory')
    l_out = LogisticRegression(incoming=l_lstm, nb_class=10, name='Logistic regression')

    # Create network and add layers
    net = Network('lstm')
    net.add(l_in)
    net.add(l_lstm)
    net.add(l_out)

    return net, hp

