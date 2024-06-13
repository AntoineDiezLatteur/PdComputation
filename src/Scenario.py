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

class Scenario:

    def __init__(self):

        self.__target_range = None
        self.__swelring_model = None

        self.__clutter_rcs = None
        self.__clutter_range = None
        # self.__clutter_reflectivity = 1
        # self.__clutter_ds = 200
        # self.__clutter_rcs = self.__clutter_reflectivity * self.__clutter_ds

        # self.__wave_definition = None
        self.__frequency = None
        self.__celerity = 3e8
        self.__wavelength = None

        self.__power = None
        self.__antenna_gain = None
        self.__doppler_gain_target = None
        self.__doppler_gain_clutter = None
        self.__loss = None

        # self.__noise_definition = None
        self.__boltzmann_ct = 1.38e-23
        self.__system_temperature = None
        self.__noise_bandwight = None
        self.__noise = None

        self.__dwell_nb_burst = None
        self.__dwell_total_duration = None
        self.__duty_cycle =None
        self.Nb = None
        self.Kb = None

        self.tau = None
        self.azimuth_angle = None
        self.radar_height = None
        self.clutter_reflectivity = None

        self.pfa = 1e-6
        self.desired_pd = 0.9

        self.default_scenario = {
            "target_rcs": 2.0,
            "target_range": 10000,
            "swelring_model": 1,
            "clutter_rcs": 33.0,
            "clutter_range": 10000,
            "celerity": 3e8,  # Speed of light in m/s
            # "wave_definition": "frequency",
            "frequency": 3.1e9,  # 1 GHz
            "wavelength": None,  # This will be calculated if wave_definition is frequency
            "power": 17920,  # in watts
            "antenna_gain": 64,  # in dBi
            "doppler_gain_target": 11.8,  # in dBi
            "doppler_gain_clutter": -40,  # in dBi
            "loss": 9.7,  # Loss factor
            "boltzmann_ct": 1.38e-23,  # Boltzmann constant
            # "noise_definition": "temperature",
            "system_temperature": 1064,  # in Kelvin
            "noise_bandwight": 17575,  # 1 MHz
            "noise": None,  # This will be calculated if noise_definition is temperature
            "dwell_nb_burst": 4,
            "dwell_total_duration": 1,  # in seconds
            "duty_cycle": 0.1,
            "Nb": 4,
            "Kb": 2,
            "pfa": 1e-6,
            "desired_pd": 0.9,
            "tau": 5e-5,
            "azimuth_angle": 3,
            "radar_height": 20,
            "clutter_reflectivity": 1e-2
        }

        self.parameter_list = [
            "target_rcs",
            "target_range",
            "swelring_model",
            "clutter_rcs",
            "clutter_range",
            "celerity",
            "frequency",
            "wavelength",
            "power",
            "antenna_gain",
            "doppler_gain_target",
            "doppler_gain_clutter",
            "loss",
            "boltzmann_ct",
            "system_temperature",
            "noise_bandwight",
            "noise",
            "dwell_nb_burst",
            "dwell_total_duration",
            "duty_cycle",
            "Nb",
            "Kb",
            "pfa",
            "desired_pd",
            "tau",
            "azimuth_angle",
            "radar_height",
            "clutter_reflectivity"
        ]

        # Calculating derived values
        # if self.default_scenario['wave_definition'] == 'frequency':
        #     self.default_scenario['wavelength'] = self.default_scenario['celerity'] / self.default_scenario['frequency']
        # elif self.default_scenario['wave_definition'] == 'wavelength':
        #     self.default_scenario['frequency'] = self.default_scenario['celerity'] / self.default_scenario['wavelength']
        #
        # if self.default_scenario['noise_definition'] == 'temperature':
        #     self.default_scenario['noise'] = self.default_scenario['boltzmann_ct'] * self.default_scenario[
        #         'system_temperature'] * self.default_scenario['noise_bandwight']

    def __str__(self):
        return f'Target RCS: {self.target_rcs} \nTarget range: {self.target_range} \nSWELRING model: {self.swelring_model} \nClutter RCS: {self.clutter_rcs} \nClutter range: {self.clutter_range} \nFrequency: {self.frequency} \nWavelength: {self.wavelength} \nPower: {self.power} \nAntenna gain: {self.antenna_gain} \nLoss: {self.loss} \nBoltzmann constant: {self.boltzmann_ct} \nSystem temperature: {self.system_temperature} \nNoise bandwight: {self.noise_bandwight} \nNoise: {self.noise} \nDwell number of burst: {self.dwell_nb_burst} \nDwell total duration: {self.dwell_total_duration} \nDuty cycle: {self.duty_cycle} \nNb: {self.Nb} \nKb: {self.Kb} \nPfa: {self.pfa} \nDesired Pd: {self.desired_pd}'

    @property
    def target_rcs(self):
        return self.__target_rcs

    @target_rcs.setter
    def target_rcs(self, new_target_rcs):
        self.__target_rcs = new_target_rcs

    @property
    def target_range(self):
        return self.__target_range

    @target_range.setter
    def target_range(self, new_target_range):
        self.__target_range = new_target_range


    @property
    def swelring_model(self):
        return self.__swelring_model

    @swelring_model.setter
    def swelring_model(self, new_swelring_model):
        if new_swelring_model not in [1, 2, 3, 4]:
            raise ValueError('The Swelring model must be 1, 2 or 3')
        else :
            self.__swelring_model = new_swelring_model

    @property
    def clutter_rcs(self):
        return self.__clutter_rcs

    @clutter_rcs.setter
    def clutter_rcs(self, new_clutter_rcs):
        self.__clutter_rcs = new_clutter_rcs

    @property
    def clutter_range(self):
        return self.__clutter_range

    @clutter_range.setter
    def clutter_range(self, new_clutter_range):
        self.__clutter_range = new_clutter_range

    # @property
    # def clutter_reflectivity(self):
    #     return self.__clutter_reflectivity
    #
    # @clutter_reflectivity.setter
    # def clutter_reflectivity(self, new_clutter_reflectivity):
    #     self.__clutter_reflectivity = new_clutter_reflectivity
    #
    # @property
    # def clutter_ds(self):
    #     return self.__clutter_ds
    #
    # @clutter_ds.setter
    # def clutter_ds(self, new_clutter_ds):
    #     self.__clutter_ds = new_clutter_ds

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, new_frequency):
        self.__frequency = new_frequency
        self.__wavelength = self.__celerity/self.__frequency
        print(f'Wavelength updated to {self.__wavelength} m')

    @property
    def celerity(self):
        return self.__celerity

    @property
    def wavelength(self):
        return self.__wavelength

    @wavelength.setter
    def wavelength(self, new_wavelength):
        self.__wavelength = new_wavelength
        freq = self.__celerity/self.__wavelength
        self.__frequency = freq
        print(f'Frequency updated to {self.__frequency} Hz')

    @property
    def power(self):
        return self.__power

    @power.setter
    def power(self, new_power):
        self.__power = new_power

    @property
    def antenna_gain(self):
        return self.__antenna_gain

    @antenna_gain.setter
    def antenna_gain(self, new_antenna_gain):
        self.__antenna_gain = new_antenna_gain

    @property
    def loss(self):
        return self.__loss

    @loss.setter
    def loss(self, new_loss):
        self.__loss = new_loss

    @property
    def boltzmann_ct(self):
        return self.__boltzmann_ct

    @property
    def system_temperature(self):
        return self.__system_temperature

    @system_temperature.setter
    def system_temperature(self, new_system_temperature):
        self.__system_temperature = new_system_temperature
        try :
            noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
            self.__noise = noise
        except TypeError:
            pass
        # if self.noise_bandwight != None:
        #     self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
        print(f'Noise updated to {self.__noise} W')


    @property
    def noise_bandwight(self):
        return self.__noise_bandwight

    @noise_bandwight.setter
    def noise_bandwight(self, new_noise_bandwight):
        self.__noise_bandwight = new_noise_bandwight
        try :
            noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
            self.__noise = noise
        except TypeError:
            pass
        # if self.system_temperature != None:
        #     self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
        print(f'Noise updated to {self.__noise} W')

    @property
    def noise(self):
        return self.__noise

    @noise.setter
    def noise(self, new_noise):
        self.__noise = new_noise
        print('Noise updated independently of the system temperature and noise bandwight')

    @property
    def dwell_nb_burst(self):
        return self.__dwell_nb_burst

    @dwell_nb_burst.setter
    def dwell_nb_burst(self, new_dwell_nb_burst):
        self.__dwell_nb_burst = new_dwell_nb_burst

    @property
    def dwell_total_duration(self):
        return self.__dwell_total_duration

    @dwell_total_duration.setter
    def dwell_total_duration(self, new_dwell_total_duration):
        self.__dwell_total_duration = new_dwell_total_duration

    @property
    def duty_cycle(self):
        return self.__duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, new_duty_cycle):
        self.__duty_cycle = new_duty_cycle

    @property
    def Nb(self):
        return self.__Nb

    @Nb.setter
    def Nb(self, new_Nb):
        self.__Nb = new_Nb

    @property
    def Kb(self):
        return self.__Kb

    @Kb.setter
    def Kb(self, new_Kb):
        self.__Kb = new_Kb

    @property
    def pfa(self):
        return self.__pfa

    @pfa.setter
    def pfa(self, new_pfa):
        self.__pfa = new_pfa

    @property
    def desired_pd(self):
        return self.__desired_pd

    @desired_pd.setter
    def desired_pd(self, new_desired_pd):
        self.__desired_pd = new_desired_pd

    # @property
    # def wave_definition(self):
    #     return self.__wave_definition
    #
    # @wave_definition.setter
    # def wave_definition(self, new_wave_definition):
    #     self.__wave_definition = new_wave_definition
    #
    # @property
    # def noise_definition(self):
    #     return self.__noise_definition
    #
    # @noise_definition.setter
    # def noise_definition(self, new_noise_definition):
    #     self.__noise_definition = new_noise_definition

    @property
    def doppler_gain_target(self):
        return self.__doppler_gain_target

    @doppler_gain_target.setter
    def doppler_gain_target(self, new_doppler_gain_target):
        self.__doppler_gain_target = new_doppler_gain_target

    @property
    def doppler_gain_clutter(self):
        return self.__doppler_gain_clutter

    @doppler_gain_clutter.setter
    def doppler_gain_clutter(self, new_doppler_gain_clutter):
        self.__doppler_gain_clutter = new_doppler_gain_clutter

    def main(self):
        pass

    def load_scenario(self, scenario_file='scenario.json', total_path=False):
        data_path = f'{DATA_PATH}/{scenario_file}' if not total_path else scenario_file
        print(data_path)
        with open(data_path, 'r') as file:
            scenario = json.load(file)

        self.__target_rcs = scenario['target_rcs']
        self.__target_range = scenario['target_range']
        self.__swelring_model = scenario['swelring_model']

        self.__clutter_rcs = scenario['clutter_rcs']
        self.__clutter_range = scenario['clutter_range']
        # self.__clutter_reflectivity = scenario['clutter_reflectivity']
        # self.__clutter_ds = scenario['clutter_ds']

        self.__celerity = scenario['celerity']
        self.__wave_definition = scenario['wave_definition']
        self.__frequency = scenario['frequency']
        self.__wavelength = self.__celerity/self.__frequency
        # elif self.__wave_definition == 'wavelength':
        #     self.__wavelength = scenario['wavelength']
        #     self.__frequency = self.__celerity/self.__wavelength
        # else:
        #     print('Wave definition not recognized')

        self.__power = scenario['power']
        self.__antenna_gain = scenario['antenna_gain']
        self.__doppler_gain_target = scenario['doppler_gain_target']
        self.__doppler_gain_clutter = scenario['doppler_gain_clutter']
        self.__loss = scenario['loss']

        self.__boltzmann_ct = scenario['boltzmann_ct']
        self;__noise_definition = scenario['noise_definition']
        # if scenario['noise_definition'] == 'temperature':
        self.__system_temperature = scenario['system_temperature']
        self.__noise_bandwight = scenario['noise_bandwight']
        self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
        # elif self.__noise_definition == 'independant':
        #     self.__noise = scenario['noise']
        #     self.__system_temperature = None
        #     self.__noise_bandwight = None
        # else:
        #     print('Noise definition not recognized')

        self.__dwell_nb_burst = scenario['dwell_nb_burst']
        self.__dwell_total_duration = scenario['dwell_total_duration']
        self.__duty_cycle = scenario['duty_cycle']
        self.Nb = scenario['Nb']
        self.Kb = scenario['Kb']

        self.pfa = scenario['pfa']
        self.desired_pd = scenario['desired_pd']

        self.tau = scenario['tau']
        self.azimuth_angle = scenario['azimuth_angle']
        self.radar_height = scenario['radar_height']
        self.clutter_reflectivity = scenario['clutter_reflectivity']
        print('Scenario loaded')

    def config(self, config_file='config.json'):
        config_path = f'{CONFIG_PATH}/{config_file}'
        with open(config_path, 'r') as file:
            scenario = json.load(file)

        self.__target_rcs = scenario['target_rcs']
        self.__swelring_model = scenario['swelring_model']
        self.__clutter_rcs = scenario['clutter_rcs']
        self.Nb = scenario['Nb']
        self.Kb = scenario['Kb']
        self.azimuth_angle = scenario['azimuth_angle']
        self.radar_height = scenario['radar_height']
        self.clutter_reflectivity = scenario['clutter_reflectivity']


        self.__target_range = scenario['target_range']
        self.__clutter_range = scenario['clutter_range']
        # self.__clutter_reflectivity = scenario['clutter_reflectivity']
        # self.__clutter_ds = scenario['clutter_ds']

        self.__celerity = scenario['celerity']
        self.__wave_definition = scenario['wave_definition']
        self.__frequency = scenario['frequency']
        self.__wavelength = self.__celerity/self.__frequency
        # elif self.__wave_definition == 'wavelength':
        #     self.__wavelength = scenario['wavelength']
        #     self.__frequency = self.__celerity/self.__wavelength
        # else:
        #     print('Wave definition not recognized')

        self.__power = scenario['power']
        self.__antenna_gain = scenario['antenna_gain']
        self.__doppler_gain_target = scenario['doppler_gain_target']
        self.__doppler_gain_clutter = scenario['doppler_gain_clutter']
        self.__loss = scenario['loss']

        self.__boltzmann_ct = scenario['boltzmann_ct']
        self;__noise_definition = scenario['noise_definition']
        # if scenario['noise_definition'] == 'temperature':
        self.__system_temperature = scenario['system_temperature']
        self.__noise_bandwight = scenario['noise_bandwight']
        self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
        # elif self.__noise_definition == 'independant':
        #     self.__noise = scenario['noise']
        #     self.__system_temperature = None
        #     self.__noise_bandwight = None
        # else:
        #     print('Noise definition not recognized')

        self.__dwell_nb_burst = scenario['dwell_nb_burst']
        self.__dwell_total_duration = scenario['dwell_total_duration']
        self.__duty_cycle = scenario['duty_cycle']


        self.pfa = scenario['pfa']
        self.desired_pd = scenario['desired_pd']

        self.tau = scenario['tau']

        print('Scenario loaded')

    # def generate_scenario(self):
    def scenario_generator(self, file_name='scenario.json', scenario=None):

        if scenario != None:
            self.default_scenario = scenario
            # self.default_scenario['wave_definition'] = 'frequency'
            # self.default_scenario['noise_definition'] = 'temperature'

        # Write the scenario to a JSON file
        with open(os.path.join(DATA_PATH, file_name), 'w') as file:
            json.dump(self.default_scenario, file, indent=4)


# if __name__ == '__main__':
#     scenario = Scenario()
#     print(type(scenario.target_rcs))
#     scenario.scenario_generator()
#     scenario.load_scenario('scenario.json')
#     print(scenario.target_rcs)

# @dataclass
# class Scenario:
#     target_rcs: float
#     target_range: float
#     swelring_model: int
#     clutter_rcs: float
#     clutter_range: float
#     frequency: float
#     power: float
#     antenna_gain: float
#     doppler_gain_target: float
#     doppler_gain_clutter: float
#     loss: float
#     boltzmann_ct: float = 1.38e-23
#     system_temperature: float
#     noise_bandwight: float
#     noise: float
#     dwell_nb_burst: int
#     dwell_total_duration: float
#     duty_cycle: float
#     Nb: int
#     Kb: int
#     pfa: float
#     desired_pd: float
#     wavelength: Optional[float] = None
#     celerity: float = 3e8
#     noise: Optional[float] = None
#     # wave_definition: str = 'frequency'
#     # noise_definition: str = 'temperature'
#
#     def __post_init__(self):
#         if self.wavelength is None:
#             self.wavelength = self.celerity / self.frequency
#         if self.noise is None:
#             self.noise = self.boltzmann_ct * self.system_temperature * self.noise_bandwight
#         if self.swelring_model not in [1, 2, 3, 4]:
#             raise ValueError('The Swelring model must be 1, 2 or 3')
#         if self.desired_pd > 1 or self.desired_pd < 0:
#             raise ValueError('The desired probability of detection must be between 0 and 1')
#         if self.pfa > 1 or self.pfa < 0:
#             raise ValueError('The probability of false alarm must be between 0 and 1')
#         if self.duty_cycle > 1 or self.duty_cycle < 0:
#             raise ValueError('The duty cycle must be between 0 and 1')
#         if self.dwell_nb_burst < 0:
#             raise ValueError('The number of bursts per dwell must be positive')
#         if self.dwell_total_duration < 0:
#             raise ValueError('The total duration of the dwell must be positive')
#         if self.Nb < 0:
#             raise ValueError('The number of bursts must be positive')
#         if self.Kb < 0:
#             raise ValueError('The number of bursts must be positive')
#         if self.clutter_rcs < 0:
#             raise ValueError('The clutter RCS must be positive')
#         if self.clutter_range < 0:
#             raise ValueError('The clutter range must be positive')
#         if self.target_rcs < 0:
#             raise ValueError('The target RCS must be positive')
#         if self.target_range < 0:
#             raise ValueError('The target range must be positive')
#         if self.frequency < 0:
#             raise ValueError('The frequency must be positive')
#         if self.power < 0:
#             raise ValueError('The power must be positive')
#         if self.antenna_gain < 0:
#             raise ValueError('The antenna gain must be positive')
#         if self.doppler_gain_target < 0:
#             raise ValueError('The target Doppler gain must be positive')
#         if self.doppler_gain_clutter < 0:
#             raise ValueError('The clutter Doppler gain must be positive')
#         if self.loss < 0:
#             raise ValueError('The loss must be positive')
#         if self.boltzmann_ct < 0:
#             raise ValueError('The Boltzmann constant must be positive')
#         if self.system_temperature < 0:
#             raise ValueError('The system temperature must be positive')
#         if self.noise_bandwight < 0:
#             raise ValueError('The noise bandwidth must be positive')
#         if self.noise < 0:
#             raise ValueError('The noise must be positive')
#         print('Scenario loaded')
#         self._subject = Subject()
#
#     def subscribe(self, observer):
#         self._subject.subscribe(observer)
#
#     def __str__(self):
#         return f'Target RCS: {self.target_rcs} \nTarget range: {self.target_range} \nSWELRING model: {self.swelring_model} \nClutter RCS: {self.clutter_rcs} \nClutter range: {self.clutter_range} \nFrequency: {self.frequency} \nWavelength: {self.wavelength} \nPower: {self.power} \nAntenna gain: {self.antenna_gain} \nLoss: {self.loss} \nBoltzmann constant: {self.boltzmann_ct} \nSystem temperature: {self.system_temperature} \nNoise bandwight: {self.noise_bandwight} \nNoise: {self.noise} \nDwell number of burst: {self.dwell_nb_burst} \nDwell total duration: {self.dwell_total_duration} \nDuty cycle: {self.duty_cycle} \nNb: {self.Nb} \nKb: {self.Kb} \nPfa: {self.pfa} \nDesired Pd: {self.desired_pd}'
#
#
#     def load_scenario(self, scenario_file='scenario.json', total_path=False):
#         data_path = f'{DATA_PATH}/{scenario_file}' if not total_path else scenario_file
#         with open(data_path, 'r') as file:
#             scenario = json.load(file)
#
#         return Scenario(**scenario)
#
