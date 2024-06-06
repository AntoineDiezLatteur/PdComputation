"""
File: InputFrame
Author: antoi
Date: 06/06/2024
Description: 
"""
import customtkinter as ctk

class InputFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        self.scenario = scenario

        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Enter Numerical Values")
        self.label.grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        i=1
        for  param in self.scenario.parameter_list :

            label = ctk.CTkLabel(self, text=f"{param}")
            label.grid(row=i, column=0, pady=5, sticky="w", padx=5)
            entry = ctk.CTkEntry(self, placeholder_text='Enter a value')
            entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)


            if param == 'wavelength':
                entry.configure(state='disabled')
            elif param == 'noise':

                entry.configure(state='disabled')


            if param == 'pfa':
                entry.insert(0, 1e-6)
                self.entries[param] = entry
            elif param == 'desired_pd':
                entry.insert(0, 0.9)
                self.entries[param] = entry
            elif param == 'celerity':
                entry.insert(0, 3e8)
                self.entries[param] = entry
            elif param == 'boltzmann_ct':
                entry.insert(0, 1.38e-23)
                self.entries[param] = entry
            else:
                self.entries[param] = entry




            # entry.insert(0, f"{float(value):.2e}")
            # entry.insert(0, 1)

            i+=1

        # entry_wavelength =
        scenario = {key: float(entry.get()) for key, entry in self.entries.items()}
        print(scenario)



        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=i, column=0, columnspan=2, pady=10, padx=20, sticky="ew")




    def submit_values(self):


        self.entries['wavelength'] = self.entries['celerity'] / self.entries['frequency']
        # self.entries['wavelength'].config(state='disabled')

        self.entries['noise'] = self.entries['bolzmann_ct'] * self.entries['system_temperature'] * self.entries[
            'noise_bandwight']
        # self.values = {key: float(entry.get()) for key, entry in self.entries.items()}
        # self.scenario.scenario_generator(scenario=self.values)
        # self.scenario.load_scenario('scenario.json')
        self.scenario.__target_rcs = scenario['target_rcs']
        self.scenario.__target_range = scenario['target_range']
        self.scenario.__swelring_model = scenario['swelring_model']

        self.scenario.__clutter_rcs = scenario['clutter_rcs']
        self.scenario.__clutter_range = scenario['clutter_range']
        # self.__clutter_reflectivity = scenario['clutter_reflectivity']
        # self.__clutter_ds = scenario['clutter_ds']

        self.scenario.__celerity = scenario['celerity']
        self.scenario.__wave_definition = scenario['wave_definition']
        self.scenario.__frequency = scenario['frequency']
        self.scenario.__wavelength = self.__celerity / self.__frequency
        # elif self.__wave_definition == 'wavelength':
        #     self.__wavelength = scenario['wavelength']
        #     self.__frequency = self.__celerity/self.__wavelength
        # else:
        #     print('Wave definition not recognized')

        self.scenario.__power = scenario['power']
        self.scenario.__antenna_gain = scenario['antenna_gain']
        self.scenario.__doppler_gain_target = scenario['doppler_gain_target']
        self.scenario.__doppler_gain_clutter = scenario['doppler_gain_clutter']
        self.scenario.__loss = scenario['loss']

        self.scenario.__boltzmann_ct = scenario['boltzmann_ct']
        # self.__noise_definition = scenario['noise_definition']
        # if scenario['noise_definition'] == 'temperature':
        self.scenario.__system_temperature = scenario['system_temperature']
        self.scenario.__noise_bandwight = scenario['noise_bandwight']
        self.scenario.__noise = self.scenario.__boltzmann_ct * self.scenario.__system_temperature * self.scenario.__noise_bandwight
        # elif self.__noise_definition == 'independant':
        #     self.__noise = scenario['noise']
        #     self.__system_temperature = None
        #     self.__noise_bandwight = None
        # else:
        #     print('Noise definition not recognized')

        self.scenario.__dwell_nb_burst = scenario['dwell_nb_burst']
        self.scenario.__dwell_total_duration = scenario['dwell_total_duration']
        self.scenario.__duty_cycle = scenario['duty_cycle']
        self.scenario.Nb = scenario['Nb']
        self.scenario.Kb = scenario['Kb']

        self.scenario.pfa = scenario['pfa']
        self.scenario.desired_pd = scenario['desired_pd']
