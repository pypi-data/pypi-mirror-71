
# Testing for development

import numpy as np
import math
from collections import Counter

from pure_ldp.development.priv_count_sketch.pcs_client import PCSClient
from pure_ldp.development.priv_count_sketch.pcs_server import PCSServer

from pure_ldp.development.apple_cms.cms_client import CMSClient
from pure_ldp.development.apple_cms.cms_sever import CMSServer

from pure_ldp.development.explicit_hist.eh_client import ExplicitHistClient
from pure_ldp.development.explicit_hist.eh_server import  ExplicitHistServer

from pure_ldp.development.hashtogram.hashtogram_client import HashtogramClient
from pure_ldp.development.hashtogram.hashtogram_server import HashtogramServer

# Super simple synthetic dataset
data = np.concatenate(([1 ] *8000, [2 ] *4000, [3 ] *1000, [4 ] *500, [5 ] *1000, [6 ] *1800, [7 ] *2000, [8 ] *300))
original_freq = list(Counter(data).values()) # True frequencies of the dataset

# Parameters for experiment
epsilon = 3
d = 8
is_the = True
is_oue = True
is_olh = True

l = 250
N = 18600
w = 250

# Optimal Local Hashing (OLH)
client_pcs = PCSClient(epsilon ,l ,w)
server_pcs = PCSServer(epsilon ,l ,w)

# Apple's Count Mean Sketch (CMS)
server_cms = CMSServer(epsilon, 2, 2048, is_hadamard=True)
client_cms = CMSClient(epsilon, server_cms.get_hash_funcs(), 2048, is_hadamard=True)

# Explicit Histogram
client_eh = ExplicitHistClient(epsilon, d)
server_eh = ExplicitHistServer(epsilon, d)

# Hashtogram
server_hashto = HashtogramServer(epsilon, 100, 100)
client_hashto = HashtogramClient(epsilon, 100, 100, server_hashto.get_hash_funcs())

# Simulate client-side privatisation + server-side aggregation
for index, item in enumerate(data):
    # priv_pcs_data = client_pcs.privatise(item)
    # priv_eh_data = client_eh.privatise(item)
    priv_hashto_data = client_hashto.privatise(item)
    # priv_cms_data = client_cms.privatise(item)
    # server_cms.aggregate(priv_cms_data)

    # server_pcs.aggregate(priv_pcs_data)
    # server_eh.aggregate(priv_eh_data)
    server_hashto.aggregate(priv_hashto_data)

# Simulate server-side estimation
pcs_estimates = []
cms_estimates = []
eh_estimates = []
hashto_estimates = []
mse_arr = np.zeros(4)

for i in range(0, d):
    # cms_estimates.append(round(server_cms.estimate(i+1)))
    # pcs_estimates.append(round(server_pcs.estimate(i+1)))
    # eh_estimates.append(round(server_eh.estimate(i+1)))
    hashto_estimates.append(round(server_hashto.estimate(i+1)))

# Calculate variance
for i in range(0 ,d):
    # mse_arr[1] += (cms_estimates[i] - original_freq[i])**2
    # mse_arr[0] += (pcs_estimates[i] - original_freq[i])**2
    # mse_arr[2] += (eh_estimates[i]-original_freq[i])**2
    mse_arr[3] += (hashto_estimates[i]-original_freq[i])**2

mse_arr = mse_arr /d

# Output:
print("\n")
print("Experiment run on a dataset of size", len(data), "with d=" ,d, "and epsilon=" ,epsilon, "\n")
print("Apple Count Mean Sketch (CMS) Variance: ", mse_arr[1])
print("Private Count Sketch (PCS) Variance: ", mse_arr[0])
print("ExplicitHist (EH) Variance: ", mse_arr[2])
print("Hashtogram Variance:", mse_arr[3])

print("\n")
print("Original Frequencies:", original_freq)
print("CMS Estimates:", cms_estimates)
print("PCS Estimates:", pcs_estimates)
print("EH Estimates:", eh_estimates)
print("Hashtogram Estimates:", hashto_estimates)

print("Note: We round estimates to the nearest integer")
