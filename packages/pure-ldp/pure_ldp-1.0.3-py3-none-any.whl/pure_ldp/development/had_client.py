import math
import numpy as np

from pure_ldp.core import FreqOracleClient

from scipy.linalg import hadamard

class HadamardClient(FreqOracleClient):
    def __init__(self, epsilon, d, index_mapper=None):
        super().__init__(epsilon, index_mapper)
        self.d = d
        self.had = hadamard(2 ** math.ceil(math.log(self.d, 2)))

        self.p = math.exp(self.epsilon) / (math.exp(self.epsilon) + 1)
        self.q = 1.0 / (math.exp(self.epsilon) + 1)

    def _peturb(self, data, seed):
        index = self.index_mapper(data)
        w = self.had[:, index]
        sampled_i = np.random.randint(self.d)

        x = (w[sampled_i] + 1) / 2
        y = x

        p_sample = np.random.random_sample()
        # the following two are equivalent
        # if p_sample > p:
        #     while not y == x:
        #         y = np.random.randint(0, g)
        if p_sample > self.p - self.q:
            # perturb
            y = np.random.randint(0, 2)

        return y, sampled_i

    def privatise(self, data, seed):
        return self._peturb(data, seed)