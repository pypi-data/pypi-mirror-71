import numpy as np
import math
import random

# Used for simulations only
    # Works only for a fixed known domain of elements

from pure_ldp.core import FreqOracleClient

class ExplicitHistClient(FreqOracleClient):
    # The ExplicitHist algorithm requires us to set values of our matrix by using the value of the data to be privatised as an index
    # To get around this for non-integer data, we use an index_map, which takes a data element and produces an index of the matrix
        # Typically we use a hash function to do this

    def __init__(self, epsilon, d, index_mapper=None):
        super().__init__(epsilon, d ,index_mapper)
        self.prob = 1 / ((math.e ** epsilon) + 1)

        # Constructing randomised dataset (Step 1 of algorithm 5)
        # TODO: This should be generated for each user
        # self.z = np.random.choice([1, -1], size=self.d)

    # Algorithm 4
    def _perturb(self, data):
        return random.choices([data, -data], k=1, weights=[1 - self.prob, self.prob])[0]

    def privatise(self, data):
        index = self.index_mapper(data)
        z = np.random.choice([1, -1], size=self.d)
        perturbed_bit = self._perturb(z[index])
        return perturbed_bit, z

