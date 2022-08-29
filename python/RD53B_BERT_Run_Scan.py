# RD53B_BERT_Run_Scan.py

from RD53B_BERT_Scan import run, getUserInputs

def main():
    # get user inputs
    inputs = getUserInputs()
    cable_number    = inputs["cable_number"]
    channel         = inputs["channel"]
    voltage         = inputs["voltage"]
    output_dir      = inputs["output_dir"]
    # Press enter to continue...
    input("Press enter to continue... ")
    # run scan
    run(cable_number, channel, voltage, output_dir)

if __name__ == "__main__":
    main()

