# BERT_Scan.py

import subprocess
import argparse
import os

# Get setup info: used for both data-taking and analysis
def getSetupInfo():
    info = {}

    # Default port card slot: currently, only J4 is supported
    port_card_slot = "J4"

    # Hardware configuration
    #hardware_config = "Module"
    #hardware_config = "Module_Chip12"
    #hardware_config = "Module_Chip13"
    #hardware_config = "DP_SMA_Adapter"
    hardware_config = "DP_RedAdapter"

    info["port_card_slot"]  = port_card_slot
    info["hardware_config"] = hardware_config
    
    return info

# Get base directory name: used for both data-taking and analysis
# For now, assume we are using an optical FMC and a port card
def getBaseDirectory():
    info = getSetupInfo()
    port_card_slot  = info["port_card_slot"]
    hardware_config = info["hardware_config"]
    
    # Example: "Optical_FMC_PortCard_J4_DP_RedAdapter"
    base_dir = "Optical_FMC_PortCard_{0}_{1}".format(port_card_slot, hardware_config)
    
    return base_dir

# Get default inputs
def getDefaultInputs(cable_number, cable_type, branch, channel):
    # Default input parameters
    inputs      = {}

    info = getSetupInfo()
    port_card_slot  = info["port_card_slot"]
    hardware_config = info["hardware_config"]

    base_dir = getBaseDirectory()

    # Micro TAP0 range
    tap0_min    = 10
    tap0_max    = 90
    tap0_step   = 10

    # Mini TAP0 range
    #tap0_min    = 20
    #tap0_max    = 120
    #tap0_step   = 10
    
    # Small TAP0 range
    #tap0_min    = 50
    #tap0_max    = 150
    #tap0_step   = 10
    
    # Medium TAP0 range
    #tap0_min    = 100
    #tap0_max    = 300
    #tap0_step   = 10
    
    # Large TAP0 range
    #tap0_min    = 100
    #tap0_max    = 1000
    #tap0_step   = 100
    
    signal      = 0     # Type of secondary signal; use 0 as default.
    TAP1        = 0     # See note below about setting TAP1!!!
    
    # Important!!! You must also update TAP1 settings in CMSIT_RD53B_Optical_BERT.xml:
    # - Don't change DAC_CML_BIAS_0 or DAC_CML_BIAS_2.
    # - DAC_CML_BIAS_1 should be changed to the desired TAP1 setting, for example "0" or "100".
    # - To use TAP1 = 0, CML_CONFIG_SER_EN_TAP and CML_CONFIG_SER_INV_TAP should be set to "0b00".
    # - To use TAP1 > 0, CML_CONFIG_SER_EN_TAP and CML_CONFIG_SER_INV_TAP should be set to "0b01".
    
    output_dir  = "BERT_TAP0_Scans/{0}/elink{1}_{2}_{3}_SS{4}_TAP1_{5}".format(base_dir, cable_number, branch, channel, signal, TAP1)

    inputs["port_card_slot"]    = port_card_slot
    inputs["cable_type"]        = cable_type
    inputs["branch"]            = branch
    inputs["channel"]           = channel
    inputs["tap0_min"]          = tap0_min
    inputs["tap0_max"]          = tap0_max
    inputs["tap0_step"]         = tap0_step
    inputs["signal"]            = signal
    inputs["output_dir"]        = output_dir

    return inputs

# Get user inputs
def getUserInputs():
    # Prompt user for all input parameters
    inputs      = {}
    
    port_card_slot  = str(input("Enter port card slot [J4]: "))
    cable_type      = str(input("Enter cable type [5K, 5K2, 3p2, 2p2, 2p3, 1p3]: "))
    branch          = str(input("Enter branch [A, B, C]: "))
    channel         = str(input("Enter channel [D0, D1, D2, D3]: "))
    tap0_min        = int(input("Enter min TAP0 value: "))
    tap0_max        = int(input("Enter max TAP0 value: "))
    tap0_step       = int(input("Enter step size for TAP0: "))
    signal          = int(input("Select type of secondary signal [0, 1, 2, 3]: "))
    output_dir      = str(input("Output directory: "))
    
    inputs["port_card_slot"]    = port_card_slot
    inputs["cable_type"]        = cable_type
    inputs["branch"]            = branch
    inputs["channel"]           = channel
    inputs["tap0_min"]          = tap0_min
    inputs["tap0_max"]          = tap0_max
    inputs["tap0_step"]         = tap0_step
    inputs["signal"]            = signal
    inputs["output_dir"]        = output_dir
    
    return inputs

# Check for valid inputs
def validInputs(port_card_slot, cable_type, branch, channel, tap0_min, tap0_max, tap0_step, signal, output_dir):
    # Range of valid TAP0 values
    min_val = 0
    max_val = 1023
    # Supported configurations
    port_card_slots = ["J4"]
    cable_types     = ["5K", "5K2", "3p2", "2p2", "2p3", "1p3"]
    branches        = ["A", "B", "C"]
    channels        = ["D0", "D1", "D2", "D3"]
    signal_types    = [0, 1, 2, 3]

    if port_card_slot not in port_card_slots:
        print("The port card slot must be one of these: {0}".format(port_card_slots))
        return False
    if cable_type not in cable_types:
        print("The cable type must be one of these: {0}".format(cable_types))
        return False
    if branch not in branches:
        print("The branch must be one of these: {0}".format(branches))
        return False
    if channel not in channels:
        print("The channel must be one of these: {0}".format(channels))
        return False
    if tap0_min < min_val or tap0_min > max_val:
        print("The tap0_min value {0} is not valid. It must be in the range {1} to {2}.".format(tap0_min, min_val, max_val))
        return False
    if tap0_max < min_val or tap0_max > max_val:
        print("The tap0_max value {0} is not valid. It must be in the range {1} to {2}.".format(tap0_max, min_val, max_val))
        return False
    if tap0_min > tap0_max:
        print("tap0_min ({0}) must be less than or equal to tap0_max ({1})".format(tap0_min, tap0_max))
        return False
    if tap0_step <= 0:
        print("tap0_step ({0}) must be greater than 0".format(tap0_step))
        return False
    if signal not in signal_types:
        print("The signal type must be one of these: {0}".format(signal_types))
        return False
    if not output_dir:
        print("No output directory provided; please provide an output directory.")
        return False
    return True

# Get xml config file name based on port card slot, cable type, and channel
def getXMLConfigFile(port_card_slot, cable_type, branch, channel):
    # Example: CMSIT_RD53B_Optical_J4_Type5K_D0.xml
    # Example: CMSIT_RD53B_Optical_J4_Type3p2_A_D0.xml
    xml_config_file = "CMSIT_RD53B_Optical_{0}_Type{1}_{2}_{3}.xml".format(port_card_slot, cable_type, branch, channel)
    return xml_config_file

# Get unique output file name
def getOutputFile(output_dir):
    i = 1
    output_file = "{0}/scan_{1:03}.log".format(output_dir, i)
    while(os.path.isfile(output_file)):
        #print("File exists: {0}".format(output_file))
        i += 1
        output_file = "{0}/scan_{1:03}.log".format(output_dir, i)
    return output_file

# Scan over TAP0 DAQ settings
def run(port_card_slot, cable_type, branch, channel, tap0_min, tap0_max, tap0_step, signal, output_dir):
    # Important: assign which bash script to use!
    
    # Script for running without a port card
    #bash_script = "./TrackerDAQ/scripts/BERT_Scan.sh"
    
    # Script for running with a port card
    bash_script = "./TrackerDAQ/scripts/PortCard_BERT_Scan.sh"
    
    valid = validInputs(port_card_slot, cable_type, branch, channel, tap0_min, tap0_max, tap0_step, signal, output_dir)
    
    if not valid:
        print("ERROR: Invalid inputs provided. Quitting now!")
        return
    
    xml_config_file = getXMLConfigFile(port_card_slot, cable_type, branch, channel)
    print("xml config file: {0}".format(xml_config_file))
    
    output_file = getOutputFile(output_dir)
    print("output file: {0}".format(output_file))
    
    print("Start BERT TAP0 Scan.")
    for x in range(tap0_min, tap0_max + tap0_step, tap0_step):
        # Run BERT scan script
        # Format signal type setting in 2-bit binary (e.g. 0b00, 0b01, ...)
        sig_setting = format(signal, '#04b')
        output = subprocess.run([bash_script, xml_config_file, str(x), sig_setting, output_dir, output_file])
        # append output to file
        with open(output_file, 'a') as f:
            f.write(str(output) + "\n")
    print("BERT TAP0 Scan is complete!")

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--tap0_min",     "-a",   default=-1,   help="Minimum TAP0 value")
    parser.add_argument("--tap0_max",     "-b",   default=-1,   help="Maximum TAP0 value")
    parser.add_argument("--tap0_step",    "-c",   default=-1,   help="Step size for TAP0")
    parser.add_argument("--signal",       "-d",   default=-1,   help="Select type of secondary signal [0-3]")
    parser.add_argument("--output_dir",   "-e",   default="",   help="Output directory")
    
    options     = parser.parse_args()
    tap0_min    = int(options.tap0_min)
    tap0_max    = int(options.tap0_max)
    tap0_step   = int(options.tap0_step)
    signal      = int(options.signal)
    output_dir  = options.output_dir
    
    if tap0_min < 0 or tap0_max < 0 or tap0_step < 0:
        print("Provide TAP0 DAC min, max, and step (options -a, -b, and -c). The allowed TAP0 range is [0, 1023].")
        return
    if signal < 0:
        print("Provide the type of secondary signal [0-3] with the -d option.")
        return
    if not output_dir:
        print("Provide and output directory with the -e option.")
        return
    
    run(tap0_min, tap0_max, tap0_step, signal, output_dir)

if __name__ == "__main__":
    main()

