
from pure_ldp.core import FreqOracleServer, generate_hash_funcs

import math
import numpy as np


class HashtogramServer(FreqOracleServer):
    def __init__(self, epsilon, R, T, use_median=False, index_mapper=None):
        super().__init__(epsilon, None, index_mapper)
        self.R = R
        self.T = T
        self.hash_family = generate_hash_funcs(R, T)
        self.use_median = use_median

        # Constructing randomised dataset (Step 1 of algorithm 5)
        self.y = []
        self.Z = []
        self.partition = [[] for i in range(self.R)]

        self.set_name("HashtogramServer")

    def get_hash_funcs(self):
        return self.hash_family

    def reset(self):
        super().reset()
        self.y = []
        self.Z = []
        self.partition = [[] for i in range(self.R)]

    def aggregate(self, data):
        z = data[1]
        item = data[0]
        partition_number = data[2]

        self.y.append(item)
        self.Z.append(z)
        self.partition[partition_number].append(self.n) # Assign user to their partition
        self.n += 1

    # Step 2 of Algorithm 7, creates an oracle for a specific partition
    def __freq_partition_estimate(self,r,t):
        const = ((math.e ** self.epsilon) + 1) / ((math.e ** self.epsilon) - 1)

        sum = 0
        for j in self.partition[r]:
            sum = sum + (self.y[j] * self.Z[j][t])
        return const * sum

    # Step 2 and 3 of Algorithm 7
    def estimate(self, data, suppress_warnings=False):
        freq = 0
        data = str(data)
        const = ((math.e ** self.epsilon) + 1) / ((math.e ** self.epsilon) - 1)

        frequency_estimates = [0] * self.R

        for i in range(0, self.R):
            hashed_data = self.hash_family[i](data)

            frequency_estimates[i] = self.__freq_partition_estimate(i, hashed_data)

        # BNST Paper uses median for Hashtogram, mean seems to give better results.
        if self.use_median:
            return self.R * np.median(frequency_estimates)
        else:
            return self.R * np.mean(frequency_estimates)
