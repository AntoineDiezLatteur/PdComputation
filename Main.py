"""
File: Main
Author: antoi
Date: 03/06/2024
Description: argument parser and main function
"""

import argparse
from src.Scenario import Scenario
from src.computation import Computation
from src.App import App

class Main():
    def __init__(self):
        self.args = self.parse_args

    @property
    def parse_args(self):
        parser = argparse.ArgumentParser(add_help=True)

        parser.add_argument('-r', '--run', action='store_true',
                            help='Edit the scenario file')
        parser.add_argument('-c', '--config', type=str, default='default_config.json',
                            help='Select the config file')
        return parser.parse_args()

    def main(self):
        if self.args.run:
            App(config_file=self.args.config).main()

if __name__ == '__main__':
    Main().main()