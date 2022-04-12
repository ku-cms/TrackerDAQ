# BERT_Run_Scan.py

from BERT_Scan import run

def main():
    
    # Prompt user for input parameters
    tap0_min    = int(input("Enter min TAP0 value: "))
    tap0_max    = int(input("Enter max TAP0 value: "))
    tap0_step   = int(input("Enter step size for TAP0: "))
    signal      = int(input("Select type of secondary signal [0-3]: "))
    output_dir  = str(input("Output directory: "))
    
    # Press enter to continue...
    input("Press enter to continue... ")

    # TODO:
    # - add function to check for valid inputs
    
    run(tap0_min, tap0_max, tap0_step, signal, output_dir)

if __name__ == "__main__":
    main()

