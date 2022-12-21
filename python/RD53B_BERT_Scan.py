# RD53B_BERT_Scan.py

import subprocess
from BERT_Scan import getOutputFile 
from tools import getTempRD53B, makeDir
from datetime import datetime

# Get user inputs
def getUserInputs():
    # Prompt user for input parameters
    inputs                  = {}
    cable_number            = int(input("Enter cable number (must be a positive integer): "))
    channel                 = str(input("Enter channel [D0, D3]: "))
    voltage                 = int(input("Enter voltage (mV) for temperature (must be a positive integer): "))
    
    #output_dir              = "BERT_TAP0_Scans/DoubleDP_DPAdapter/elink_{0}_{1}".format(cable_number, channel)
    output_dir              = "BERT_TAP0_Scans/ShortDoubleDP_DPAdapter/elink_{0}_{1}".format(cable_number, channel)
    #output_dir              = "BERT_TAP0_Scans/ShortDP/DP_TAP1_90"
    #output_dir              = "BERT_TAP0_Scans/ShortDP/DP_CERNFMC"
    #output_dir              = "BERT_TAP0_Scans/ShortDP/DP_KSUFMC"
    #output_dir              = "BERT_TAP0_Scans/ShortDoubleDP_DPAdapter/elink_{0}_{1}_TAP1_100".format(cable_number, channel)
    
    
    inputs["cable_number"]  = cable_number
    inputs["channel"]       = channel
    inputs["voltage"]       = voltage
    inputs["output_dir"]    = output_dir
    return inputs

# Check for valid inputs
def validInputs(cable_number, channel, voltage, output_dir):
    channels = ["D0", "D3"]
    if cable_number <= 0:
        print("The cable number {0} is not valid. It must be greater than 0.".format(cable_number))
        return False
    if channel not in channels:
        print("The channel {0} is not valid. It must be in the set {1}.".format(channel, channels))
        return False
    if voltage <= 0:
        print("The voltage {0} is not valid. It must be greater than 0.".format(voltage))
        return False
    if not output_dir:
        print("No output directory provided; please provide an output directory.")
        return False
    return True

def run(cable_number, channel, voltage, output_dir):
    # Check for valid inputs
    valid = validInputs(cable_number, channel, voltage, output_dir)
    if not valid:
        print("ERROR: Invalid inputs provided. Quitting now!")
        return
    
    makeDir(output_dir)
    output_file = getOutputFile(output_dir)

    # message for log file
    message = ""
    # Get date and time
    now = datetime.now()
    #now_string = now.strftime("%Y-%m-%d %H:%M:%S")
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    # Convert voltage (mV) to temperature (C)
    temperature = getTempRD53B(voltage)
    #temp_log = "voltage: {0} mV, temperature: {1:.1f} C".format(voltage, temperature) 
    
    line            = "------------------------------"
    title_log       = "RD53B BERT TAP0 Scan"
    date_log        = "date: {0}".format(date)
    time_log        = "time: {0}".format(time)
    cable_log       = "cable: {0}".format(cable_number)
    channel_log     = "channel: {0}".format(channel)
    voltage_log     = "voltage: {0} mV".format(voltage)
    temperature_log = "temperature: {0:.1f} C".format(temperature)

    message += line             + "\n"
    message += title_log        + "\n"
    message += line             + "\n"
    message += date_log         + "\n"
    message += time_log         + "\n"
    message += cable_log        + "\n"
    message += channel_log      + "\n"
    message += voltage_log      + "\n"
    message += temperature_log  + "\n"
    message += line             + "\n"
    
    print(message, end='')
    
    # append voltage and temperature to file
    with open(output_file, 'a') as f:
        f.write(message)
    
    output = subprocess.run(["./TrackerDAQ/scripts/RD53B_BERT_Scan.sh", output_dir, output_file])
    print("Done")

