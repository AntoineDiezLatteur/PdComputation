# Probability of detection simulator

## Description

For a given radar and scenario, compute the probability of detection and snr of a target depending of the ambiant clutter function of the range. Multiple options are given as single scan pd, multiple scan pd, clutter, no clutter, presence of clutter un a sidelobe.

## Launch Editor

### 1 - To open the editor
```
python main.py -r
```
### 2 - To select a specific radar config file
```
python main.py -r -c config.json
```
### 3 - Launch the editor from a script
Run the script App.py
## HMI presentation
![image](https://github.com/Azo1hz/PdComputation/assets/147478644/25c03af1-0e5b-4b44-a846-90ad99e4287e)
### 1 - Load Configuration button
The button loads the configuration file from the config directory (default : default_config.json)
### 2 - Browse button
Selects the scenario file by opening a file explorer
### 3 - Load JSON Scenario button
Loads the scenario file from the data directory (default : default_scenario)
### 4 - Submit button
Allows to define a custom scenario and submit it for computations (loading a scenario automaticly inserts the values in the boxes)
### 5 - Option menu
Allows to select the kind of desired computations : Single scan Pd, Multiple scan Pd, Snr computation
### 6 - Run computation button
Runs the selected mode computations and displays them on the canvas


