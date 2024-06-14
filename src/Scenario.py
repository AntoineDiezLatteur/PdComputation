"""
File: Scenario
Author: antoi
Date: 03/06/2024
Description: 
"""

import json
from src.loader import DATA_PATH
from src.loader import CONFIG_PATH
import os
import rx
from rx.subject import Subject

class Scenario:

    def __init__(self):
        self._subject = Subject()

        self.__scenario_parameters = {
            'swelring_model': None,
            'target_rcs': None,
            'Nb': None,
            'Kb': None,
            'azimuth_angle': None,
            'radar_height': None,
            'clutter_reflectivity': None,
            'side_lobe_loss': None,
            'pfa': None,
        }

        self.__config_parameters = {
            'celerity': 3e8,
            'frequency': None,
            'wavelength': None,
            'power': None,
            'antenna_gain': None,
            'doppler_gain_target': None,
            'doppler_gain_clutter': None,
            'loss': None,
            'boltzmann_ct': 1.38e-23,
            'system_temperature': None,
            'noise_bandwight': None,
            'noise': None,
            'desired_pd': None,
            'tau': None,
        }

    @property
    def config_parameters(self):
        return self.__config_parameters

    @config_parameters.setter
    def config_parameters(self, new_config_parameters):
        self.__config_parameters = new_config_parameters

    @property
    def scenario_parameters(self):
        return self.__scenario_parameters

    @scenario_parameters.setter
    def scenario_parameters(self, new_scenario):
        self.__scenario_parameters = new_scenario
        self._subject.on_next(new_scenario)

    def subscribe(self, observer):
        return self._subject.subscribe(observer)

    def __str__(self):
        return f'Scenario: {self.scenario_parameters}\nConfig: {self.config_parameters}'

    def load_scenario(self, scenario_file='scenario.json', total_path=False):
        data_path = f'{DATA_PATH}/{scenario_file}' if not total_path else scenario_file
        with open(data_path, 'r') as file:
            scenario = json.load(file)
        self.scenario_parameters = scenario

    def config(self, config_file='config.json'):
        config_path = f'{CONFIG_PATH}/{config_file}'
        with open(config_path, 'r') as file:
            scenario = json.load(file)

        self.config_parameters = scenario
        c = self.config_parameters['celerity']
        f = self.config_parameters['frequency']
        self.config_parameters['wavelength'] = c/f
        t = self.config_parameters['system_temperature']
        nb = self.config_parameters['noise_bandwight']
        cb = self.config_parameters['boltzmann_ct']
        self.config_parameters['noise'] = cb * t * nb