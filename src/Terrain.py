"""
File: Terrain
Author: antoi
Date: 24/06/2024
Description: 
"""

import numpy as np
import src.computation.Reflection as rfl
from src.loader import TERRAIN_PATH
import json

class Terrain:

    def __init__(self):
        self.step = 100
        self.range_min = 1000
        self.range_max = 100000
        self.nb_cells = (self.range_max - self.range_min) // self.step

        self.__range = np.arange(self.range_min, self.range_max, self.step)
        self.__reflectivity = np.zeros(self.nb_cells)
        self.__height = np.zeros(self.nb_cells)
        self.__terrain_type = np.array(['       ' for i in range(self.nb_cells)])

    def __str__(self):
        topography = []
        reflectivity_map = []
        height_map = []
        for i in range(1, len(self.terrain_type)):
            if i == 1 or self.terrain_type[i] != self.terrain_type[i-1]:
                topography.append(self.terrain_type[i])
            if i == 1 or self.reflectivity[i] != self.reflectivity[i-1]:
                reflectivity_map.append(self.reflectivity[i])
            if i == 1 or self.height[i] != self.height[i-1]:
                height_map.append(self.height[i])

        start_stop_range = []
        current_start = self.range[0]
        current_type = self.terrain_type[0]
        for i in range(1, len(self.terrain_type)):
            current_stop = self.range[i]
            terrain_type = self.terrain_type[i]
            if terrain_type != current_type:
                start_stop_range.append((current_start, self.range[i-1]))
                current_type = terrain_type
                current_start = current_stop

        return f'Topography: {topography}\n' \
                    f'Start_stop: {start_stop_range}\n' \
                    f'Height: {height_map}\n' \
                    f'Reflectivity: {reflectivity_map}'

    def load_terrain(self, terrain_file):
        data_path = f'{TERRAIN_PATH}/{terrain_file}'
        with open(data_path, 'r') as file:
            terrain = json.load(file)
        for obj in terrain:
            start_idx = int((obj['start_range'] - self.range_min) // self.step)
            end_idx = int((obj['stop_range'] - self.range_min) // self.step)
            if obj['type'] == 'sea':
                self.terrain_type[start_idx:end_idx] = 'sea'
                reflectivity = rfl.Reflection().sea_reflectivity(obj['height'])
            elif obj['type'] == 'lowland':
                self.terrain_type[start_idx:end_idx] = 'lowland'
                reflectivity = rfl.Reflection().lowland_reflectivity(obj['height'])
            elif obj['type'] == 'hill':
                self.terrain_type[start_idx:end_idx] = 'hill'
                reflectivity = rfl.Reflection().hill_reflectivity(obj['height'])
            self.height[start_idx:end_idx] = obj['height']
            self.reflectivity[start_idx:end_idx] = reflectivity

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, new_height):
        self.__height = new_height

    @property
    def terrain_type(self):
        return self.__terrain_type

    @terrain_type.setter
    def terrain_type(self, new_terrain_type):
        self.__terrain_type = new_terrain_type

    @property
    def reflectivity(self):
        return self.__reflectivity

    @reflectivity.setter
    def reflectivity(self, new_reflectivity):
        self.__reflectivity = new_reflectivity

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, new_range):
        self.__range = new_range

if __name__ == '__main__':
    terrain = Terrain()
    terrain.load_terrain('terrain.json')
    print(terrain)