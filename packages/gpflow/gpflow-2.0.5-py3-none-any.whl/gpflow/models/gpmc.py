# Copyright 2016 James Hensman, alexggmatthews
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Optional

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from ..base import Parameter
from ..conditionals import conditional
from ..config import default_float, default_jitter
from ..kernels import Kernel
from ..likelihoods import Likelihood
from ..mean_functions import MeanFunction
from ..utilities import to_default_float
from .model import InputData, RegressionData, MeanAndVariance, GPModel
from .training_mixins import InternalDataTrainingLossMixin
from .util import data_input_to_tensor


class GPMC(GPModel, InternalDataTrainingLossMixin):
    def __init__(
        self,
        data: RegressionData,
        kernel: Kernel,
        likelihood: Likelihood,
        mean_function: Optional[MeanFunction] = None,
        num_latent_gps: Optional[int] = None,
    ):
        """
        data is a tuple of X, Y with X, a data matrix, size [N, D] and Y, a data matrix, size [N, R]
        kernel, likelihood, mean_function are appropriate GPflow objects

        This is a vanilla implementation of a GP with a non-Gaussian
        likelihood. The latent function values are represented by centered
        (whitened) variables, so

            v ~ N(0, I)
            f = Lv + m(x)

        with

            L L^T = K

        """
        if num_latent_gps is None:
            num_latent_gps = self.calc_num_latent_gps_from_data(data, kernel, likelihood)
        super().__init__(kernel, likelihood, mean_function, num_latent_gps)
        self.data = data_input_to_tensor(data)
        self.num_data = self.data[0].shape[0]
        self.V = Parameter(np.zeros((self.num_data, self.num_latent_gps)))
        self.V.prior = tfp.distributions.Normal(
            loc=to_default_float(0.0), scale=to_default_float(1.0)
        )

    def log_posterior_density(self) -> tf.Tensor:
        return self.log_likelihood() + self.log_prior_density()

    def _training_loss(self) -> tf.Tensor:
        return -self.log_posterior_density()

    def maximum_log_likelihood_objective(self) -> tf.Tensor:
        return self.log_likelihood()

    def log_likelihood(self) -> tf.Tensor:
        r"""
        Construct a tf function to compute the likelihood of a general GP
        model.

            \log p(Y | V, theta).

        """
        X_data, Y_data = self.data
        K = self.kernel(X_data)
        L = tf.linalg.cholesky(
            K + tf.eye(tf.shape(X_data)[0], dtype=default_float()) * default_jitter()
        )
        F = tf.linalg.matmul(L, self.V) + self.mean_function(X_data)

        return tf.reduce_sum(self.likelihood.log_prob(F, Y_data))

    def predict_f(self, Xnew: InputData, full_cov=False, full_output_cov=False) -> MeanAndVariance:
        """
        Xnew is a data matrix, point at which we want to predict

        This method computes

            p(F* | (F=LV) )

        where F* are points on the GP at Xnew, F=LV are points on the GP at X.

        """
        X_data, Y_data = self.data
        mu, var = conditional(
            Xnew, X_data, self.kernel, self.V, full_cov=full_cov, q_sqrt=None, white=True
        )
        return mu + self.mean_function(Xnew), var
