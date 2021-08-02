# BERT_Scan.py

import subprocess

# Scan over TAP0 DAQ settings
def run(tap0_min, tap0_max, tap0_step):
    for x in range(tap0_min, tap0_max + tap0_step, tap0_step):
        # Use BERT scan script
        output = subprocess.run(["./TrackerDAQ/scripts/BERT_Scan.sh", str(x)])
        print(output)
        #output = subprocess.check_output(["./TrackerDAQ/scripts/BERT_Scan.sh", "100"])
        #print(output)

def main():
    tap0_min  = 50
    tap0_max  = 600
    tap0_step = 10
    run(tap0_min, tap0_max, tap0_step)

if __name__ == "__main__":
    main()

