from pure_ldp.core import FreqOracleServer
import math
import numpy as np
from scipy.linalg import hadamard

from pure_ldp.core import generate_hash_funcs

class CMSServer(FreqOracleServer):
    def __init__(self, epsilon, k, m, is_hadamard=False):
        super().__init__(epsilon, None)
        self.k = k
        self.m = m
        self.epsilon = epsilon
        self.hash_funcs = generate_hash_funcs(k,m)
        self.c = (math.pow(math.e, epsilon / 2) + 1) / (math.pow(math.e, epsilon / 2) - 1)
        self.sketch_matrix = np.zeros((self.k, self.m))
        self.transformed_matrix = np.zeros((self.k, self.m))
        self.is_hadamard = is_hadamard

        self.cached_aggregation = self.n
        self.ones = np.ones(self.m)

        if self.is_hadamard:
            self.had = hadamard(self.m)

    def _add_to_cms_sketch(self, data):
        item, hash_index = data
        self.sketch_matrix[hash_index] = self.sketch_matrix[hash_index] + self.k * ((self.c / 2) * item + 0.5 * self.ones)

    def _add_to_hcms_sketch(self, data):
        bit_value, j, l = data
        self.sketch_matrix[j][l] = self.sketch_matrix[j][l] + self.k * self.c * bit_value

    def _transform_sketch_matrix(self):
        return np.matmul(self.sketch_matrix, np.transpose(self.had))

    def get_hash_funcs(self):
        return self.hash_funcs

    def reset(self):
        super().reset()
        self.sketch_matrix = np.zeros((self.k, self.m))

    def aggregate(self, data):
        if self.is_hadamard:
            self._add_to_hcms_sketch(data)
        else:
            self._add_to_cms_sketch(data)
        self.n += 1

    def estimate(self, data, suppress_warnings=False):
        self.check_warnings(suppress_warnings)

        # If it's hadamard we need to transform the sketch matrix
            # To prevent this being performance intensive, we only transform if new data has been aggregated since it was last transformed

        if self.is_hadamard and self.cached_aggregation < self.n:
            self.cached_aggregation = self.n
            self.transformed_matrix = self._transform_sketch_matrix()

        sketch = self.sketch_matrix if not self.is_hadamard else self.transformed_matrix

        data = str(data)
        k, m = sketch.shape
        freq_sum = 0
        for i in range(0, k):
            freq_sum += sketch[i][self.hash_funcs[i](data)]
        return (m / (m - 1)) * ((1 / k) * freq_sum - (self.n / m))
