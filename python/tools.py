# tools.py

import os
import re
import numpy as np

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# return list of TAP0 settings that had errors for RD53A data
def findErrorsRD53A(input_file):
    f = open(input_file, 'r')
    # list of TAP0 settings that had errors
    errors = []
    for line in f:
        # check for errors
        if "returncode=1" in line:
            # get all numbers in string
            numbers = re.findall(r'\d+', line)
            # first number is TAP0 setting
            z = int(numbers[0])
            #print("ERROR: {0}".format(line), end='')
            errors.append(z)
    f.close()
    return errors

# return list of TAP0 settings that had errors for RD53B data
def findErrorsRD53B(input_file):
    f = open(input_file, 'r')
    # list of TAP0 settings that had errors
    errors = []
    previous_TAP0_value = -1
    previous_TAP0_line_number = -1
    lines = f.readlines()
    f_len = len(lines)
    for i, line in enumerate(lines):
        # check for errors
        if "TAP0" in line:
            #print("Found TAP0 in line {0}".format(i))
            array = line.split()
            z = int(array[-1])
            # if this TAP0 and the previous are two lines apart (yes, the log files are weird), there was an error
            if i - 2 == previous_TAP0_line_number:
                errors.append(previous_TAP0_value)
            # if this is the last line in the file, there was an error
            if i == f_len - 1:
                errors.append(z)
            previous_TAP0_value = z
            previous_TAP0_line_number = i
    f.close()
    return errors

# get data:
# x = TAP0 setting
# y = bit error rate
def getBERTData(input_file, useRD53B):
    # check for errors
    printError = True
    errors = []
    if useRD53B:
        errors = findErrorsRD53B(input_file)
    else:
        errors = findErrorsRD53A(input_file)
    if errors and printError:
        print("ERROR for {0}".format(input_file))
        print(" - There were errors for these TAP0 settings: {0}".format(errors))
        print(" - These data points will be skipped.")
    f = open(input_file, 'r')
    x_values = []
    y_values = []
    for line in f:
        # TAP0 DAC Setting (x values)
        if useRD53B:
            if "TAP0" in line:
                array = line.split()
                x = int(array[-1])
                # skip the x value if there were errors
                if x not in errors:
                    x_values.append(x)
        else:
            if "CML_TAP0_BIAS" in line:
                array = line.split()
                # must remove " before using int()
                x = int(array[-1].replace('"', ''))
                # skip the x value if there were errors
                if x not in errors:
                    x_values.append(x)
        # Total error counter (y values)
        if "Final counter" in line:
            # get all numbers in string
            numbers = [int(s) for s in line.split() if s.isdigit()]
            y = numbers[0]
            y_values.append(y)
    
    f.close()
    return [x_values, y_values]

# Get temperature for RD53B; input: voltage (mV), output: temperature (C)
# - Based on functions from excel file from Matt Joyce (matthew.lawrence.joyce@cern.ch)
# - The excel file is "Temperature_NTC.xlsx" in the attachments section here: https://twiki.cern.ch/twiki/bin/view/Main/USTFPXPhase2
def getTempRD53B(voltage_mv):
    # current in amps
    current     = 0.05
    parameter_1 = current / 4990.0
    # convert voltage from mV to V
    voltage_v   = voltage_mv / 1e3
    # resistance (ohms?)
    resistance  = (voltage_v / parameter_1) / 1e3
    # temperature (C)
    temperature = 1.0 / (1.0 / 298.15 + np.log(resistance / 10) / 3435.0) - 273.15
    return temperature

