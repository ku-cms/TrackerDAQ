# CompareRD53AB.py 

import tools
import csv
import numpy as np
import matplotlib.pyplot as plt

# get lengths
def getLengths(data, length_col):
    lengths = []
    for i, row in enumerate(data):
        # skip first row (headers)
        if i == 0:
            continue
        length = float(row[length_col])
        if length not in lengths:
            lengths.append(length)
    lengths.sort()
    return lengths

def getAvgData(data, lengths, length_col, data_col):
    avg_data = []
    for length in lengths:
        vals = []
        for i, row in enumerate(data):
            # skip first row (headers)
            if i == 0:
                continue
            this_length = float(row[length_col])
            if this_length == length:
                val = float(row[data_col])
                vals.append(val)
        avg = np.mean(vals)
        avg_data.append(avg)
    return avg_data

def plot(datasets, output_name, title, x_label, y_label, xlim, ylim):
    fig, ax = plt.subplots(figsize=(6, 6))
    for dataset in datasets:
        name    = dataset["name"]
        x_vals  = dataset["x_vals"]
        y_vals  = dataset["y_vals"]
        print("name: {0}".format(name))
        print("x_vals: {0}".format(x_vals))
        print("y_vals: {0}".format(y_vals))
        plt.plot(x_vals, y_vals, 'o', label=name, alpha=0.75)

    
    legend_font_size = 12
    ax.legend(loc='upper left', prop={'size': legend_font_size})
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title,     fontsize=20)
    ax.set_xlabel(x_label,  fontsize=16)
    ax.set_ylabel(y_label,  fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    
    output_png = "{0}.png".format(output_name)
    output_pdf = "{0}.pdf".format(output_name)
    
    plt.savefig(output_png, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
    
    # close to avoid memory warning 
    plt.close('all')


def run(input_csv, output_name):
    data = tools.readCSV(input_csv)
    #for row in data: 
    #    print(row)
    length_col  = 1
    data_cols   = [3, 4, 5, 6]
    lengths = getLengths(data, length_col)
    #print(lengths)
    datasets = []
    for data_col in data_cols:
        name = data[0][data_col]
        avg_data = getAvgData(data, lengths, length_col, data_col)
        #print(name)
        #print(avg_data)
        data_map = {}
        data_map["name"]    = name
        data_map["x_vals"]  = lengths
        data_map["y_vals"]  = avg_data
        datasets.append(data_map)
    title   = "Error rate comparison"
    x_label = "e-link length (m)"
    y_label = "TAP0 for BER=1e-10"
    xlim    = [0.0, 2.0]
    ylim    = [0.0, 800.0]
    plot(datasets, output_name, title, x_label, y_label, xlim, ylim)

def main():
    input_csv   = "CompareRD53AB/BERT_TAP0_Scan_Comparison_v1.csv"
    output_name = "CompareRD53AB/Comparison_v1"
    run(input_csv, output_name)

if __name__ == "__main__":
    main()

