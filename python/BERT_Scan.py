# BERT_Scan.py

import subprocess
import argparse


# Scan over TAP0 DAQ settings
def run(tap0_min, tap0_max, tap0_step, output_dir):
    for x in range(tap0_min, tap0_max + tap0_step, tap0_step):
        # Run BERT scan script
        output = subprocess.run(["./TrackerDAQ/scripts/BERT_Scan.sh", str(x), output_dir])
        print(output)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--tap0_min",     "-a",   default=-1,   help="Minimum TAP0 value")
    parser.add_argument("--tap0_max",     "-b",   default=-1,   help="Maximum TAP0 value")
    parser.add_argument("--tap0_step",    "-c",   default=-1,   help="Step size for TAP0")
    parser.add_argument("--output_dir",   "-d",   default="",   help="output directory")
    
    options     = parser.parse_args()
    tap0_min    = int(options.tap0_min)
    tap0_max    = int(options.tap0_max)
    tap0_step   = int(options.tap0_step)
    output_dir  = options.output_dir
    
    if tap0_min < 0 or tap0_max < 0 or tap0_step < 0:
        print("Provide TAP0 DAC min, max, and step (options -a, -b, and -c). The allowed TAP0 range is [0, 1000].")
        return
    if not output_dir:
        print("Provide and output directory with the -d option.")
        return
    
    run(tap0_min, tap0_max, tap0_step, output_dir)

if __name__ == "__main__":
    main()

