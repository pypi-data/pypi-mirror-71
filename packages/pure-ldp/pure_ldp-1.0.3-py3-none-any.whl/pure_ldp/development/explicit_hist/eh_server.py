from pure_ldp.core import FreqOracleServer

import math
import numpy as np


class ExplicitHistServer(FreqOracleServer):
    def __init__(self, epsilon, d, index_mapper=None):
        super().__init__(epsilon, d, index_mapper)

        # Constructing randomised dataset (Step 1 of algorithm 5)
        self.y = []
        self.Z = []
        self.set_name("ExplicitHistServer")

    def reset(self):
        super().reset()
        self.y = []
        self.Z = []

    def aggregate(self, data):
        z = data[1]
        item = data[0]

        self.y.append(item)
        self.Z.append(z)
        self.n += 1

    # Step 2 of Algorithm 5
    def estimate(self, data, suppress_warnings=False):
        self.check_warnings(suppress_warnings)

        freq = 0
        for j in range(0, self.n):
            i = self.index_mapper(data)
            freq += self.y[j] * self.Z[j][i]

        const = ((math.e ** self.epsilon) + 1) / ((math.e ** self.epsilon) - 1)

        return const * freq
