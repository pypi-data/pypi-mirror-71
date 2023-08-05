# A non-static rewrite of the PrivCountSketch.py class ()

# This is mainly used in simulations to test the PrivCountSketch frequency oracle
# The core logic for private count sketch [Charikar-Chen-Farach-Colton 2004]

import numpy as np
from bitstring import BitArray
import math

from pure_ldp.core import FreqOracleClient
from pure_ldp.development.priv_count_sketch import get_sha256_hash_arr

class PCSClient(FreqOracleClient):
    def __init__(self, epsilon, l, w):
        super().__init__(epsilon, None)
        self.l = l
        self.w = w
        self.epsilon = epsilon

    # Duchi-Jordan-Wainwright 2013, Bassily-Smith-2015 randomizer
    def _perturb(self, data):
        bitVec = data
        unsigned_bits = np.abs(bitVec)
        assert (np.sum(unsigned_bits) == 1.0), 'Incorrect number of bits set in the data vector'
        index_of_data = np.where(unsigned_bits == 1)[0][0]

        un_biased_pm_bits = 2 * np.random.binomial(1, 0.5, len(bitVec)) - 1
        un_biased_pm_bits[index_of_data] = 0
        privatized_bit_vec = un_biased_pm_bits + bitVec

        bias = math.exp(self.epsilon) / (1 + math.exp(self.epsilon))
        privatized_bit_vec[index_of_data] *= (2 * np.random.binomial(1,bias) - 1)
        return privatized_bit_vec

    def privatise(self, data):
        data = str(data)
        # assert (isinstance(data, str) is True), 'Data should be a string'

        hash_id = np.random.randint(0, self.l)
        message_in_bit_array = get_sha256_hash_arr(hash_id, data)

        h_loc = BitArray(message_in_bit_array[0: int(math.log(self.w, 2))]).uint
        g_val = 2 * message_in_bit_array[int(math.log(self.w, 2))] - 1

        data_vector = np.zeros(self.w)
        data_vector[h_loc] = g_val

        privatized_vec = self._perturb(data_vector)
        return privatized_vec, hash_id
