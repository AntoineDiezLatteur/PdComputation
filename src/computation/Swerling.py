"""
File: Swerling
Author: antoi
Date: 03/06/2024
Description: Manage Swerling model computations
"""

import numpy as np
import scipy as sp
from scipy.integrate import quad

class Swerling:

    def __init__(self):
          pass

    def sweling_I_II(self, pfa, snr):
        return pfa ** (1 / (1 + snr))

    def sweling_III_IV(self, pfa, snr):
        c1 = pfa**(2/(2+snr))
        c2 = (2 * snr) / (2 + snr)**2
        return c1 * (1 - c2 * np.log(pfa))

    def sweling_V(self, pfa, snr):
        # inner_integrand = np.exp(2 * np.sqrt(s * x) * np.cos(theta))

        def inner_integrand(theta, s, x):
            return np.exp(2 * np.sqrt(s * x) * np.cos(theta))

        def outer_integrand(x, s):
            inner_integral, _ = quad(inner_integrand, 0, np.pi, args=(s, x))
            return np.exp(-(x + s)) * (1 / np.pi) * inner_integral

        lower_limit = -np.log(pfa)
        result, error = quad(outer_integrand, lower_limit, np.inf, args=(snr,))
        return result