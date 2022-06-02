# BERT_Analyze.py

import os
import glob
import csv
from BERT_Plot import plot, plotMultiple
from tools import getBERTData, makeDir

# find min TAP0 for 0 errors from a scan
def findMin_v1(x_values, y_values):
    n = len(x_values)
    # search data starting with the last point
    # iterate over list backwards
    for i in range(n-1, -1, -1):
        if y_values[i] > 0:
            if i < n - 1:
                # found min TAP0
                return x_values[i + 1]
            else:
                # did not find min TAP0
                return -1
    # did not find min TAP0
    return -1

# find min TAP0 for 0 errors from a scan
def findMin_v2(x_values, y_values):
    # search data starting with the last point
    # iterate over list backwards
    result = -1
    search = True
    n = len(x_values)
    i = n - 1
    while search:
        if i < 0:
            break
        if y_values[i] > 0:
            if i < n - 1:
                # found min TAP0
                result = x_values[i + 1]
                search = False
            else:
                # did not find min TAP0
                result = -1
                search = False
        i -= 1
    return result

# analyze data from a scan
def analyze(input_file, plot_dir, output_file):
    debug = False
    data = getBERTData(input_file)
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
    min_value = findMin_v1(x_values, y_values)
    #print("Min TAP0: {0}".format(min_value))
    return min_value

# run over a single directory
def runDir(plot_dir, data_dir, table, data_name):
    # get list of input files in directory
    files = glob.glob(data_dir + "/scan_*.log")
    for input_file in files:
        # get output file name based on input file name
        name        = os.path.basename(input_file)
        x           = name.split(".")[0]
        output_file = "BERT_" + x
        min_value = analyze(input_file, plot_dir, output_file)
        table.append([data_name, x, min_value])

# run over directories in base directory
def runSet(base_plot_dir, base_data_dir, output_csv_dir="", output_csv_name=""):
    table = []
    print("Plotting data in {0}".format(base_data_dir))
    # get list of directories in base directory
    dirs = glob.glob(base_data_dir + "/*")
    # sort directories alphabetically
    dirs.sort()
    for data_dir in dirs:
        # get name for plot directory
        name = os.path.basename(data_dir)
        plot_dir = "{0}/{1}".format(base_plot_dir, name)
        print(" - {0}".format(name))
        runDir(plot_dir, data_dir, table, name)
    # sort table alphabetically
    table.sort()
    # output min TAP0 values to a table
    if output_csv_dir and output_csv_name:
        makeDir(output_csv_dir)
        with open(output_csv_name, 'w', newline='') as output_csv:
            output_writer = csv.writer(output_csv)
            output_column_titles = ["cable", "run", "min_value"]
            output_writer.writerow(output_column_titles)
            for row in table:
                output_writer.writerow(row)

# make a plot for each scan
def analyzeScans():
    #plot_dir    = "plots/BERT_Scan_SingleDP_Data"
    #data_dir    = "data/BERT_Scan_SingleDP_Data"
    #runDir(plot_dir, data_dir)
    #
    #plot_dir    = "plots/BERT_Scan_DoubleDP_DoubleBonn_Data"
    #data_dir    = "data/BERT_Scan_DoubleDP_DoubleBonn_Data"
    #runDir(plot_dir, data_dir)
    #
    #base_plot_dir    = "plots/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow"
    #base_data_dir    = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow"
    #runSet(base_plot_dir, base_data_dir)
    
    base_plot_dir    = "plots/BERT_TAP0_Scans/DoubleDP_DPAdapter"
    base_data_dir    = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter"
    output_csv_dir   = "output"
    output_csv_name  = "output/BERT_Min_TAP0_Values.csv"
    runSet(base_plot_dir, base_data_dir, output_csv_dir, output_csv_name)

    #base_plot_dir    = "plots/BERT_TAP0_Scans/DoubleDP_DPAdapter_ErnieCrossTalk"
    #base_data_dir    = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter_ErnieCrossTalk"
    #runSet(base_plot_dir, base_data_dir)
    #
    #base_plot_dir    = "plots/BERT_Scan_Compare_SCC"
    #base_data_dir    = "data/BERT_Scan_Compare_SCC"
    #runSet(base_plot_dir, base_data_dir)
    
    base_plot_dir    = "plots/BERT_TAP0_Scans/SCC173_UnlashedElinks/0mm_Spacing"
    base_data_dir    = "data/BERT_TAP0_Scans/SCC173_UnlashedElinks/0mm_Spacing"
    runSet(base_plot_dir, base_data_dir)
    
    base_plot_dir    = "plots/BERT_TAP0_Scans/SCC173_UnlashedElinks/1mm_Spacing"
    base_data_dir    = "data/BERT_TAP0_Scans/SCC173_UnlashedElinks/1mm_Spacing"
    runSet(base_plot_dir, base_data_dir)
    
    base_plot_dir    = "plots/BERT_TAP0_Scans/SCC173_UnlashedElinks/2mm_Spacing"
    base_data_dir    = "data/BERT_TAP0_Scans/SCC173_UnlashedElinks/2mm_Spacing"
    runSet(base_plot_dir, base_data_dir)

# add entry to list of inputs
# each entry is a dictionary
def addEntry(input_list, input_file, label):
    data = getBERTData(input_file)
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
    # Description:
    # compare readout chain setups
    # flex cables using new power supply, others using old power supply
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
    # Description:
    # flex cables, new power supply
    # Bonn boards and yellow boards 
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
    # Description:
    # Type 1B elinks, old power supply
    # Bonn boards and yellow boards 
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
    # Description:
    # Type 1B elinks, old power supply
    # Bonn boards and yellow boards 
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
    # Description:
    # Type 1B elinks, new power supply
    # Bonn boards and yellow boards 
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
    # Description:
    # Type 1B elinks, new power supply
    # DP to Type 1 elink adapter board
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_006"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink101/scan_001.log",
        label       = "e-link 101 (34 AWG, 0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink102/scan_001.log",
        label       = "e-link 102 (34 AWG, 0.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink104/scan_001.log",
        label       = "e-link 104 (34 AWG, 1.00 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink106/scan_001.log",
        label       = "e-link 106 (34 AWG, 1.60 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink111/scan_002.log",
        label       = "e-link 111 (34 AWG, 1.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink113/scan_001.log",
        label       = "e-link 113 (34 AWG, 2.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # Type 1A elinks, new power supply
    # Bonn boards and yellow boards 
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_007"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink136/scan_001.log",
        label       = "e-link 136 (36 AWG, 0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink140/scan_001.log",
        label       = "e-link 140 (36 AWG, 0.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink145/scan_001.log",
        label       = "e-link 145 (36 AWG, 1.00 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink149/scan_001.log",
        label       = "e-link 149 (36 AWG, 1.40 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink154/scan_001.log",
        label       = "e-link 154 (36 AWG, 1.60 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink172/scan_001.log",
        label       = "e-link 172 (36 AWG, 1.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink178/scan_001.log",
        label       = "e-link 178 (36 AWG, 2.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # Type 1A elinks, new power supply
    # DP to Type 1 elink adapter board
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_008"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink136/scan_001.log",
        label       = "e-link 136 (36 AWG, 0.35 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink140/scan_001.log",
        label       = "e-link 140 (36 AWG, 0.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink145/scan_001.log",
        label       = "e-link 145 (36 AWG, 1.00 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink149/scan_001.log",
        label       = "e-link 149 (36 AWG, 1.40 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154/scan_001.log",
        label       = "e-link 154 (36 AWG, 1.60 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink172/scan_001.log",
        label       = "e-link 172 (36 AWG, 1.80 m)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink178/scan_001.log",
        label       = "e-link 178 (36 AWG, 2.00 m)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # Type 2 elinks, new power supply
    # Bonn boards and yellow boards 
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_009"
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
    
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 149 (36 AWG, 1.40 m)
    # Type 1A elinks, new power supply
    # DP to Type 1 elink adapter board
    # External cross talk: wind cable with another secondary 1.4m 36 AWG cable on Ernie board
    # Change amplitude voltage for signals on secondary cable
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_010"
    xlim = [40.0, 210.0]
    #ylim = [0.0, 1.0e13]
    ylim = [1.0e-11, 1.0e3]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter_ErnieCrossTalk/elink149_OFF/scan_001.log",
        label       = "Aggressor amplitude: OFF",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter_ErnieCrossTalk/elink149_269mV/scan_001.log",
        label       = "Aggressor amplitude: 269 mV",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter_ErnieCrossTalk/elink149_741mV/scan_001.log",
        label       = "Aggressor amplitude: 741 mV",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter_ErnieCrossTalk/elink149_1119mV/scan_001.log",
        label       = "Aggressor amplitude: 1119 mV",
    )
    #plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim, y_label="Bit Error Rate", setLogY=False, setBERY=True)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 206 (36 AWG, 1.40 m)
    # Type 0 elink (33 pin to 33 pin)
    # DP to Type 0 adapter board
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_011"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink206/scan_001.log",
        label       = "Single adapter",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink206/scan_002.log",
        label       = "Two adapters",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink206/scan_004.log",
        label       = "Two adapters and 2mm spacing",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 205 (36 AWG, 1.40 m)
    # Type 0 elink (33 pin to 33 pin)
    # DP to Type 0 adapter board
    # SCC 173
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_012"
    xlim = [90.0, 310.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/scc173_elink205/scan_008.log",
        label       = "SCC 173: Run 1",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/scc173_elink205/scan_009.log",
        label       = "SCC 173: Run 2",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/scc173_elink205/scan_010.log",
        label       = "SCC 173: Run 3",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 205 (36 AWG, 1.40 m)
    # Type 0 elink (33 pin to 33 pin)
    # DP to Type 0 adapter board
    # SCC 212
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_013"
    xlim = [90.0, 310.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/scc212_elink205/scan_005.log",
        label       = "SCC 212: Run 1",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/scc212_elink205/scan_006.log",
        label       = "SCC 212: Run 2",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/scc212_elink205/scan_007.log",
        label       = "SCC 212: Run 3",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 205 (36 AWG, 1.40 m)
    # Type 0 elink (33 pin to 33 pin)
    # DP to Type 0 adapter board
    # SCC from CERN
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_014"
    xlim = [90.0, 310.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/sccCERN_elink205/scan_004.log",
        label       = "SCC from CERN: Run 1",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/sccCERN_elink205/scan_005.log",
        label       = "SCC from CERN: Run 2",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_Scan_Compare_SCC/sccCERN_elink205/scan_006.log",
        label       = "SCC from CERN: Run 3",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # Type 1 e-links (36 AWG, 1.40 m)
    # DP to Type 1 elink adapter board
    # SCC 173
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_015"
    xlim = [90.0, 310.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink149/scan_002.log",
        label       = "e-link 149",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink150/scan_001.log",
        label       = "e-link 150",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink151/scan_001.log",
        label       = "e-link 151",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink153/scan_001.log",
        label       = "e-link 153",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 137 (36 AWG, 0.35 m)
    # DP to Type 1 elink adapter boards: Rev. B and Rev. C.2
    # SCC 173
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_016"
    xlim = [40.0, 210.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink137/scan_006.log",
        label       = "Adapter Rev. B",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink137/scan_004.log",
        label       = "Adapter Rev. C.2 (swap side)",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink137/scan_007.log",
        label       = "Adapter Rev. C.2 (SMA side)",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 207 (36 AWG, 1.4 m)
    # 0 mm spacing
    # DP to Type 1 elink adapter board
    # SCC 173
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_017"
    xlim = [90.0, 310.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink207_0mm_SS0/scan_001.log",
        label       = "207: 0mm, Clock",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink207_0mm_SS1/scan_001.log",
        label       = "207: 0mm, Aurora",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink207_0mm_SS2/scan_001.log",
        label       = "207: 0mm, PRBS",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink207_0mm_SS3/scan_001.log",
        label       = "207: 0mm, Ground",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    # ---------------------------- #
    # --- create combined plot --- #
    # ---------------------------- #
    # Description:
    # e-link 154 (36 AWG, 1.6 m)
    # DP to Type 1 elink adapter board
    # SCC 173
    plot_dir    = "plots/BERT_Scans"
    output_file = "BERT_Scans_018"
    xlim = [90.0, 310.0]
    ylim = [0.0, 1.0e13]
    inputs = []
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS0/scan_001.log",
        label       = "154, Clock",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS1/scan_001.log",
        label       = "154, Aurora",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS2/scan_001.log",
        label       = "154, PRBS",
    )
    addEntry(
        input_list  = inputs,
        input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS3/scan_001.log",
        label       = "154, Ground",
    )
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)
    
def crossTalkPlot(cable_number, custom_files={}):
    signal_map = {
        0 : "Clock",
        1 : "Aurora",
        2 : "PRBS",
        3 : "Ground",
    }
    plot_dir    = "plots/BERT_Scan_SCC_Crosstalk"
    output_file = "elink{0}".format(cable_number)
    xlim = [90.0, 310.0]
    ylim = [0.0, 1.0e13]
    inputs = []

    # use custom file paths
    if custom_files:
        for i in range(4):
            addEntry(
                input_list  = inputs,
                input_file  = custom_files[i],
                label       = "{0}, {1}".format(cable_number, signal_map[i]),
            )
    # use default file paths
    else:
        for i in range(4):
            addEntry(
                input_list  = inputs,
                input_file  = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink{0}_SS{1}/scan_001.log".format(cable_number, i),
                label       = "{0}, {1}".format(cable_number, signal_map[i]),
            )
    
    plotMultiple(plot_dir, output_file, inputs, xlim, ylim)

def makeCrossTalkPlots():
    
    custom_files_elink153 = {
        0 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink153_SS0/scan_001.log",
        1 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink153_SS1/scan_001.log",
        2 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink153_SS2_v2/scan_001.log",
        3 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink153_SS3/scan_001.log",
    }
    custom_files_elink154 = {
        0 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS0_v2/scan_001.log",
        1 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS1/scan_001.log",
        2 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS2_v2/scan_001.log",
        3 : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154_SS3/scan_001.log",
    }
    crossTalkPlot(144)
    crossTalkPlot(153, custom_files_elink153)
    crossTalkPlot(154, custom_files_elink154)

def comparisonPlot(cable_map, plot_dir, xlim, ylim):
    for cable in cable_map:
        inputs = []
        output_file = cable_map[cable]["output_file"]
        addEntry(
            input_list  = inputs,
            input_file  = cable_map[cable]["input_file_1"],
            label       = cable_map[cable]["label_1"],
        )
        addEntry(
            input_list  = inputs,
            input_file  = cable_map[cable]["input_file_2"],
            label       = cable_map[cable]["label_2"],
        )
        plotMultiple(plot_dir, output_file, inputs, xlim, ylim)

def makeComparisonPlots():
    plot_dir    = "plots/BERT_Scan_Comparison"
    xlim = [40.0, 610.0]
    ylim = [0.0, 1.0e13]
    cable_map = {
        101 : {
            "output_file"   : "BERT_Scans_elink101",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink101/scan_005.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink101/scan_001.log",
            "label_1"       : "e-link 101 (34 AWG, 0.35 m) Setup 1",
            "label_2"       : "e-link 101 (34 AWG, 0.35 m) Setup 2",
        },
        102 : {
            "output_file"   : "BERT_Scans_elink102",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink102/scan_003.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink102/scan_001.log",
            "label_1"       : "e-link 102 (34 AWG, 0.80 m) Setup 1",
            "label_2"       : "e-link 102 (34 AWG, 0.80 m) Setup 2",
        },
        104 : {
            "output_file"   : "BERT_Scans_elink104",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink104/scan_003.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink104/scan_001.log",
            "label_1"       : "e-link 104 (34 AWG, 1.00 m) Setup 1",
            "label_2"       : "e-link 104 (34 AWG, 1.00 m) Setup 2",
        },
        106 : {
            "output_file"   : "BERT_Scans_elink106",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink106/scan_003.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink106/scan_001.log",
            "label_1"       : "e-link 106 (34 AWG, 1.60 m) Setup 1",
            "label_2"       : "e-link 106 (34 AWG, 1.60 m) Setup 2",
        },
        111 : {
            "output_file"   : "BERT_Scans_elink111",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink111/scan_003.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink111/scan_002.log",
            "label_1"       : "e-link 111 (34 AWG, 1.80 m) Setup 1",
            "label_2"       : "e-link 111 (34 AWG, 1.80 m) Setup 2",
        },
        113 : {
            "output_file"   : "BERT_Scans_elink113",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink113/scan_003.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink113/scan_001.log",
            "label_1"       : "e-link 113 (34 AWG, 2.00 m) Setup 1",
            "label_2"       : "e-link 113 (34 AWG, 2.00 m) Setup 2",
        },
    }
    comparisonPlot(cable_map, plot_dir, xlim, ylim)
    cable_map = {
        136 : {
            "output_file"   : "BERT_Scans_elink136",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink136/scan_001.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink136/scan_001.log",
            "label_1"       : "e-link 136 (36 AWG, 0.35 m) Setup 1",
            "label_2"       : "e-link 136 (36 AWG, 0.35 m) Setup 2",
        },
        140 : {
            "output_file"   : "BERT_Scans_elink140",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink140/scan_001.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink140/scan_001.log",
            "label_1"       : "e-link 140 (36 AWG, 0.80 m) Setup 1",
            "label_2"       : "e-link 140 (36 AWG, 0.80 m) Setup 2",
        },
        145 : {
            "output_file"   : "BERT_Scans_elink145",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink145/scan_001.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink145/scan_001.log",
            "label_1"       : "e-link 145 (36 AWG, 1.00 m) Setup 1",
            "label_2"       : "e-link 145 (36 AWG, 1.00 m) Setup 2",
        },
        149 : {
            "output_file"   : "BERT_Scans_elink149",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink149/scan_001.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink149/scan_001.log",
            "label_1"       : "e-link 149 (36 AWG, 1.40 m) Setup 1",
            "label_2"       : "e-link 149 (36 AWG, 1.40 m) Setup 2",
        },
        154 : {
            "output_file"   : "BERT_Scans_elink154",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink154/scan_001.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink154/scan_001.log",
            "label_1"       : "e-link 154 (36 AWG, 1.60 m) Setup 1",
            "label_2"       : "e-link 154 (36 AWG, 1.60 m) Setup 2",
        },
        172 : {
            "output_file"   : "BERT_Scans_elink172",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink172/scan_001.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink172/scan_001.log",
            "label_1"       : "e-link 172 (36 AWG, 1.80 m) Setup 1",
            "label_2"       : "e-link 172 (36 AWG, 1.80 m) Setup 2",
        },
        178 : {
            "output_file"   : "BERT_Scans_elink178",
            "input_file_1"  : "data/BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink178/scan_001.log",
            "input_file_2"  : "data/BERT_TAP0_Scans/DoubleDP_DPAdapter/elink178/scan_001.log",
            "label_1"       : "e-link 178 (36 AWG, 2.00 m) Setup 1",
            "label_2"       : "e-link 178 (36 AWG, 2.00 m) Setup 2",
        },
    }
    comparisonPlot(cable_map, plot_dir, xlim, ylim)
    xlim = [40.0, 310.0]
    ylim = [0.0, 1.0e13]
    cable_map = {
        151 : {
            "output_file"   : "BERT_Scans_elink151",
            "input_file_1"  : "data/BERT_Scan_Compare_SCC/scc173_elink151/scan_001.log",
            "input_file_2"  : "data/BERT_Scan_Compare_SCC/scc212_elink151/scan_002.log",
            "label_1"       : "e-link 151 (36 AWG, 1.4 m) SCC 173",
            "label_2"       : "e-link 151 (36 AWG, 1.4 m) SCC 212",
        },
    }
    comparisonPlot(cable_map, plot_dir, xlim, ylim)
    xlim = [49.0, 71.0]
    ylim = [0.0, 1.0e6]
    cable_map = {
        "SingleDP" : {
            "output_file"   : "BERT_Scans_SingleDP",
            "input_file_1"  : "data/BERT_Scan_Compare_SCC/scc173_SingleDP/scan_001.log",
            "input_file_2"  : "data/BERT_Scan_Compare_SCC/scc212_SingleDP/scan_001.log",
            "label_1"       : "Single DP SCC 173",
            "label_2"       : "Single DP SCC 212",
        },
    }
    comparisonPlot(cable_map, plot_dir, xlim, ylim)

def main():
    analyzeScans()
    makeCombinedPlots()
    makeComparisonPlots()
    makeCrossTalkPlots()

if __name__ == "__main__":
    main()

