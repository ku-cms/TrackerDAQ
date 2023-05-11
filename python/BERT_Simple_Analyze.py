# BERT_Analyze.py

import re
import os
import glob
import csv
import argparse
from BERT_Plot import plot
from tools import getBERTData, makeDir

# get cable number from directory name
def getNumber(name):
    # use try/except in case the directory name does not contain a number
    try:
        number = re.search(r'\d+', name).group()
        number = int(number)
    except:
        print("WARNING: No number found in the name '{0}'.".format(name))
        number = -1
    return number

# find min TAP0 for 0 errors from a scan
def findMin(x_values, y_values):
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

# analyze data from a scan
def analyze(input_file, plot_dir, output_file, useRD53B):
    debug = True
    data = getBERTData(input_file, useRD53B)
    x_values = data[0]
    y_values = data[1]
    if debug:
        print("x_values: {0}".format(x_values))
        print("y_values: {0}".format(y_values))
    # check for the same number of x and y values
    if len(x_values) != len(y_values):
        print("ERROR: number of x and y values do not match")
        print("input file: {0}, num x vals: {1}, num y vals: {2}".format(input_file, len(x_values), len(y_values)))
        return
    if debug:
        print("input file: {0}, num x vals: {1}, num y vals: {2}".format(input_file, len(x_values), len(y_values)))
    
    plot(plot_dir, output_file, x_values, y_values)
    #plot(plot_dir, output_file, x_values, y_values,setLogY=False)
    
    min_value = findMin(x_values, y_values)
    #print("Min TAP0: {0}".format(min_value))
    return min_value

# run over a single directory
def runDir(plot_dir, data_dir, table, data_name, useRD53B):
    # get list of input files in directory
    files = glob.glob(data_dir + "/scan_*.log")
    for input_file in files:
        # get output file name based on input file name
        name        = os.path.basename(input_file)
        x           = name.split(".")[0]
        output_file = "BERT_" + x
        min_value = analyze(input_file, plot_dir, output_file, useRD53B)
        table.append([data_name, x, min_value])
    # sort so that the latest file is last
    table.sort()

# run over directories in base directory
def runSet(base_plot_dir, base_data_dir, useRD53B, cable_number=-1, output_csv_dir="", output_csv_name=""):
    foundCable = False
    table = []
    print("Plotting data in {0}".format(base_data_dir))
    # get list of directories in base directory
    dirs = glob.glob(base_data_dir + "/*")
    # sort directories alphabetically
    dirs.sort()
    for data_dir in dirs:
        # get name for plot directory
        name = os.path.basename(data_dir)
        # get number from directory name
        number_from_name = getNumber(name)
        # compare number from directory name with cable number
        # run analysis over data in directory if cable number matches the number from the directory,
        # or if cable number is negative (for negative cable numbers, analyze all directories)
        if cable_number < 0 or cable_number == number_from_name:
            foundCable = True
            plot_dir = "{0}/{1}".format(base_plot_dir, name)
            # result is appended to table
            runDir(plot_dir, data_dir, table, name, useRD53B)
            # print all results in table for this cable
            for row in table:
                cable       = row[0]
                run         = row[1]
                min_value   = row[2]
                # check that first column (cable) matches this directory name (name) 
                if cable == name:
                    print(" - {0}, {1}: min value = {2}".format(cable, run, min_value))
            # print result for the latest scan, defined as last entry in sorted table
            #last_row    = table[-1]
            #run         = last_row[1]
            #min_value   = last_row[2]
            #print(" - {0}: Latest scan ({1}) for e-link {2}: min value = {3}".format(name, run, number_from_name, min_value))
    
    #print(table)
    
    # output min TAP0 values to a table
    if output_csv_dir and output_csv_name:
        makeDir(output_csv_dir)
        with open(output_csv_name, 'w', newline='') as output_csv:
            output_writer = csv.writer(output_csv)
            output_column_titles = ["cable", "run", "min_value"]
            output_writer.writerow(output_column_titles)
            # sort table alphabetically
            table.sort()
            for row in table:
                output_writer.writerow(row)
    if not foundCable:
        print("No data found for e-link {0}".format(cable_number))

# RD53A: make a plot for each scan
def analyzeScansRD53A(cable_number):
    useRD53B = False
    output_csv_dir   = "output"
    
    base_plot_dir    = "plots/BERT_TAP0_Scans/SingleDP"
    base_data_dir    = "data/BERT_TAP0_Scans/SingleDP"
    output_csv_name  = "output/BERT_Min_TAP0_Values_SingleDP.csv"
    
    #base_plot_dir    = "plots/BERT_TAP0_Scans/DoubleDP_DPAdapter"
    #base_data_dir    = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter"
    #output_csv_name  = "output/BERT_Min_TAP0_Values.csv"
    
    #base_plot_dir    = "plots/BERT_TAP0_Scans/KSU_FMC_DoubleDP_DPAdapter"
    #base_data_dir    = "data/BERT_TAP0_Scans/KSU_FMC_DoubleDP_DPAdapter"
    #output_csv_name  = "output/BERT_Min_TAP0_Values_KSU_FMC.csv"
   
    #base_plot_dir    = "plots/BERT_TAP0_Scans/CERN_FMC_DoubleDP_DPAdapter"
    #base_data_dir    = "data/BERT_TAP0_Scans/CERN_FMC_DoubleDP_DPAdapter"
    #output_csv_name  = "output/BERT_Min_TAP0_Values_CERN_FMC.csv"
   
    if cable_number < 0:
        # run for all cables
        runSet(base_plot_dir, base_data_dir, useRD53B, cable_number, output_csv_dir, output_csv_name)
    else:
        # run for a specific cable
        runSet(base_plot_dir, base_data_dir, useRD53B, cable_number)

# RD53B: make a plot for each scan
def analyzeScansRD53B(cable_number):
    useRD53B = True
    output_csv_dir   = "output"

    # using port card:
    base_plot_dir    = "plots/BERT_TAP0_Scans/CERN_FMC_PortCard"
    base_data_dir    = "data/BERT_TAP0_Scans/CERN_FMC_PortCard"
    output_csv_name  = "output/BERT_Min_TAP0_Values.csv"
    
    #base_plot_dir    = "plots/BERT_TAP0_Scans/SingleDP"
    #base_data_dir    = "data/BERT_TAP0_Scans/SingleDP"
    
    #base_plot_dir    = "plots/BERT_TAP0_Scans/DoubleDP_DPAdapter"
    #base_data_dir    = "data/BERT_TAP0_Scans/DoubleDP_DPAdapter"
    #output_csv_name  = "output/BERT_Min_TAP0_Values.csv"
    
    #base_plot_dir    = "plots/BERT_TAP0_Scans/ShortDoubleDP_DPAdapter"
    #base_data_dir    = "data/BERT_TAP0_Scans/ShortDoubleDP_DPAdapter"
    #output_csv_name  = "output/BERT_Min_TAP0_Values_ShortDoubleDP_DPAdapter.csv"
    
    #base_plot_dir    = "plots/BERT_TAP0_Scans/ShortDP"
    #base_data_dir    = "data/BERT_TAP0_Scans/ShortDP"
    #output_csv_name  = "output/BERT_Min_TAP0_Values_ShortDP.csv"
    
    if cable_number < 0:
        # run for all cables
        runSet(base_plot_dir, base_data_dir, useRD53B, cable_number, output_csv_dir, output_csv_name)
    else:
        # run for a specific cable
        runSet(base_plot_dir, base_data_dir, useRD53B, cable_number)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--cable_number",  "-n",  default=-1,       help="Cable number to analyze a specific cable; to run over all cables, use default (-1).")
    parser.add_argument("--rd53_b",        "-b",  default=False,    action='store_true',    help="Analyze RD53B data (default False).")
    
    options      = parser.parse_args()
    cable_number = int(options.cable_number)
    rd53_b       = options.rd53_b
    
    if rd53_b:
        analyzeScansRD53B(cable_number)
    else:
        analyzeScansRD53A(cable_number)

if __name__ == "__main__":
    main()

