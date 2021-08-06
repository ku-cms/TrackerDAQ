# BERT_Analyze.py

import os
import glob
import re
from BERT_Plot import plot, plotMultiple

# return list of TAP0 settings that had errors
def findErrors(input_file):
    f = open(input_file, 'r')
    # list of TAP0 settings that had errors
    errors = []
    for line in f:
        # check for errors
        if "returncode=1" in line:
            # get all numbers in string
            numbers = re.findall(r'\d+', line)
            # first number is TAP0 setting
            z = int(numbers[0])
            #print("ERROR: {0}".format(line), end='')
            errors.append(z)
    f.close()
    return errors

def getData(input_file):
    # check for errors
    printError = False
    errors = findErrors(input_file)
    if errors and printError:
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
        # Total error counter (y values)
        if "Final counter" in line:
            # get all numbers in string
            numbers = [int(s) for s in line.split() if s.isdigit()]
            y = numbers[0]
            y_values.append(y)
    
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

# run over a single directory
def runDir(plot_dir, data_dir):
    # get list of input files in directory
    files = glob.glob(data_dir + "/scan_*.log")
    for input_file in files:
        # get output file name based on input file name
        name        = os.path.basename(input_file)
        x           = name.split(".")[0]
        output_file = "BERT_" + x
        analyze(input_file, plot_dir, output_file)

# run over directories in base directory
def runSet(base_plot_dir, base_data_dir):
    # get list of directories in base directory
    dirs = glob.glob(base_data_dir + "/*")
    for data_dir in dirs:
        # get name for plot directory
        name = os.path.basename(data_dir)
        plot_dir = "{0}/{1}".format(base_plot_dir, name)
        print(" - {0}".format(name))
        runDir(plot_dir, data_dir)

# make a plot for each scan
def analyzeScans():
    plot_dir    = "plots/BERT_Scan_SingleDP_Data"
    data_dir    = "data/BERT_Scan_SingleDP_Data"
    runDir(plot_dir, data_dir)

    plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_Data"
    data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_Data"
    runDir(plot_dir, data_dir)
    
    base_plot_dir    = "plots/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow"
    base_data_dir    = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow"
    runSet(base_plot_dir, base_data_dir)

# add entry to list of inputs
# each entry is a dictionary
def addEntry(input_list, input_file, label):
    data = getData(input_file)
    entry = {}
    entry["x_values"] = data[0]
    entry["y_values"] = data[1]
    entry["label"]    = label 
    input_list.append(entry)

# make plots with multiple scans
def makeCombinedPlots():
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_001"
    xlim = [49.0, 101.0]
    ylim = [0.0, 1.0e12]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_SingleDP_Data/scan_003.log",
        label       = "Single DP",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_DoubleDP_DoubleBonn_Data/scan_001.log",
        label       = "Double DP Double Bonn",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/flex0p10m/scan_001.log",
        label       = "Add Double Yellow & flex (0.10 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/flex0p35m/scan_001.log",
        label       = "Add Double Yellow & flex (0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink101/scan_001.log",
        label       = "Add Double Yellow & e-link 101 (34 AWG, 0.35 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_002"
    xlim = [49.0, 101.0]
    ylim = [0.0, 1.0e12]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/flex0p10m/scan_001.log",
        label       = "flex (0.10 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/flex0p35m/scan_001.log",
        label       = "flex (0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/flex1p00m/scan_001.log",
        label       = "flex (1.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_003"
    xlim = [45.0, 305.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink101/scan_003.log",
        label       = "e-link 101 (34 AWG, 0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink102/scan_001.log",
        label       = "e-link 102 (34 AWG, 0.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink104/scan_001.log",
        label       = "e-link 104 (34 AWG, 1.00 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink106/scan_001.log",
        label       = "e-link 106 (34 AWG, 1.60 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink111/scan_001.log",
        label       = "e-link 111 (34 AWG, 1.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink113/scan_001.log",
        label       = "e-link 113 (34 AWG, 2.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_004"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink101/scan_004.log",
        label       = "e-link 101 (34 AWG, 0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink102/scan_002.log",
        label       = "e-link 102 (34 AWG, 0.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink104/scan_002.log",
        label       = "e-link 104 (34 AWG, 1.00 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink106/scan_002.log",
        label       = "e-link 106 (34 AWG, 1.60 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink111/scan_002.log",
        label       = "e-link 111 (34 AWG, 1.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink113/scan_002.log",
        label       = "e-link 113 (34 AWG, 2.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_005"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink101/scan_005.log",
        label       = "e-link 101 (34 AWG, 0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink102/scan_003.log",
        label       = "e-link 102 (34 AWG, 0.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink104/scan_003.log",
        label       = "e-link 104 (34 AWG, 1.00 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink106/scan_003.log",
        label       = "e-link 106 (34 AWG, 1.60 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink111/scan_003.log",
        label       = "e-link 111 (34 AWG, 1.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink113/scan_003.log",
        label       = "e-link 113 (34 AWG, 2.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_006"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink183/scan_001.log",
        label       = "e-link 183 (36 AWG, 0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink187/scan_001.log",
        label       = "e-link 187 (36 AWG, 0.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink191/scan_001.log",
        label       = "e-link 191 (36 AWG, 1.00 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink195/scan_001.log",
        label       = "e-link 195 (36 AWG, 1.60 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink200/scan_001.log",
        label       = "e-link 200 (36 AWG, 2.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)

def main():
    analyzeScans()
    makeCombinedPlots()

if __name__ == "__main__":
    main()

