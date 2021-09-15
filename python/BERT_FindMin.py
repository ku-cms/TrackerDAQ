# BERT_FindMin.py

from BERT_Plot import plot, plotMultiple
from tools import getBERTData

def findMin(input_file):
    data = getBERTData(input_file)
    x_values = data[0]
    y_values = data[1]
    for i in range(len(x_values) - 1, -1, -1):
        #print("{0}: ({1}, {2})".format(i, x_values[i], y_values[i]))
        if y_values[i] > 0:
            answer = x_values[i+1]
            break
    return answer

def run():
    plot_dir = "plots/BERT_Min_TAP0"
    y_axis_label = "TAP0 for BER=10^(-11)"
    xlim = [0.00, 2.50]
    ylim = [0.0, 500.0]
    
    inputs_Type1B = []
    inputs_Setup1 = []
    inputs_Type1A = []
    inputs_Setup2 = []

    x_values = [0.35, 0.80, 1.00, 1.60, 1.80, 2.00]
    
    # Description:
    # Type 1B elinks, new power supply
    # Bonn boards and yellow boards 
    input_files = []
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink101/scan_005.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink102/scan_003.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink104/scan_003.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink106/scan_003.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink111/scan_003.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink113/scan_003.log")
    y_values = [findMin(input_file) for input_file in input_files]
    y_errors = [10.0] * len(y_values)
    entry = {}
    entry["x_values"] = x_values
    entry["y_values"] = y_values
    entry["y_errors"] = y_errors
    entry["label"]    = "Type 1B (34 AWG) Setup 1"
    inputs_Type1B.append(entry)
    inputs_Setup1.append(entry)
    plot(plot_dir, "Type1B_Setup1", x_values, y_values, x_label="Length (m)", y_label=y_axis_label, setLogY=False, y_errors=y_errors)
    
    # Description:
    # Type 1B elinks, new power supply
    # DP to Type 1 elink adapter board
    input_files = []
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink101/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink102/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink104/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink106/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink111/scan_002.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink113/scan_001.log")
    y_values = [findMin(input_file) for input_file in input_files]
    y_errors = [10.0] * len(y_values)
    entry = {}
    entry["x_values"] = x_values
    entry["y_values"] = y_values
    entry["y_errors"] = y_errors
    #entry["label"]    = "Type 1B (34 AWG) Setup 2"
    entry["label"]    = "Type 1B (34 AWG)"
    inputs_Type1B.append(entry)
    inputs_Setup2.append(entry)
    plot(plot_dir, "Type1B_Setup2", x_values, y_values, x_label="Length (m)", y_label=y_axis_label, setLogY=False, y_errors=y_errors)


    x_values = [0.35, 0.80, 1.00, 1.40, 1.60, 1.80, 2.00]
    
    # Description:
    # Type 1A elinks, new power supply
    # Bonn boards and yellow boards 
    input_files = []
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink136/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink140/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink145/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink149/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink154/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink172/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink178/scan_001.log")
    y_values = [findMin(input_file) for input_file in input_files]
    y_errors = [10.0] * len(y_values)
    entry = {}
    entry["x_values"] = x_values
    entry["y_values"] = y_values
    entry["y_errors"] = y_errors
    entry["label"]    = "Type 1A (36 AWG) Setup 1"
    inputs_Type1A.append(entry)
    inputs_Setup1.append(entry)
    plot(plot_dir, "Type1A_Setup1", x_values, y_values, x_label="Length (m)", y_label=y_axis_label, setLogY=False, y_errors=y_errors)

    # Description:
    # Type 1A elinks, new power supply
    # DP to Type 1 elink adapter board
    input_files = []
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink136/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink140/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink145/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink149/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink172/scan_001.log")
    input_files.append("data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink178/scan_001.log")
    y_values = [findMin(input_file) for input_file in input_files]
    y_errors = [10.0] * len(y_values)
    entry = {}
    entry["x_values"] = x_values
    entry["y_values"] = y_values
    entry["y_errors"] = y_errors
    #entry["label"]    = "Type 1A (36 AWG) Setup 2"
    entry["label"]    = "Type 1A (36 AWG)"
    inputs_Type1A.append(entry)
    inputs_Setup2.append(entry)
    plot(plot_dir, "Type1A_Setup2", x_values, y_values, x_label="Length (m)", y_label=y_axis_label, setLogY=False, y_errors=y_errors)

    plotMultiple(plot_dir, "Type1B", inputs_Type1B, xlim, ylim, x_label="Length (m)", y_label=y_axis_label, setLogY=False, alpha=0.5)
    plotMultiple(plot_dir, "Type1A", inputs_Type1A, xlim, ylim, x_label="Length (m)", y_label=y_axis_label, setLogY=False, alpha=0.5)
    plotMultiple(plot_dir, "Setup1", inputs_Setup1, xlim, ylim, x_label="Length (m)", y_label=y_axis_label, setLogY=False, alpha=0.5)
    plotMultiple(plot_dir, "Setup2", inputs_Setup2, xlim, ylim, x_label="Length (m)", y_label=y_axis_label, setLogY=False, alpha=0.5)

def main():
    run()

if __name__ == "__main__":
    main()

