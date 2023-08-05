from pure_ldp.core import FreqOracleServer
from scipy.linalg import hadamard
import numpy as np
import math


class HadamardServer(FreqOracleServer):
    def __init__(self, epsilon, d, index_mapper=None):
        super().__init__(epsilon, d, index_mapper)
        self.set_name("HadamardServer")
        self.rounded_domain = 2 ** math.ceil(math.log(self.d, 2))
        self.had = hadamard(self.rounded_domain)
        self.aggregated_data = np.zeros(self.rounded_domain)
        self.estimated_data = np.zeros(self.rounded_domain)

        self.p = math.exp(self.epsilon) / (math.exp(self.epsilon) + 1)

    def aggregate(self, priv_data, index):
        for i in range(0, self.d):
            w = self.had[:, i]
            x = (w[index] + 1) / 2
            if priv_data == x:
                self.aggregated_data[i] += 1

        self.n += 1

    def estimate(self, data, supress_warnings=False):
        super().estimate(data) # Check and display warnings

        index = self.index_mapper(data)
        a = 2 / (self.p * 2 - 1)
        b = self.n / (self.p * 2 - 1)

        # transformed_data = np.matmul(self.aggregated_data, np.transpose(self.had))
        transformed_data = self.aggregated_data
        self.estimated_data = a * transformed_data - b

        index = self.index_mapper(data)
        return self.estimated_data[index]
