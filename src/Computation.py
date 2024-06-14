"""
File: Computation
Author: antoi
Date: 03/06/2024
Description: Manage the computations
"""

import numpy as np
import src.Scenario as scn
import src.Swerling as swr
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

    def ds_computation(self, range):
        c = self.scenario.config_parameters['celerity']
        h = self.scenario.scenario_parameters['radar_height']
        theta_az = self.scenario.scenario_parameters['azimuth_angle']
        tau = self.scenario.config_parameters['tau']
        if h/range > 1 or h/range < -1:
            return 0
        else:
            a1 = 0.5 * range * np.tan(np.deg2rad(theta_az/2))
            a2 = (c * tau) / (np.cos(np.arcsin(h / range)))
            a3 = np.sqrt(np.pi / (2* np.log(2)))

        return a1 * a2 * a3

    def swerling_computation(self, pfa, snr):
        swerling_instance = swr.Swerling()
        if self.scenario.scenario_parameters['swelring_model'] in [1, 2]:
            burst_pd = swerling_instance.sweling_I_II(pfa, snr)
            return burst_pd
        elif self.scenario.scenario_parameters['swelring_model'] in [3, 4]:
            burst_pd = swerling_instance.sweling_III_IV(pfa, snr)
            return burst_pd
        elif self.scenario.scenario_parameters['swelring_model'] == 5:
            burst_pd = swerling_instance.sweling_V(pfa, snr)
            return burst_pd
        else:
            return "Model not implemented"

    def S_computation(self, rcs, range, G_doppler):
        if rcs == 0 :
            return 0
        P = 10 * np.log10(self.scenario.config_parameters['power'])
        G_antenna = self.scenario.config_parameters['antenna_gain']
        L = self.scenario.config_parameters['loss']
        G_lambda = 20 * np.log10(self.scenario.config_parameters['wavelength'])
        G_clutter_rcs = 10 * np.log10(rcs)
        G_pc = 0
        L_range = 40 * np.log10(range)
        L_4pi3 = 30 * np.log10(4 * np.pi)
        S = P + G_antenna + G_doppler + G_lambda + G_clutter_rcs + G_pc - L - L_range - L_4pi3
        return S

    def snrc_computation(self, s_clutter : float, s_target : float) -> float:
        noise = self.scenario.config_parameters['noise']
        target_raw_S = 10 ** (s_target / 10)
        if s_clutter == 0:
            snrc = target_raw_S / noise
            return snrc
        else:
            clutter_raw_S = 10 ** (s_clutter / 10)
            snrc = target_raw_S / (clutter_raw_S + noise)
        return snrc

    def global_pd_computation(self, nb, kb, burst_pd):
        global_pd = 0.0
        for k in range(int(kb), int(nb) + 1):
            binomial_coefficient = comb(nb, k)
            term = binomial_coefficient * (burst_pd ** k) * ((1 - burst_pd) ** (nb - k))
            global_pd += term
        return global_pd

    def pd_analysis(self):
        x = np.linspace(10, 100000, 100)
        y = []
        z = []
        w = []

        for i in x:

            target_range = i

            target_rcs = self.scenario.scenario_parameters['target_rcs']
            target_doppler_gain = self.scenario.config_parameters['doppler_gain_target']

            clutter_range = i
            ds = self.ds_computation(clutter_range)
            reflectivity = self.scenario.scenario_parameters['clutter_reflectivity']
            clutter_rcs = reflectivity * ds

            clutter_doppler_gain = self.scenario.config_parameters['doppler_gain_clutter']
            s_clutter = self.S_computation(clutter_rcs, clutter_range, clutter_doppler_gain)
            side_lobe_loss = self.scenario.scenario_parameters['side_lobe_loss']
            s_clutter_side_lobe = s_clutter - side_lobe_loss

            pfa = self.scenario.scenario_parameters['pfa']
            nb = self.scenario.scenario_parameters['Nb']
            kb = self.scenario.scenario_parameters['Kb']

            s_target = self.S_computation(target_rcs, target_range, target_doppler_gain)
            snrc = self.snrc_computation(s_clutter, s_target)
            snr = self.snrc_computation(0, s_target)
            snrc_side_lobe = self.snrc_computation(s_clutter_side_lobe, s_target)

            burst_pd = self.swerling_computation(pfa, snrc)
            burst_pd_wo_clutter = self.swerling_computation(pfa, snr)
            burst_pd_side_lobe = self.swerling_computation(pfa, snrc_side_lobe)

            global_pd = self.global_pd_computation(nb, kb, burst_pd)
            global_pd_wo_clutter = self.global_pd_computation(nb, kb, burst_pd_wo_clutter)
            global_pd_side_lobe = self.global_pd_computation(nb, kb, burst_pd_side_lobe)

            y.append(global_pd)
            z.append(global_pd_wo_clutter)
            w.append(global_pd_side_lobe)

        return x, y, z, w

    def snr_analysis(self):
        x = np.linspace(10, 100000, 100)
        y = []
        z = []
        w = []

        for i in x:

            target_range = i
            target_rcs = self.scenario.scenario_parameters['target_rcs']
            target_doppler_gain = self.scenario.config_parameters['doppler_gain_target']

            clutter_range = i
            ds = self.ds_computation(clutter_range)
            reflectivity = self.scenario.scenario_parameters['clutter_reflectivity']
            clutter_rcs = reflectivity * ds

            clutter_doppler_gain = self.scenario.config_parameters['doppler_gain_clutter']
            s_clutter = self.S_computation(clutter_rcs, clutter_range, clutter_doppler_gain)
            side_lobe_loss = self.scenario.scenario_parameters['side_lobe_loss']
            s_clutter_side_lobe = s_clutter - side_lobe_loss

            pfa = self.scenario.scenario_parameters['pfa']
            nb = self.scenario.scenario_parameters['Nb']
            kb = self.scenario.scenario_parameters['Kb']

            s_target = self.S_computation(target_rcs, target_range, target_doppler_gain)

            snrc = self.snrc_computation(s_clutter, s_target)
            snr = self.snrc_computation(0, s_target)
            snrc_side_lobe = self.snrc_computation(s_clutter_side_lobe, s_target)

            y.append(10 * np.log10(snrc))
            z.append(10 * np.log10(snrc_side_lobe))
            w.append(10 * np.log10(snr))
        return x, y, z, w