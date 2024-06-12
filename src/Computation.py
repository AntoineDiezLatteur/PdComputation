"""
File: Computation
Author: antoi
Date: 03/06/2024
Description: 
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
        c = self.scenario.celerity
        h = self.scenario.radar_height
        theta_az = self.scenario.azimuth_angle
        tau = self.scenario.tau

        a1 = 0.5 * range * np.tan(np.deg2rad(theta_az/2))
        a2 = (c * tau) / (np.cos(np.arcsin(h / range)))
        a3 = np.sqrt(np.pi / (2* np.log(2)))

        return a1 * a2 * a3

    def swerling_computation(self, pfa, snr):
        swerling_instance = swr.Swerling()
        if self.scenario.swelring_model in [1, 2]:
            burst_pd = swerling_instance.sweling_I_II(pfa, snr)
            return burst_pd
        elif self.scenario.swelring_model in [3, 4]:
            burst_pd = swerling_instance.sweling_III_IV(pfa, snr)
            return burst_pd
        elif self.scenario.swelring_model == 5:
            burst_pd = swerling_instance.sweling_V(pfa, snr)
            return burst_pd
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

    def S_computation(self, rcs, range, G_doppler):
        if rcs == 0 :
            return 0
        P = 10 * np.log10(self.scenario.power)
        G_antenna = self.scenario.antenna_gain
        L = self.scenario.loss
        G_lambda = 20 * np.log10(self.scenario.wavelength)
        G_clutter_rcs = 10 * np.log10(rcs)
        G_pc = 10 * np.log10(self.scenario.duty_cycle)
        G_pc = 0
        L_range = 40 * np.log10(range)
        L_4pi3 = 30 * np.log10(4 * np.pi)
        S = P + G_antenna + G_doppler + G_lambda + G_clutter_rcs + G_pc - L - L_range - L_4pi3
        return S

    def snrc_computation(self, s_clutter : float, s_target : float) -> float:
        noise = self.scenario.noise
        clutter_raw_S = 10 ** (s_clutter / 10)
        target_raw_S = 10 ** (s_target / 10)
        snrc = 10 * np.log10(target_raw_S / (clutter_raw_S + noise))
        return snrc

    def global_pd_computation(self, nb, kb, burst_pd):
        global_pd = 0.0
        for k in range(int(kb), int(nb) + 1):
            binomial_coefficient = comb(nb, k)
            term = binomial_coefficient * (burst_pd ** k) * ((1 - burst_pd) ** (nb - k))
            global_pd += term
        return global_pd

    def run(self):
        target_rcs = self.scenario.target_rcs
        target_range = self.scenario.target_range
        target_doppler_gain = self.scenario.doppler_gain_target
        s_target = self.S_computation(target_rcs, target_range, target_doppler_gain)

        clutter_range = self.scenario.clutter_range
        clutter_rcs = self.scenario.clutter_rcs
        ds = self.ds_computation(clutter_range)
        reflectivity = self.scenario.clutter_reflectivity
        print(f'Clutter range: {clutter_range}')
        print(f'reflectivity: {reflectivity}')
        print(f'reflectivity in db: {10 * np.log10(reflectivity)}')
        print(f'ds: {ds}')
        clutter_rcs = reflectivity * ds
        print(f'Clutter rcs: {clutter_rcs}')
        print(f'clutter rcs in db: {10 * np.log10(clutter_rcs)}')
        clutter_doppler_gain = self.scenario.doppler_gain_clutter
        s_clutter = self.S_computation(clutter_rcs, clutter_range, clutter_doppler_gain)

        snrc = self.snrc_computation(s_clutter, s_target)
        pfa = self.scenario.pfa

        burst_pd = self.swerling_computation(pfa, snrc)
        print(f'Burst pd: {burst_pd}')
        nb = self.scenario.Nb
        kb = self.scenario.Kb

        global_pd = self.global_pd_computation(nb, kb, burst_pd)
        print(f'Global pd: {global_pd}')
        return global_pd

if __name__ == '__main__':
    scenario = scn.Scenario()
    # scenario.scenario_generator(file_name='scenario.json')
    scenario.load_scenario(scenario_file='default_scenario.json')
    computation = Computation(scenario)

    target_rcs = computation.scenario.target_rcs
    target_range = computation.scenario.target_range
    target_doppler_gain = computation.scenario.doppler_gain_target
    s_target = computation.S_computation(target_rcs, target_range, target_doppler_gain)
    print(f'Target rcs: {target_rcs}')
    print(f'Target range: {target_range}')
    print(f'Target S: {s_target}')


    clutter_rcs = computation.scenario.clutter_rcs
    clutter_range = computation.scenario.clutter_range
    clutter_doppler_gain = computation.scenario.doppler_gain_clutter
    s_clutter = computation.S_computation(clutter_rcs, clutter_range, clutter_doppler_gain)
    print(f'Clutter rcs: {clutter_rcs}')
    print(f'Clutter range: {clutter_range}')
    print(f'Clutter S: {s_clutter}')

    snrc = computation.snrc_computation(s_clutter, s_target)
    pfa = computation.scenario.pfa
    noise = computation.scenario.noise
    print(f'Noise: {10 * np.log10(noise)}')
    print(f'SNRC: {snrc}')
    print(f'PFA: {pfa}')

    burst_pd = computation.swerling_computation(pfa, snrc)
    nb = computation.scenario.Nb
    kb = computation.scenario.Kb
    print(f'Burst pd: {burst_pd}')
    print(f'Nb: {nb}')
    print(f'Kb: {kb}')

    global_pd = computation.global_pd_computation(nb, kb, burst_pd)
    print(f'Global pd: {global_pd}')

