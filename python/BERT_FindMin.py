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
    xlim = [0.00, 2.50]
    ylim = [0.0, 500.0]
    inputs = []
    
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
    x_values = [0.35, 0.80, 1.00, 1.60, 1.80, 2.00]
    y_values = [findMin(input_file) for input_file in input_files]
    entry = {}
    entry["x_values"] = x_values
    entry["y_values"] = y_values
    entry["label"]    = "Type 1B Setup 1"
    inputs.append(entry)
    plot(plot_dir, "Type1B_Setup1", x_values, y_values, x_label="Length (m)", y_label="Min TAP0 for 0 errors", setLogY=False)
    
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
    x_values = [0.35, 0.80, 1.00, 1.60, 1.80, 2.00]
    y_values = [findMin(input_file) for input_file in input_files]
    entry = {}
    entry["x_values"] = x_values
    entry["y_values"] = y_values
    entry["label"]    = "Type 1B Setup 2"
    inputs.append(entry)
    plot(plot_dir, "Type1B_Setup2", x_values, y_values, x_label="Length (m)", y_label="Min TAP0 for 0 errors", setLogY=False)

    plotMultiple(plot_dir, "Type1B", inputs, xlim, ylim, x_label="Length (m)", y_label="Min TAP0 for 0 errors", setLogY=False)


def main():
    run()

if __name__ == "__main__":
    main()

