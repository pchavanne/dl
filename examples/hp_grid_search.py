#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

import dl
from dl.hyperparameters import *
from dl.model import *

# load the data
datafile = 'mnist.pkl.gz'
if not os.path.isfile(datafile):
    import urllib
    origin = 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
    print 'Downloading data from %s' % origin
    urllib.urlretrieve(origin, datafile)
data = dl.data.Data(datafile)

# Hyperparameters
hps = Hyperparameters()
hps('batch_size', 500, [50, 100, 500, 1000])
hps('n_epochs', 1000)
hps('learning_rate', 0.1, [0.001, 0.01, 0.1, 1])
hps('l1_reg', 0.00, [0, 0.0001, 0.001, 0.01])
hps('l2_reg', 0.0001, [0, 0.0001, 0.001, 0.01])
hps('activation', tanh, [tanh, sigmoid, relu])
hps('initialisation', glorot_uniform, [glorot_uniform, glorot_normal])
hps('patience', 10000)

reports = []


@timer(' Grid Search')
def grid_search():
    for hp in hps:
        # create the model
        model = dl.model.Model(name='mlp grid search', data=data)
        # add the hyperparameters to the model
        model.hp = hp
        # Create connected layers
        # Input layer
        l_in = InputLayer(shape=(hp.batch_size, 28 * 28), input_var=model.x, name='Input')
        # Dense Layer 1
        l_hid1 = DenseLayer(incoming=l_in, nb_units=500, W=glorot_uniform, l1=hp.l1_reg,
                            l2=hp.l2_reg, activation=hp.activation, name='Hidden layer 1')
        # Dense Layer 2
        l_hid2 = DenseLayer(incoming=l_hid1, nb_units=500, W=glorot_uniform, l1=hp.l1_reg,
                            l2=hp.l2_reg, activation=hp.activation, name='Hidden layer 2')
        # Logistic regression Layer
        l_out = LogisticRegression(incoming=l_hid2, nb_class=10, l1=hp.l1_reg,
                                   l2=hp.l2_reg, name='Logistic regression')

        # Create network and add layers
        net = Network('mlp')
        net.add(l_in)
        net.add(l_hid1)
        net.add(l_hid2)
        net.add(l_out)
        # add the network to the model
        model.network = net

        # updates method
        model.updates = dl.updates.sgd
        reports.append((hp, model.train()))

        report_file = open('reports.pkl', 'wb')
        cPickle.dump(reports, report_file)
        report_file.close()


# Grid search
grid_search()


# Report Analysis
import cPickle
import pandas as pd
report_file = open('reports.pkl', 'rb')
reports = cPickle.load(report_file)
reports = pd.DataFrame(reports)
param_reports = pd.DataFrame.from_records(reports['parameters'])
pd_report = pd.DataFrame(reports,
                         columns=['iteration', 'test', 'validation', 'training time'])
reports = pd.concat([param_reports, pd_report], axis=1)

reports.to_html(open('/home/philippe/Python/Theano/report.html', 'w'))

print reports.loc[reports['validation'].idxmin()]
