"""
File: Main
Author: antoi
Date: 03/06/2024
Description: 
"""

import argparse
from src.Scenario import Scenario
from src.Computation import Computation
from src.App import App


class Main():

    def __init__(self):
        self.args = self.parse_args

    @property
    def parse_args(self):
        parser = argparse.ArgumentParser(add_help=True)

        parser.add_argument('-e', '--edit', action='store_true',
                            help='Edit the scenario file')
        parser.add_argument('-r', '--run', action='store_true',
                            help='Run the scenario')
        parser.add_argument('-s', '--scenario', type=str, default='scenario.json',
                            help='Select the scenario file')

        return parser.parse_args()

    def main(self):
        scenario = Scenario()
        if self.args.edit:
            App().main()

        elif self.args.run:
            scenario.load_scenario(scenario_file=self.args.scenario)
            Computation(scenario).run()


if __name__ == '__main__':
    Main().main()
    #TODO: Add a json generator, an IHM scenario editor, clutter rcs computation, detailed gain/loss computation



