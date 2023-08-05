import numpy as np
import math

from bitstring import BitArray

from pure_ldp.core import FreqOracleServer
from pure_ldp.development.priv_count_sketch import get_sha256_hash_arr

class PCSServer(FreqOracleServer):
    def __init__(self, epsilon, l, w, use_median=False):
        super().__init__(epsilon, None)
        self.l = l
        self.w = w
        self.sketch_matrix = np.zeros((self.l, self.w))
        self.use_median = use_median

    def _set_sketch_element(self, data, hash_id):
        self.sketch_matrix[hash_id] += (data * self.l)

    def write_sketch(self, sketch_location):
        np.save(sketch_location, self.sketch_matrix)

    def read_sketch(self, sketch_location):
        self.sketch_matrix = np.load(sketch_location)

    def reset(self):
        super().reset()
        self.sketch_matrix = np.zeros((self.l, self.w))

    def aggregate(self, data):
        hash_id = data[1]
        data = data[0]

        self._set_sketch_element(data, hash_id)
        self.n += 1

    def estimate(self, data, suppress_warnings=False):
        self.check_warnings(suppress_warnings)
        data = str(data)
        # assert (isinstance(data, str) is True), 'Data should be a string'

        weak_freq_estimates = np.zeros(self.l)
        for hashId in range(0, self.l):
            message_in_bit_array = get_sha256_hash_arr(hashId, data)

            h_loc = BitArray(message_in_bit_array[0: int(math.log(self.w, 2))]).uint
            g_val = 2 * message_in_bit_array[int(math.log(self.w, 2))] - 1
            weak_freq_estimates[hashId] = g_val * self.sketch_matrix[hashId, h_loc]

        if self.use_median:
            return np.median(weak_freq_estimates)
        else:
            return np.mean(weak_freq_estimates)
