"""
File: Scenario
Author: antoi
Date: 03/06/2024
Description: 
"""
import json

class Scenario:

    def __init__(self):
        self.__target_rcs = None
        self.__target_range = None
        self.__swelring_model = None

        self.__clutter_rcs = None
        self.__clutter_range = None
        # self.__clutter_reflectivity = 1
        # self.__clutter_ds = 200
        # self.__clutter_rcs = self.__clutter_reflectivity * self.__clutter_ds

        self.__wave_definition = None
        self.__frequency = None
        self.__celerity = 3e8
        self.__wavelength = self.__celerity/self.__frequency

        self.__power = None
        self.__antenna_gain = None
        self.__loss = None

        self.__noise_definition = None
        self.__boltzmann_ct = 1.380649e-23
        self.__system_temperature = None
        self.__noise_bandwight = None
        self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight

        self.__dwell_nb_burst = None
        self.__dwell_total_duration = None
        self.__duty_cycle =None
        self.Nb = None
        self.Kb = None

        self.pfa = 1e-6
        self.desired_pd = 0.9

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
        self.__wave_definition = 'frequency'
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
        self.__frequency = self.__celerity/self.__wavelength
        self.__wave_definition = 'wavelength'
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
        self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
        self.__noise_definition = 'temperature'
        print(f'Noise updated to {self.__noise} W')


    @property
    def noise_bandwight(self):
        return self.__noise_bandwight

    @noise_bandwight.setter
    def noise_bandwight(self, new_noise_bandwight):
        self.__noise_bandwight = new_noise_bandwight
        self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
        self.__noise_definition = 'temperature'
        print(f'Noise updated to {self.__noise} W')

    @property
    def noise(self):
        return self.__noise

    @noise.setter
    def noise(self, new_noise):
        self.__noise = new_noise
        self.__noise_definition = 'independant'
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

    @property
    def wave_definition(self):
        return self.__wave_definition

    @wave_definition.setter
    def wave_definition(self, new_wave_definition):
        self.__wave_definition = new_wave_definition

    @property
    def noise_definition(self):
        return self.__noise_definition

    @noise_definition.setter
    def noise_definition(self, new_noise_definition):
        self.__noise_definition = new_noise_definition

    def main(self):
        pass

    def load_scenario(self, scenario_file):
        with open('scenario.json', 'r') as file:
            scenario = json.load(file)

        self.__target_rcs = scenario['target_rcs']
        self.__target_range = scenario['target_range']
        self.__swelring_model = scenario['swelring_model']

        self.__clutter_range = scenario['clutter_range']
        # self.__clutter_reflectivity = scenario['clutter_reflectivity']
        # self.__clutter_ds = scenario['clutter_ds']

        self.__celerity = scenario['celerity']
        self.__wave_definition = scenario['wave_definition']
        if self.__wave_definition == 'frequency':
            self.__frequency = scenario['frequency']
            self.__wavelength = self.__celerity/self.__frequency
        elif self.__wave_definition == 'wavelength':
            self.__wavelength = scenario['wavelength']
            self.__frequency = self.__celerity/self.__wavelength
        else:
            print('Wave definition not recognized')

        self.__power = scenario['power']
        self.__antenna_gain = scenario['antenna_gain']
        self.__loss = scenario['loss']

        self.__boltzmann_ct = scenario['boltzmann_ct']
        self;__noise_definition = scenario['noise_definition']
        if scenario['noise_definition'] == 'temperature':
            self.__system_temperature = scenario['system_temperature']
            self.__noise_bandwight = scenario['noise_bandwight']
            self.__noise = self.__boltzmann_ct * self.__system_temperature * self.__noise_bandwight
        elif self.__noise_definition == 'independant':
            self.__noise = scenario['noise']
            self.__system_temperature = None
            self.__noise_bandwight = None
        else:
            print('Noise definition not recognized')

        self.__dwell_nb_burst = scenario['dwell_nb_burst']
        self.__dwell_total_duration = scenario['dwell_total_duration']
        self.__duty_cycle = scenario['duty_cycle']
        self.Nb = scenario['Nb']
        self.Kb = scenario['Kb']

        self.pfa = scenario['pfa']
        self.desired_pd = scenario['desired_pd']
        print('Scenario loaded')

    # def generate_scenario(self):
