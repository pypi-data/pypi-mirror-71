import numpy as np
import math
import random

from pure_ldp.core import FreqOracleClient


class HashtogramClient(FreqOracleClient):
    def __init__(self, epsilon, R, T, hash_family, index_mapper=None):
        super().__init__(epsilon, None, index_mapper)
        self.prob = 1 / ((math.e ** self.epsilon) + 1)
        self.T = T
        self.R = R
        self.hash_family = hash_family

        # Constructing randomised dataset (Step 1 of algorithm 5)
        # TODO: This should be generated for each user
        # self.z = np.random.choice([1, -1], size=self.d)

    # Algorithm 4
    def _perturb(self, data):
        x = random.choices([data, -data], k=1, weights = [1 - self.prob, self.prob])[0]
        return x

    def privatise(self, data):
        index = self.index_mapper(data)
        z = np.random.choice([1, -1], size=self.T)
        r = random.randint(0, self.R-1) # Assign partition to user

        index = self.hash_family[r](str(data))
        perturbed_bit = self._perturb(z[index])
        return perturbed_bit, z, r
