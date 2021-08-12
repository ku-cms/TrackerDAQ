# tools.py

import os
import re

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# return list of TAP0 settings that had errors
def findErrors(input_file):
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

# get data:
# x = TAP0 setting
# y = bit error rate
def getBERTData(input_file):
    # check for errors
    printError = False
    errors = findErrors(input_file)
    if errors and printError:
        print("ERROR for {0}".format(input_file))
        print("There were errors for these TAP0 settings: {0}".format(errors))
        print("These will be skipped.")
    f = open(input_file, 'r')
    x_values = []
    y_values = []
    for line in f:
        # TAP0 DAC Setting (x values)
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

