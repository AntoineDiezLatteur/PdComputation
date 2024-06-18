"""
File: Geometry
Author: antoi
Date: 18/06/2024
Description: Handle the geometrical computations
"""

import numpy as np

class Geometry:

    def __init__(self):
        pass

    def ds_computation(self, range, c, h, theta_az, tau):
        if h/range > 1 or h/range < -1:
            return 0
        else:
            a1 = 0.5 * range * np.tan(np.deg2rad(theta_az/2))
            a2 = (c * tau) / (np.cos(np.arcsin(h / range)))
            a3 = np.sqrt(np.pi / (2* np.log(2)))
        return a1 * a2 * a3

    def r_horizon(self, z, h, er):
        return np.sqrt(2 * er * z) + np.sqrt(2 * er * h)

    def theta_horizon(self, h, er):
        return - np.sqrt((2 * h)/er)

    def is_visible(self, range, theta, z, theta_horizon, r_horizon):
        if theta >= theta_horizon :
            return True
        else:
            if range < r_horizon:
                if z >= 0:
                    return True
                else:
                    return False
            else:
                return False

    def theta_computation(self, range, h, er, z):
        upper =  (er + z)**2 - (er + h)**2 - range**2
        lower = 2 * range * (er + h)
        return np.arcsin(upper / lower)
