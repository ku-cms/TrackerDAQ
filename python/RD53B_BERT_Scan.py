# RD53B_BERT_Scan.py

import subprocess

from BERT_Scan import getOutputFile 

# Get user inputs
def getUserInputs():
    # Prompt user for input parameters
    inputs                  = {}
    cable_number            = int(input("Enter cable number: "))
    channel                 = str(input("Enter channel [D0, D3]: "))
    voltage                 = int(input("Enter voltage from multimeter for temperature (mV): "))
    output_dir              = "BERT_TAP0_Scans/DoubleDP_DPAdapter/elink_{0}_{1}".format(cable_number, channel)
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
    valid = validInputs(cable_number, channel, voltage, output_dir)
    if not valid:
        print("ERROR: Invalid inputs provided. Quitting now!")
        return
    output_file = getOutputFile(output_dir)
    output = subprocess.run(["./TrackerDAQ/scripts/RD53B_BERT_Scan.sh", output_dir, output_file])
    print("---------- output ----------")
    print(output)

