"""
File: Pd
Author: antoi
Date: 18/06/2024
Description: Handle probability of detection computations
"""

from scipy.special import comb
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

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

if __name__ == '__main__' :
    # # Define the number of points
    # num_points = 100
    #
    # # Generate the coordinates for the line
    # x = np.linspace(0, 10, num_points)
    # y = np.ones(num_points)  # Straight horizontal line at y=1
    #
    # # Define the indices where the color should change
    # color_change_indices = [30, 60, 100]  # Example indices
    #
    # # Create segments
    # points = np.array([x, y]).T.reshape(-1, 1, 2)
    # segments = np.concatenate([points[:-1], points[1:]], axis=1)
    #
    # # Define colors for each segment
    # colors = ['red'] * color_change_indices[0] + ['green'] * (color_change_indices[1] - color_change_indices[0]) + [
    #     'blue'] * (color_change_indices[2] - color_change_indices[1])
    #
    # # Create a LineCollection from the segments
    # lc = LineCollection(segments, colors=colors, linewidth=2)
    #
    # # Create a plot
    # fig, ax = plt.subplots()
    # ax.add_collection(lc)
    #
    # # Set limits to fit the data
    # ax.set_xlim(x.min() - 0.5, x.max() + 0.5)
    # ax.set_ylim(y.min() - 0.5, y.max() + 0.5)
    #
    # plt.show()
    print(np.rad2deg(np.arctan(100/40000)))