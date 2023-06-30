# tools.py

import csv
import os
import re
import numpy as np

# TODO:
# - If error occur in logs for port card data, test and update "find error" functions.

# DONE:
# - Improve getBERTData() for RD53A and port card + RD53B use cases
# - Save BERT TAP0 scan data to csv files
# - Fix bug: plot and record number of bits with errors instead of frames with errors

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# read csv file: takes a csv file as input and outputs data in a matrix
def readCSV(input_file):
    data = []
    with open(input_file, mode="r", newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            data.append(row)
    return data

# write csv file: takes data matrix as input and outputs a csv file 
def writeCSV(output_file, data):
    with open(output_file, mode="w", newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)

# check if all values in list are the same
def valuesAreSame(values):
    # If there are no values, return false:
    if len(values) == 0:
        return False
    else:
        first_value = values[0]
        for value in values:
            if value != first_value:
                return False
        return True

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
        # Warning: can't use only "TAP0" due to new header in log file
        if "Setting TAP0" in line:
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

# get data from log file:
# x = TAP0 setting
# y = bit error rate
def getBERTData(input_file, useRD53B):
    # check for errors
    printError = True
    # Updated TAP0 variable name: works for RD53A and port card + RD53B
    TAP0_variable = "DAC_CML_BIAS_0"
    errors = []
    
    # TODO: if error occurs when using a port card, test find error functions
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
    
    # Get x and y values
    # Updated version: works for RD53A and port card + RD53B
    for line in f:
        # Save TAP0 DAC as x values
        if TAP0_variable in line:
            array = line.split()
            # must remove " before using int()
            x = int(array[-1].replace('"', ''))
            # skip the x value if there were errors
            if x not in errors:
                x_values.append(x)
        # Save total error counter as y values
        if "Final counter" in line:
            # get all numbers in string
            # WARNING: The final counter has the number of frames with errors and bits with errors
            # - We should use the number of bits with errors!!!
            # - Note: bits with errors ~ 32 * (frames with errors)
            numbers = [int(s) for s in line.split() if s.isdigit()]
            y = numbers[-1]
            #print("Number of numbers: {0}; numbers = {1}; y = {2}".format(len(numbers), numbers, y))
            y_values.append(y)
    
    f.close()
    return [x_values, y_values]

# Get temperature for RD53B; input: voltage (mV), output: temperature (C)
# - Connect multimeter to GND and NTC pins on the RD53B CROCv1 SCC to measure voltage (mV).
# - Based on functions from excel file from Matt Joyce (matthew.lawrence.joyce@cern.ch)
# - The excel file is "Temperature_NTC.xlsx" in the attachments section here: https://twiki.cern.ch/twiki/bin/view/Main/USTFPXPhase2
def getTempRD53B(voltage_mv):
    if voltage_mv <= 0:
        print("ERROR: Positive voltage required; the voltage {0} is not positive!".format(voltage_mv))
        return -999
    else:
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

