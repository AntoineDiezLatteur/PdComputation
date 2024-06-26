"""
File: power
Author: antoi
Date: 18/06/2024
Description: Handle energetic computations
"""

import numpy as np

class Power:

    def __init__(self):
        pass

    def S_computation(self, rcs, range, G_doppler, P, G_antenna, L, G_lambda, G_clutter_rcs, G_pc, L_range, L_4pi3):
        return P + G_antenna + G_doppler + G_lambda + G_clutter_rcs + G_pc - L - L_range - L_4pi3

    def snrc_computation(self, s_clutter : float, s_target : float, noise : float) -> float:
        target_raw_S = 10 ** (s_target / 10)
        if s_clutter == 0:
            snrc = target_raw_S / noise
        else:
            clutter_raw_S = 10 ** (s_clutter / 10)
            snrc = target_raw_S / (clutter_raw_S + noise)
        return snrc
