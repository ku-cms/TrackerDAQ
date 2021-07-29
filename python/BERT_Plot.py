# BERT_Plot.py

import matplotlib.pyplot as plt
import tools

def plot(plot_dir, output_file, x_values, y_values):
    tools.makeDir(plot_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    
    plt.plot(x_values, y_values, 'ro')

    ax.set_yscale('symlog')
    ax.set_title("BERT TAP0 Scan",          fontsize=20)
    ax.set_xlabel("TAP0 DAC Setting",       fontsize=16)
    ax.set_ylabel("Errors (over 10 s)",     fontsize=16)
    
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    plt.savefig(output_png)
    plt.savefig(output_pdf)

def plotMultiple(plot_dir, output_file, inputs):
    tools.makeDir(plot_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    
    for item in inputs:
        x_values = item["x_values"]
        y_values = item["y_values"]
        color    = item["color"]
        label    = item["label"]
        plt.plot(x_values, y_values, 'o', color=color, label=label)

    ax.set_yscale('symlog')
    ax.legend(loc='upper right')
    ax.set_xlim([49.0, 101.0])
    ax.set_ylim([0.0, 10.0**9])
    ax.set_title("BERT TAP0 Scan",          fontsize=20)
    ax.set_xlabel("TAP0 DAC Setting",       fontsize=16)
    ax.set_ylabel("Errors (over 10 s)",     fontsize=16)
    
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    plt.savefig(output_png)
    plt.savefig(output_pdf)

def main():
    plot_dir    = "plots"
    output_file = "BERT_example"
    x_values = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    y_values = [179652, 9469, 192, 0, 0, 0, 0, 0, 0, 0, 0]
    plot(plot_dir, output_file, x_values, y_values)

if __name__ == "__main__":
    main()

