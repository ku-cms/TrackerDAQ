# BERT_Scan.py

import subprocess
import argparse
import os

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
    output_file = getOutputFile(output_dir)
    for x in range(tap0_min, tap0_max + tap0_step, tap0_step):
        # Run BERT scan script
        # Format signal type setting in 2-bit binary (e.g. 0b00, 0b01, ...)
        sig_setting = format(signal, '#04b')
        output = subprocess.run(["./TrackerDAQ/scripts/BERT_Scan.sh", str(x), sig_setting, output_dir, output_file])
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

