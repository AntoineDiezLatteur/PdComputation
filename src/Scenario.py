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
from dataclasses import dataclass
from typing import Optional
import rx
from rx.subject import Subject

class Scenario:

    def __init__(self):
        self._subject = Subject()
        self._scenario = {
            'swelring_model': None,
            'target_rcs': None,
            'Nb': None,
            'Kb': None,
            'azimuth_angle': None,
            'radar_height': None,
            'clutter_reflectivity': None,
        }

        self._config_parameters = {
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
            'pfa': None,
            'desired_pd': None,
            'tau': None,
        }

    @property
    def config_parameters(self):
        return self._config_parameters

    @config_parameters.setter
    def config_parameters(self, new_config_parameters):
        self._config_parameters = new_config_parameters

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, new_scenario):
        self._scenario = new_scenario
        self._subject.on_next(new_scenario)


    def subscribe(self, observer):
        return self._subject.subscribe(observer)


    def __str__(self):
        return f'Scenario: {self._scenario}'

    def main(self):
        pass

    def load_scenario(self, scenario_file='scenario.json', total_path=False):
        print('Loading scenario')
        data_path = f'{DATA_PATH}/{scenario_file}' if not total_path else scenario_file
        with open(data_path, 'r') as file:
            scenario = json.load(file)
        self.scenario = scenario
        print(self)
        print('Scenario loaded')

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
        print(self.config_parameters)
        print('Config loaded')

    # # def generate_scenario(self):
    # def scenario_generator(self, file_name='scenario.json', scenario=None):
    #
    #     if scenario != None:
    #         self.default_scenario = scenario
    #
    #     # Write the scenario to a JSON file
    #     with open(os.path.join(DATA_PATH, file_name), 'w') as file:
    #         json.dump(self.default_scenario, file, indent=4)