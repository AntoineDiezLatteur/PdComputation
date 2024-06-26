"""
File: computation
Author: antoi
Date: 03/06/2024
Description: Manage global computations using the computation's libraries
"""

import numpy as np
import src.computation.Geometry as geo
import src.computation.Pd as pd
import src.computation.Power as pw
import src.computation.Swerling as swr
import src.Scenario
import matplotlib.pyplot as plt
from src import Terrain as trn

class Computation:

    def __init__(self, scenario, terrain):
        self.__scenario = scenario
        self.__terrain = terrain
        self._geometry = geo.Geometry()
        self._swerling = swr.Swerling()
        self._power = pw.Power()
        self._pd = pd.Pd()

    @property
    def scenario(self):
        return self.__scenario

    @scenario.setter
    def scenario(self, new_scenario):
        self.__scenario = new_scenario

    @property
    def terrain(self):
        return self.__terrain

    @terrain.setter
    def terrain(self, new_terrain):
        self.__terrain = new_terrain

    def ds_computation(self, range):
        c = self.scenario.config_parameters['celerity']
        h = self.scenario.scenario_parameters['radar_height']
        theta_az = self.scenario.scenario_parameters['azimuth_angle']
        tau = self.scenario.config_parameters['tau']
        elevation_angle = self.elevation_angle(range)
        grazing_angle = self.grazing_angle(range)
        return self._geometry.ds_computation(range, c, h, elevation_angle=elevation_angle, grazing_angle=grazing_angle, tau=tau)

    def r_horizon(self):
        z = self.scenario.scenario_parameters['target_height']
        h = self.scenario.scenario_parameters['radar_height']
        er = self.scenario.config_parameters['earth_radius']
        return self._geometry.r_horizon(z, h, er)

    def theta_horizon(self):
        h = self.scenario.scenario_parameters['radar_height']
        er = self.scenario.config_parameters['earth_radius']
        return self._geometry.theta_horizon(h, er)

    def is_visible(self, range, theta):
        theta_horizon = self.theta_horizon()
        r_horizon = self.r_horizon()
        z = self.scenario.scenario_parameters['target_height']
        return self._geometry.is_visible(range, theta, z, theta_horizon, r_horizon)

    def elevation_angle(self, range):
        h = self.scenario.scenario_parameters['radar_height']
        er = self.scenario.config_parameters['earth_radius']
        z = self.scenario.scenario_parameters['target_height']
        return self._geometry.elevation_angle_computation(range, h, er, z)

    def grazing_angle(self, range):
        h = self.scenario.scenario_parameters['radar_height']
        er = self.scenario.config_parameters['earth_radius']
        z = self.scenario.scenario_parameters['target_height']
        return self._geometry.grazing_angle_computation(range, h, er, z)

    def swerling_computation(self, pfa, snr):

        if self.scenario.scenario_parameters['swelring_model'] in [1, 2]:
            burst_pd = self._swerling.sweling_I_II(pfa, snr)
            return burst_pd
        elif self.scenario.scenario_parameters['swelring_model'] in [3, 4]:
            burst_pd = self._swerling.sweling_III_IV(pfa, snr)
            return burst_pd
        elif self.scenario.scenario_parameters['swelring_model'] == 5:
            # burst_pd = self._swerling.sweling_V(pfa, snr)
            # return burst_pd
            return "Model not working for now"
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
        return self._power.S_computation(rcs, range, G_doppler, P, G_antenna, L, G_lambda, G_clutter_rcs, G_pc, L_range, L_4pi3)

    def snrc_computation(self, s_clutter : float, s_target : float) -> float:
        noise = self.scenario.config_parameters['noise']
        return self._power.snrc_computation(s_clutter, s_target, noise)

    def global_pd_computation(self, nb, kb, burst_pd):
        return self._pd.global_pd_computation(nb, kb, burst_pd)

    def computation_loop(self, mutli_scan_mode=False, snr_mode=False):
        x = np.arange(self.scenario.range_min, self.scenario.range_max, self.scenario.step, dtype=float)
        print(x)
        print(len(x))
        y1 = self.elevation_angle(x)
        x2 = np.linspace(1000, 100000,100)
        print(x2)
        print(len(x2))
        y2 = self.elevation_angle(x2)

        y = []
        z = []
        w = []
        # print(self.theta_horizon())
        # print(self.r_horizon())


        for i in x:

            target_range = i

            target_rcs = self.scenario.scenario_parameters['target_rcs']
            target_doppler_gain = self.scenario.config_parameters['doppler_gain_target']

            clutter_range = i
            ds = self.ds_computation(clutter_range)
            reflectivity = self.scenario.scenario_parameters['clutter_reflectivity']

            range_idx = int((clutter_range - self.scenario.range_min) // self.scenario.step)
            reflectivity = self.terrain.reflectivity[range_idx]
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

            if mutli_scan_mode:
                n = 4
                k = 3
                global_pd = self.global_pd_computation(n, k, global_pd)
                global_pd_wo_clutter = self.global_pd_computation(n, k, global_pd_wo_clutter)
                global_pd_side_lobe = self.global_pd_computation(n, k, global_pd_side_lobe)

            theta = self.elevation_angle(target_range)
            # if target_range >= self.r_horizon():
                # print(theta)

            if not snr_mode :
                if not self.is_visible(target_range, theta):
                    global_pd = 0
                    global_pd_wo_clutter = 0
                    global_pd_side_lobe = 0

                y.append(global_pd)
                z.append(global_pd_wo_clutter)
                w.append(global_pd_side_lobe)
            else :
                if not self.is_visible(target_range, theta):
                    y.append(0)
                    z.append(0)
                    w.append(0)
                else:
                    y.append(10 * np.log10(snrc))
                    z.append(10 * np.log10(snr))
                    w.append(10 * np.log10(snrc_side_lobe))
        return x, y, z, w, x2, y2, y1

if __name__ == "__main__":
    scenario = src.Scenario.Scenario()
    scenario.load_scenario()
    scenario.config()
    terrain = trn.Terrain()
    terrain.load_terrain('terrain.json')
    computation = Computation(scenario, terrain)

    x, y, z, w, x2, y2, y1 = computation.computation_loop(mutli_scan_mode=False, snr_mode=False)
    print(len(x), len(y), len(z), len(w), len(x2), len(y2), len(y1))
    print(computation.elevation_angle(46000))
    print(computation.elevation_angle(46000.))
    plt.subplot(121)
    plt.plot(x, y1)
    plt.plot(np.arange(1000, 101000, 1000), [computation.elevation_angle(46000) for i in range(100)])
    plt.plot(np.arange(1000, 101000, 1000), [computation.elevation_angle(47000) for i in range(100)])
    plt.subplot(122)
    plt.plot(x2, y2)
    plt.plot(np.arange(1000, 101000, 1000), [computation.elevation_angle(46000) for i in range(100)])
    plt.plot(np.arange(1000, 101000, 1000), [computation.elevation_angle(47000) for i in range(100)])

    plt.show()