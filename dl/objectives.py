# -*- coding: UTF-8 -*-

import theano.tensor as T

from .utils import _EPSILON


def mean_squared_error(prediction, target):
    return T.mean(T.square(prediction - target), axis=-1)


def root_mean_squared_error(prediction, target):
    return T.sqrt(T.mean(T.square(prediction - target), axis=-1))


def mean_absolute_error(prediction, target):
    return T.mean(T.abs(prediction - target), axis=-1)


def hinge(prediction, target):
    return T.mean(T.maximum(1. - target * prediction, 0.), axis=-1)


def squared_hinge(prediction, target):
    return T.mean(T.square(T.maximum(1. - target * prediction, 0.)), axis=-1)


def binary_crossentropy(prediction, target):
    clip_pred = T.clip(prediction, _EPSILON, 1 - _EPSILON)
    return T.mean(T.nnet.binary_crossentropy(clip_pred, target), axis=-1)


def categorical_crossentropy(prediction, target):
    prediction /= prediction.sum(axis=-1, keepdims=True)
    prediction = T.clip(prediction, _EPSILON, 1 - _EPSILON)
    return T.mean(T.nnet.categorical_crossentropy(prediction, target), axis=-1)