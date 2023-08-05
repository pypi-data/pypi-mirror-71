from pure_ldp.core import FreqOracleClient

import numpy as np
from scipy.linalg import hadamard
from scipy.stats import rv_discrete
import math
import random

class CMSClient(FreqOracleClient):
    def __init__(self, epsilon, hash_funcs, m, is_hadamard=False):
        super().__init__(epsilon, None)
        self.epsilon = epsilon
        self.hash_funcs = hash_funcs
        self.k = len(hash_funcs)
        self.m = m

        self.prob = 1 / (1 + math.pow(math.e, self.epsilon / 2))

        self.is_hadamard = is_hadamard

        if self.is_hadamard:
            self.had = hadamard(self.m)

    def _privatise(self, data, is_hadamard=False):
        j = random.randint(0, self.k-1)
        h_j = self.hash_funcs[j]
        v = [0] * self.m if is_hadamard else np.full(self.m, -1)
        v[h_j(data)] = 1
        return v, j

    def _cms_perturb(self, data):
        v, j = self._privatise(data)
        v[np.random.rand(*v.shape) < self.prob] *= -1 # "flip" bits with prob
        # return np.multiply(v, b), j # Used to generate a random vector b using np.random.choice but it was 3x slower than the above line
        return v, j

    def _hcms_perturb(self, data):
        if not (self.m & (self.m - 1)) == 0:
            raise ValueError("m must be a positive integer, and m must be a power of 2 to use hcms")

        v, j = self._privatise(data, is_hadamard=True)
        b = random.choices([-1, 1], k=1, weights=[self.prob, 1 - self.prob])
        h_j = self.hash_funcs[j]
        w = self.had[:, h_j(data)]
        l = random.randint(0, self.m-1)
        return b[0] * w[l], j, l  # Return (b*w_l, index j, index l)

    def privatise(self, data):
        data = str(data)
        if self.is_hadamard:
            return self._hcms_perturb(data)
        else:
            return self._cms_perturb(data)