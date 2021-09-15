# BERT_Plot.py

import matplotlib.pyplot as plt
import numpy as np
from tools import makeDir

def plot(plot_dir, output_file, x_values, y_values, x_label="TAP0 DAC", y_label="Bit errors per 10 seconds", setLogY=True, y_errors=[]):
    useXKCDStyle = False
    makeDir(plot_dir)
    if useXKCDStyle:
        plt.xkcd()
    fig, ax = plt.subplots(figsize=(6, 6))
    
    if y_errors:
        plt.errorbar(x_values, y_values, yerr=y_errors, fmt='ro')
    else:
        plt.plot(x_values, y_values, 'ro')

    if setLogY:
        ax.set_yscale('symlog')
    ax.set_title("BERT TAP0 Scan",  fontsize=20)
    ax.set_xlabel(x_label,          fontsize=16)
    ax.set_ylabel(y_label,          fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.tick_params(axis='both', which='minor', labelsize=8)
    
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    plt.savefig(output_png, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
    
    # close to avoid memory warning 
    plt.close('all')

def plotMultiple(plot_dir, output_file, inputs, xlim, ylim, x_label="TAP0 DAC", y_label="Bit errors per 10 seconds", setLogY=True, alpha=None, setBERY=False):
    useXKCDStyle = False
    makeDir(plot_dir)
    if useXKCDStyle:
        plt.xkcd()
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = [
                "xkcd:cherry red",
                "xkcd:apple green",
                "xkcd:bright blue",
                "xkcd:tangerine",
                "xkcd:electric purple",
                "xkcd:aqua blue",
                "xkcd:grass green",
                "xkcd:lilac",
                "xkcd:coral",
                "xkcd:fuchsia"
    ]
    
    for i, item in enumerate(inputs):
        x_values = item["x_values"]
        y_values = item["y_values"]
        label    = item["label"]
        color    = colors[i]
        x_values = np.array(x_values)
        y_values = np.array(y_values)
        if setBERY:
            # note: using this order of operations to fix floating point issue for 1e-11
            y_values = 1e-10 * y_values
            for i in range(len(y_values)):
                if y_values[i] == 0.0:
                    y_values[i] = 1e-11
        if "y_errors" in item:
            y_errors = item["y_errors"]
            plt.errorbar(x_values, y_values, yerr=y_errors, fmt='o', label=label, color=color, alpha=alpha)
        else:
            plt.plot(x_values, y_values, 'o', label=label, color=color, alpha=alpha)

    if setLogY:
        ax.set_yscale('symlog')
    if setBERY:
        ax.set_yscale('log')
    ax.legend(loc='upper right', prop={'size': 16})
    #ax.legend(loc='upper right', prop={'size': 12})
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title("BERT TAP0 Scan", fontsize=20)
    ax.set_xlabel(x_label,         fontsize=16)
    ax.set_ylabel(y_label,         fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    
    #plt.rcParams.update({'axes.labelsize': 'large'}) 
    
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    plt.savefig(output_png, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
    
    # close to avoid memory warning 
    plt.close('all')

def main():
    plot_dir    = "plots"
    output_file = "BERT_example"
    x_values = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    y_values = [179652, 9469, 192, 0, 0, 0, 0, 0, 0, 0, 0]
    plot(plot_dir, output_file, x_values, y_values)

if __name__ == "__main__":
    main()

