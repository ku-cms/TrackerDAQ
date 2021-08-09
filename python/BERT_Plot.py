# BERT_Plot.py

import matplotlib.pyplot as plt
import tools

def plot(plot_dir, output_file, x_values, y_values):
    useXKCDStyle = False
    tools.makeDir(plot_dir)
    if useXKCDStyle:
        plt.xkcd()
    fig, ax = plt.subplots(figsize=(6, 6))
    
    plt.plot(x_values, y_values, 'ro')

    ax.set_yscale('symlog')
    ax.set_title("BERT TAP0 Scan",              fontsize=20)
    ax.set_xlabel("TAP0 DAC",                   fontsize=16)
    ax.set_ylabel("Bit errors per 10 seconds",  fontsize=16)
    
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    plt.savefig(output_png)
    plt.savefig(output_pdf)
    
    # close to avoid memory warning 
    plt.close('all')

def plotMultiple(plot_dir, output_file, inputs, xlim, ylim):
    useXKCDStyle = False
    tools.makeDir(plot_dir)
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
        plt.plot(x_values, y_values, 'o', label=label, color=color)

    ax.set_yscale('symlog')
    ax.legend(loc='upper right')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title("BERT TAP0 Scan",              fontsize=20)
    ax.set_xlabel("TAP0 DAC",                   fontsize=16)
    ax.set_ylabel("Bit errors per 10 seconds",  fontsize=16)
    
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    plt.savefig(output_png)
    plt.savefig(output_pdf)
    
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

