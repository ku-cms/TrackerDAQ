# BERT_Plot.py

import matplotlib.pyplot as plt
import tools

def plot(plot_dir, output_file):
    tools.makeDir(plot_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    
    plt.plot([50, 60, 70, 80, 90, 100], [10**6, 10**4, 10**2, 0, 0, 0], 'ro')

    ax.set_yscale('symlog')
    ax.set_title("BERT Scan",   fontsize=20)
    ax.set_xlabel("TAP0",       fontsize=16)
    ax.set_ylabel("Errors",     fontsize=16)
    
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    plt.savefig(output_png)
    plt.savefig(output_pdf)

def main():
    plot_dir    = "plots"
    output_file = "BERT_example"
    plot(plot_dir, output_file)

if __name__ == "__main__":
    main()

