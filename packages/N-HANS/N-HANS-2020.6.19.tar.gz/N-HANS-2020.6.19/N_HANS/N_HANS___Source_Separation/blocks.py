########################################################################################################################
#                                          N-HANS speech separator: blocks                                             #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#   Description:      Neural network blocks for constructing the N-HANS model.                                         #
#   Authors:          Shuo Liu, Gil Keren, Bjoern Schuller                                                             #
#   Affiliation:      Chair of Embedded Intelligence for Health Care and Wellbeing, University of Augsburg (UAU)  #
#   Version:          2.0                                                                                              #
#   Last Update:      May. 06, 2020                                                                                    #
#   Dependence Files: xxx                                                                                              #
#   Contact:          shuo.liu@informatik.uni-augburg.de                                                               #
########################################################################################################################
#                                                                                                                      #
#   Copyright (C) 2019, Shuo Liu, Gil Keren and Björn Schuller: University of Augsburg.                                #
#                                                                                                                      #
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public    #
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any       #
# later version.                                                                                                       #
#                                                                                                                      #
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied   #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.#
#                                                                                                                      #
# You should have received a copy of the GNU General Public License along with this program. #  If not, see            #
# <http://www.gnu.org/licenses/>.                                                                                      #
#                                                                                                                      #
########################################################################################################################

from __future__ import division, absolute_import, print_function
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.python.util import deprecation

deprecation._PRINT_DEPRECATION_WARNINGS = False
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
FLAGS = tf.compat.v1.flags.FLAGS
#rnn_cell = tf.nn.rnn_cell
#static_rnn = tf.nn.static_rnn


def dense(tensor, out_dim, w_std, b_init, with_bias, scope_name, bias_initializer=None):
    in_dim = tensor.get_shape()[1].value

    with tf.compat.v1.variable_scope(scope_name):
        w = tf.compat.v1.get_variable('w', [in_dim, out_dim], initializer=tf.compat.v1.truncated_normal_initializer(stddev=w_std))
        out = tf.matmul(tensor, w)
        if with_bias:
            if bias_initializer is None:
                b = tf.compat.v1.get_variable('b', [1, out_dim], initializer=tf.constant_initializer(b_init))
            else:
                b = tf.compat.v1.get_variable('b', [1, out_dim], initializer=bias_initializer)
            out += b
        return out


def conv2d(tensor, kernel_shape, strides, out_channels, w_std, b_init, with_bias, padding, scope_name):
    in_channels = tensor.get_shape()[3].value

    with tf.compat.v1.variable_scope(scope_name):
        kernel = tf.compat.v1.get_variable('w', kernel_shape + [in_channels, out_channels],
                                           initializer=tf.compat.v1.truncated_normal_initializer(stddev=w_std))
        out = tf.nn.conv2d(tensor, kernel, strides, padding=padding)
        if with_bias:
            b = tf.compat.v1.get_variable('b', [1, 1, 1, out_channels], initializer=tf.constant_initializer(b_init))
            out += b
        return out


# Input of shape [mb, time, features]
# def lstm(tensor, nlayers, nunits, w_std):
#     with tf.compat.v1.variable_scope('rec_cell', initializer=tf.random_normal_initializer(0.0, w_std)):
#         if nlayers == 1:
#             cell = rnn_cell.LSTMCell(num_units=nunits)
#         else:
#             cell = rnn_cell.MultiRNNCell([rnn_cell.LSTMCell(num_units=nunits) for _ in range(0, nlayers)])
#
#     inputs_as_list = tf.unstack(tf.transpose(tensor, [1, 0, 2]))
#     outputs, states = static_rnn(cell, inputs_as_list, dtype=tf.float32)
#     return outputs, states


def flatten(tensor):
    sh = tensor.get_shape()
    other_dimensions = 1
    for i in range(1, len(sh)):
        other_dimensions *= sh[i].value
    return tf.reshape(tensor, [-1, other_dimensions])


def batch_norm(is_train, tensor, scope_name):
    with tf.compat.v1.variable_scope(scope_name):
        BATCHNORM_MOVING_AVERAGE_DECAY = FLAGS.bn_decay
        # Get the shape of mean, variance, beta, gamma
        mask_shape = [1] * len(tensor.get_shape())
        mask_shape[-1] = tensor.get_shape()[-1].value

        # Create trainable variables to hold beta and gamma
        beta = tf.compat.v1.get_variable('beta', mask_shape, initializer=tf.constant_initializer(0.0))
        gamma = tf.compat.v1.get_variable('gamma', mask_shape, initializer=tf.constant_initializer(1.0))

        # Create non-trainable variables for the population mean and variance, and add them to the
        pop_mean = tf.compat.v1.get_variable('pop_mean', mask_shape, initializer=tf.constant_initializer(0.0),
                                             trainable=False)
        pop_variance = tf.compat.v1.get_variable('pop_variance', mask_shape, initializer=tf.constant_initializer(1.0),
                                                 trainable=False)

        if is_train:
            # Calculate the moments based on the individual batch.
            n_dims = len(tensor.get_shape())
            mean, variance = tf.nn.moments(x=tensor, axes=[i for i in range(0, n_dims - 1)], keep_dims=True)

            # Update the population mean and variance
            pop_mean_update = pop_mean.assign(
                (BATCHNORM_MOVING_AVERAGE_DECAY * pop_mean + (1 - BATCHNORM_MOVING_AVERAGE_DECAY) * mean))
            pop_variance_update = pop_variance.assign(
                (BATCHNORM_MOVING_AVERAGE_DECAY * pop_variance + (1 - BATCHNORM_MOVING_AVERAGE_DECAY) * variance))

            # Add the update ops to a collection, in order to perform them when training
            with tf.control_dependencies([pop_mean_update, pop_variance_update]):
                return tf.nn.batch_normalization(tensor, mean, variance, beta, gamma, variance_epsilon=0.001)

        else:
            # Just use the moving_mean and moving_variance.
            mean = pop_mean
            variance = pop_variance
            return tf.nn.batch_normalization(tensor, mean, variance, beta, gamma, variance_epsilon=0.001)


def reverse_gradient(tensor, gradient_factor):
    return -gradient_factor * tensor + tf.stop_gradient((gradient_factor + 1) * tensor)
