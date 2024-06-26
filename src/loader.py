"""
File: loader
Author: antoi
Date: 06/06/2024
Description: Hold the paths to the data and config folders
"""

import os

class Loader:
    def __init__(self):
        self.data_path = os.path.dirname(os.path.abspath(__file__)) + '/../data'
        self.config_path = os.path.dirname(os.path.abspath(__file__)) + '/../config'
        self.terrain_path = os.path.dirname(os.path.abspath(__file__)) + '/../terrain'

loader = Loader()
DATA_PATH = loader.data_path
CONFIG_PATH = loader.config_path
TERRAIN_PATH = loader.terrain_path

__all__ = ['DATA_PATH', 'CONFIG_PATH', 'TERRAIN_PATH']