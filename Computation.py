"""
File: Computation
Author: antoi
Date: 03/06/2024
Description: 
"""

import numpy as np
import Scenario as scn
import Swerling as swr
from Swerling import Swerling as swr
from scipy.special import comb

class Computation:

    def __init__(self, scenario):
        self.__scenario = scenario

    @property
    def scenario(self):
        return self.__scenario

    @scenario.setter
    def scenario(self, new_scenario):
        self.__scenario = new_scenario

    def swerling_computation(self, pfa, snr):
        swerling = swr.Swerling()
        if self.scenario.swelring_model in [1, 2]:
            return swr.sweling_I_II(pfa, snr)
        elif self.scenario.swelring_model in [3, 4]:
            return swr.sweling_III_IV(pfa, snr)
        elif self.scenario.swelring_model == 5:
            return swr.sweling_V(pfa, snr)
        else:
            return "Model not implemented"

    # def target_S_computation(self):
    #     P = 10 * np.log10(self.scenario.power)
    #     G_antenna = self.scenario.antenna_gain
    #     L = self.scenario.path_loss
    #     G_lambda = 20 * np.log10(self.scenario.wavelength)
    #     G_target_rcs = 10 * np.log10(self.scenario.target_rcs)
    #     G_pc = 10 * np.log10(self.scenario.duty_cycle)
    #     L_range = 40 * np.log10(self.scenario.target_range)
    #     L_coef = 30 * np;log10(4 * np.pi)
    #     self.target_S = P + G_antenna + G_lambda + G_target_rcs + G_pc - L - L_range - L_coef
    #     return self.target_S

    def S_computation(self, rcs, range):
        P = 10 * np.log10(self.scenario.power)
        G_antenna = self.scenario.antenna_gain
        L = self.scenario.path_loss
        G_lambda = 20 * np.log10(self.scenario.wavelength)
        G_clutter_rcs = 10 * np.log10(rcs)
        G_pc = 10 * np.log10(self.scenario.duty_cycle)
        L_range = 40 * np.log10(range)
        L_coef = 30 * np;log10(4 * np.pi)
        S = P + G_antenna + G_lambda + G_clutter_rcs + G_pc - L - L_range - L_coef
        return S

    def snrc_computation(self):
        noise = self.scenario.noise
        clutter_raw_S = 10 ** (self.clutter_S / 10)
        target_raw_S = 10 ** (self.target_S / 10)
        snrc = 10 * np.log10(target_raw_S / (clutter_raw_S + noise))
        return snrc

    def global_pd_computation(self, nb, kb, burst_pd):
        global_pd = 0.0
        for k in range(kb, nb + 1):
            binomial_coefficient = comb(nb, k)
            term = binomial_coefficient * (burst_pd ** k) * ((1 - burst_pd) ** (nb - k))
            global_pd += term
        return global_pd

    def run(self):
        target_rcs = self.scenario.target_rcs
        target_range = self.scenario.target_range
        s_target = self.S_computation(target_rcs, target_rcs)

        clutter_rcs = self.scenario.clutter_rcs
        clutter_range = self.scenario.clutter_range
        s_clutter = self.clutter_S_computation(clutter_rcs, clutter_range)

        snrc = self.snrc_computation()
        pfa = self.scenario.pfa

        burst_pd = self.swerling_computation(pfa, snrc)
        nb = self.scenario.Nb
        kb = self.scenario.Kb

        global_pd = self.global_pd_computation(nb, kb, burst_pd)
        print(f'Global pd: {global_pd}')
