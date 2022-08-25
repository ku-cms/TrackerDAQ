# RD53B_BERT_Scan.py

# Get user inputs
def getUserInputs():
    # Prompt user for input parameters
    inputs                  = {}
    cable_number            = int(input("Enter cable number: "))
    channel                 = str(input("Enter channel [D0, D3]: "))
    voltage                 = int(input("Enter voltage from multimeter for temperature (mV): "))
    output_dir              = "BERT_TAP0_Scans/DoubleDP_DPAdapter/elink{0}_{1}".format(cable_number, channel)
    inputs["cable_number"]  = cable_number
    inputs["channel"]       = channel
    inputs["voltage"]       = voltage
    inputs["output_dir"]    = output_dir
    return inputs

def run(cable_number, channel, voltage, output_dir):
    print("Running")

