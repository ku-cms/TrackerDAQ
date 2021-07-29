# BERT_Analyze.py

import re
from BERT_Plot import plot, plotMultiple

def findErrors(input_file):
    f = open(input_file, 'r')
    errors = []
    for line in f:
        # check for errors
        if "returncode=1" in line:
            # get all numbers in string
            numbers = re.findall(r'\d+', line)
            z = int(numbers[0])
            print("ERROR: {0}".format(line), end='')
            #print(numbers)
            #print(z)
            errors.append(z)
    f.close()
    return errors

def getData(input_file):
    # check for errors
    errors = findErrors(input_file)
    if errors:
        print("ERROR for {0}".format(input_file))
        print("There were errors for these TAP0 settings: {0}".format(errors))
        print("These will be skipped.")
    f = open(input_file, 'r')
    x_values = []
    y_values = []
    for line in f:
        # TAP0 DAC Setting (x values)
        if "CML_TAP0_BIAS" in line:
            array = line.split()
            # must remove " before using int()
            x = int(array[-1].replace('"', ''))
            # skip the x value if there were errors
            if x not in errors:
                x_values.append(x)
            #print(line)
            #print(array)
            #print(x)
        # Total error counter (y values)
        if "Final counter" in line:
            # get all numbers in string
            numbers = [int(s) for s in line.split() if s.isdigit()]
            y = numbers[0]
            y_values.append(y)
            #print(line)
            #print(numbers)
    
    f.close()
    return [x_values, y_values]

def analyze(input_file, plot_dir, output_file):
    debug = False
    data = getData(input_file)
    x_values = data[0]
    y_values = data[1]
    # check for the same number of x and y values
    if len(x_values) != len(y_values):
        print("ERROR: number of x and v values do not match")
        print("input file: {0}, num x vals: {1}, num y vals: {2}".format(input_file, len(x_values), len(y_values)))
        return
    if debug:
        print("input file: {0}, num x vals: {1}, num y vals: {2}".format(input_file, len(x_values), len(y_values)))
    plot(plot_dir, output_file, x_values, y_values)

def analyzeScans():
    plot_dir    = "plots/BERT_Scan_SingleDP_Data"
    data_dir    = "data/BERT_Scan_SingleDP_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    output_file = "BERT_scan_002"
    input_file  = "{0}/scan_002.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    output_file = "BERT_scan_003"
    input_file  = "{0}/scan_003.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_Data"
    data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink101_Data"
    data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink101_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    output_file = "BERT_scan_002"
    input_file  = "{0}/scan_002.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    output_file = "BERT_scan_003"
    input_file  = "{0}/scan_003.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink102_Data"
    data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink102_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink104_Data"
    data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink104_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink106_Data"
    data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink106_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink111_Data"
    data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink111_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)

def makeCombinedPlots():
    # create combined plot
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_001"
    xlim = [49.0, 101.0]
    ylim = [0.0, 1.0e12]
    inputs = []
    
    input_file = "data/BERT_Scan_SingleDP_Data/scan_003.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:cherry red"
    scan["label"]    = "Single DP"
    inputs.append(scan)
    
    input_file = "data/BERT_Scan_DoubleDP_DoubleBonn_Data/scan_001.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:apple green"
    scan["label"]    = "Double DP Double Bonn"
    inputs.append(scan)
    
    input_file = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink101_Data/scan_001.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:bright blue"
    scan["label"]    = "Double DP Double Bonn Double Yellow e-link 101"
    inputs.append(scan)
    
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # create combined plot
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_002"
    xlim = [45.0, 305.0]
    ylim = [0.0, 1.0e12]
    inputs = []
    
    input_file = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink101_Data/scan_003.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:cherry red"
    scan["label"]    = "e-link 101 (34 AWG, 0.35 m)"
    inputs.append(scan)
    
    input_file = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink102_Data/scan_001.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:apple green"
    scan["label"]    = "e-link 102 (34 AWG, 0.80 m)"
    inputs.append(scan)
    
    input_file = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink104_Data/scan_001.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:bright blue"
    scan["label"]    = "e-link 104 (34 AWG, 1.00 m)"
    inputs.append(scan)
    
    input_file = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink106_Data/scan_001.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:tangerine"
    scan["label"]    = "e-link 106 (34 AWG, 1.60 m)"
    inputs.append(scan)
    
    input_file = "data/BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink111_Data/scan_001.log"
    data = getData(input_file)
    scan = {}
    scan["x_values"] = data[0]
    scan["y_values"] = data[1]
    scan["color"]    = "xkcd:electric purple"
    scan["label"]    = "e-link 111 (34 AWG, 1.80 m)"
    inputs.append(scan)
    
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)

def main():
    analyzeScans()
    makeCombinedPlots()

if __name__ == "__main__":
    main()

