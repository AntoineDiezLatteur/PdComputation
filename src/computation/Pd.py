"""
File: Pd
Author: antoi
Date: 18/06/2024
Description: 
"""

from scipy.special import comb

class Pd:

    def __init__(self):
        pass

    def global_pd_computation(self, nb, kb, burst_pd):
        global_pd = 0.0
        for k in range(int(kb), int(nb) + 1):
            binomial_coefficient = comb(nb, k)
            term = binomial_coefficient * (burst_pd ** k) * ((1 - burst_pd) ** (nb - k))
            global_pd += term
        return global_pd