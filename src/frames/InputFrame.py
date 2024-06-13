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
        self.label.grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=(10, 5))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        i=1
        for  param in self.scenario.parameter_list :

            label = ctk.CTkLabel(self, text=f"{param}")
            label.grid(row=i, column=0, pady=5, sticky="w", padx=5)
            # entry = ctk.CTkEntry(self, placeholder_text='Enter a value')
            # entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)


            if param == 'wavelength' or param == 'noise':
                entry = ctk.CTkEntry(self, placeholder_text='Computed')
                entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
                entry.configure(state='disabled')
            # elif param == 'noise':
            #     entry = ctk.CTkEntry(self, placeholder_text='Computed')
            #     entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
            #     entry.configure(state='disabled')
            elif param == 'celerity' :
                entry = ctk.CTkEntry(self, placeholder_text='Default value : 3e8')
                entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
                entry.configure(state='disabled')
            elif param == 'boltzmann_ct':
                entry = ctk.CTkEntry(self, placeholder_text='Default value : 1.38e-23')
                entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
                entry.configure(state='disabled')
            else :
                entry = ctk.CTkEntry(self, placeholder_text='Enter a value')
                entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)


            if param == 'pfa':
                entry.insert(0, 1e-6)
                self.entries[param] = entry
            elif param == 'desired_pd':
                entry.insert(0, 0.9)
                self.entries[param] = entry
            else:
                self.entries[param] = entry





            # entry.insert(0, f"{float(value):.2e}")
            # entry.insert(0, 1)

            i+=1

        # entry_wavelength =




        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=i, column=0, columnspan=2, pady=10, padx=20, sticky="ew")




    def submit_values(self):
        # for key, entry in self.entries.items():
        #     print(f"{key}: {entry.get()}")
        scenario = {key: float(entry.get()) for key, entry in self.entries.items() if key != 'wavelength' and key != 'noise' and key != 'celerity' and key != 'boltzmann_ct'}
        # scenario['wavelength'] = self.scenario.celerity / scenario['frequency']
        # scenario['noise'] = self.scenario.boltzmann_ct * scenario['system_temperature'] * scenario['noise_bandwight']
        # wavelength and noise are automatically set thanks to frequency setter, system_temperature and noise_bandwight

        # self.entries['wavelength'] = self.entries['celerity'] / self.entries['frequency']
        # # self.entries['wavelength'].config(state='disabled')
        #
        # self.entries['noise'] = self.entries['bolzmann_ct'] * self.entries['system_temperature'] * self.entries[
        #     'noise_bandwight']
        # self.values = {key: float(entry.get()) for key, entry in self.entries.items()}
        # self.scenario.scenario_generator(scenario=self.values)
        # self.scenario.load_scenario('scenario.json')
        self.scenario.target_rcs = scenario['target_rcs']
        self.scenario.target_range = scenario['target_range']
        self.scenario.swelring_model = scenario['swelring_model']

        self.scenario.clutter_rcs = scenario['clutter_rcs']
        self.scenario.clutter_range = scenario['clutter_range']
        # self.__clutter_reflectivity = scenario['clutter_reflectivity']
        # self.__clutter_ds = scenario['clutter_ds']

        # self.scenario.celerity = scenario['celerity']
        # self.scenario.__wave_definition = scenario['wave_definition']
        self.scenario.frequency = scenario['frequency']
        # self.scenario.wavelength = scenario['wavelength']
        # elif self.__wave_definition == 'wavelength':
        #     self.__wavelength = scenario['wavelength']
        #     self.__frequency = self.__celerity/self.__wavelength
        # else:
        #     print('Wave definition not recognized')

        self.scenario.power = scenario['power']
        self.scenario.antenna_gain = scenario['antenna_gain']
        self.scenario.doppler_gain_target = scenario['doppler_gain_target']
        self.scenario.doppler_gain_clutter = scenario['doppler_gain_clutter']
        self.scenario.loss = scenario['loss']

        # self.scenario.boltzmann_ct = scenario['boltzmann_ct']
        # self.__noise_definition = scenario['noise_definition']
        # if scenario['noise_definition'] == 'temperature':
        self.scenario.system_temperature = scenario['system_temperature']
        self.scenario.noise_bandwight = scenario['noise_bandwight']
        # self.scenario.noise = scenario['noise']
        # elif self.__noise_definition == 'independant':
        #     self.__noise = scenario['noise']
        #     self.__system_temperature = None
        #     self.__noise_bandwight = None
        # else:
        #     print('Noise definition not recognized')

        self.scenario.dwell_nb_burst = scenario['dwell_nb_burst']
        self.scenario.dwell_total_duration = scenario['dwell_total_duration']
        self.scenario.duty_cycle = scenario['duty_cycle']
        self.scenario.Nb = scenario['Nb']
        self.scenario.Kb = scenario['Kb']

        self.scenario.pfa = scenario['pfa']
        self.scenario.desired_pd = scenario['desired_pd']
