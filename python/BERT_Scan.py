# BERT_Scan.py

import subprocess
import argparse
import os

# Get default inputs
def getDefaultInputs(cable_number, channel):
    # Default input parameters
    inputs      = {}
    
    tap0_min    = 400
    tap0_max    = 1000
    tap0_step   = 100
    
    #tap0_min    = 100
    #tap0_max    = 300
    #tap0_step   = 10
    
    #tap0_min    = 5
    #tap0_max    = 50
    #tap0_step   = 5
    
    signal      = 0     # Type of secondary signal; use 0 as default.
    TAP1        = 75    # See note below about setting TAP1!!!
    
    # Important!!! You must also update TAP1 settings in CMSIT_RD53B_Optical_BERT.xml:
    # - Don't change DAC_CML_BIAS_0 or DAC_CML_BIAS_2.
    # - DAC_CML_BIAS_1 should be changed to the desired TAP1 setting, for example "0" or "100".
    # - To use TAP1 = 0, CML_CONFIG_SER_EN_TAP and CML_CONFIG_SER_INV_TAP should be set to "0b00".
    # - To use TAP1 > 0, CML_CONFIG_SER_EN_TAP and CML_CONFIG_SER_INV_TAP should be set to "0b01".
    
    #output_dir  = "BERT_TAP0_Scans/SingleDP/CERN_FMC_FC7_FW_v4.2"
    #output_dir  = "BERT_TAP0_Scans/SingleDP/KSU_FMC_FC7_FW_v4.2"
    #output_dir  = "BERT_TAP0_Scans/SingleDP/KSU_FMC_FC7_FW_v4.2_TAP1_100"
    #output_dir  = "BERT_TAP0_Scans/SingleDP/KSU_FMC_FC7_FW_v4.2_HybridID_3"
    
    #output_dir  = "BERT_TAP0_Scans/CERN_FMC_DoubleDP_DPAdapter/elink{0}_{1}_SS{2}".format(cable_number, channel, signal)
    #output_dir  = "BERT_TAP0_Scans/KSU_FMC_DoubleDP_DPAdapter/elink{0}_{1}_SS{2}".format(cable_number, channel, signal)
    #output_dir  = "BERT_TAP0_Scans/CERN_FMC_DoubleDP_DPAdapter/elink{0}_{1}_SS{2}_TAP1_10".format(cable_number, channel, signal)
    
    # RD53B + port card with e-link in J2:
    #output_dir  = "BERT_TAP0_Scans/Optical_FMC_PortCard_DP_SMA_Adapter/elink{0}_{1}_SS{2}".format(cable_number, channel, signal)
    #output_dir  = "BERT_TAP0_Scans/Optical_FMC_PortCard_DP_SMA_Adapter/elink{0}_{1}_SS{2}_TAP1_{3}".format(cable_number, channel, signal, TAP1)
    #output_dir  = "BERT_TAP0_Scans/Optical_FMC_PortCard_J2_DP_RedAdapter/elink{0}_{1}_SS{2}_TAP1_{3}".format(cable_number, channel, signal, TAP1)
    
    # RD53B + port card with e-link in J3:
    #output_dir  = "BERT_TAP0_Scans/Optical_FMC_PortCard_J3_DP_SMA_Adapter/elink{0}_{1}_SS{2}_TAP1_{3}".format(cable_number, channel, signal, TAP1)
    output_dir  = "BERT_TAP0_Scans/Optical_FMC_PortCard_J3_DP_RedAdapter/elink{0}_{1}_SS{2}_TAP1_{3}".format(cable_number, channel, signal, TAP1)

    inputs["tap0_min"]      = tap0_min
    inputs["tap0_max"]      = tap0_max
    inputs["tap0_step"]     = tap0_step
    inputs["signal"]        = signal
    inputs["output_dir"]    = output_dir
    return inputs

# Get user inputs
def getUserInputs():
    # Prompt user for input parameters
    inputs      = {}
    tap0_min    = int(input("Enter min TAP0 value: "))
    tap0_max    = int(input("Enter max TAP0 value: "))
    tap0_step   = int(input("Enter step size for TAP0: "))
    signal      = int(input("Select type of secondary signal [0-3]: "))
    output_dir  = str(input("Output directory: "))
    inputs["tap0_min"]      = tap0_min
    inputs["tap0_max"]      = tap0_max
    inputs["tap0_step"]     = tap0_step
    inputs["signal"]        = signal
    inputs["output_dir"]    = output_dir
    return inputs

# Check for valid inputs
def validInputs(tap0_min, tap0_max, tap0_step, signal, output_dir):
    min_val = 0
    max_val = 1023
    signal_types = [0, 1, 2, 3]
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

# Get unique output file name
def getOutputFile(output_dir):
    i = 1
    output_file = "{0}/scan_{1:03}.log".format(output_dir, i)
    while(os.path.isfile(output_file)):
        #print("File exists: {0}".format(output_file))
        i += 1
        output_file = "{0}/scan_{1:03}.log".format(output_dir, i)
    print("Final output file: {0}".format(output_file))
    return output_file

# Scan over TAP0 DAQ settings
def run(tap0_min, tap0_max, tap0_step, signal, output_dir):
    # assign bash script
    #bash_script = "./TrackerDAQ/scripts/BERT_Scan.sh"
    bash_script = "./TrackerDAQ/scripts/PortCard_BERT_Scan.sh"
    valid = validInputs(tap0_min, tap0_max, tap0_step, signal, output_dir)
    if not valid:
        print("ERROR: Invalid inputs provided. Quitting now!")
        return
    output_file = getOutputFile(output_dir)
    for x in range(tap0_min, tap0_max + tap0_step, tap0_step):
        # Run BERT scan script
        # Format signal type setting in 2-bit binary (e.g. 0b00, 0b01, ...)
        sig_setting = format(signal, '#04b')
        output = subprocess.run([bash_script, str(x), sig_setting, output_dir, output_file])
        # append output to file
        with open(output_file, 'a') as f:
            f.write(str(output) + "\n")

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

