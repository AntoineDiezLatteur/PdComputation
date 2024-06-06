"""
File: loader
Author: antoi
Date: 06/06/2024
Description: 
"""

import os

class Loader:
    def __init__(self, folder):
        self.data_path = os.path.dirname(os.path.abspath(__file__)) + '/../' + folder


loader = Loader('data')
DATA_PATH = loader.data_path

__all__ = ['DATA_PATH']