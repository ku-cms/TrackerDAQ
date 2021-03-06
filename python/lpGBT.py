# lpGBT.py

import ROOT
from tools import makeDir

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def plot(input_file, plot_dir):
    makeDir(plot_dir)
    print("input file: {0}".format(input_file))
    f = ROOT.TFile(input_file, "read")
    h = f.Get("EOM Scan")

    # Plot
    c = ROOT.TCanvas("c", "c", 2000, 1000)
    pad = c.cd()
    pad.SetLeftMargin(0.10)
    pad.SetRightMargin(0.20)
    pad.SetTopMargin(0.10)
    pad.SetBottomMargin(0.15)

    # Format
    label_size = 0.05
    title_size = 0.05
    x_axis = h.GetXaxis()
    y_axis = h.GetYaxis()
    z_axis = h.GetZaxis()
    x_axis.SetTitle("Phase DAC")
    y_axis.SetTitle("Voltage DAC")
    z_axis.SetTitle("Transitions")
    x_axis.SetLabelSize(label_size)
    y_axis.SetLabelSize(label_size)
    z_axis.SetLabelSize(label_size)
    x_axis.SetTitleSize(title_size)
    y_axis.SetTitleSize(title_size)
    z_axis.SetTitleSize(title_size)
    x_axis.SetTitleOffset(1.1)
    y_axis.SetTitleOffset(0.8)
    z_axis.SetTitleOffset(1.2)
    
    h.SetStats(ROOT.kFALSE)
    h.SetTitle("Eye Opening Monitor")
    
    h.Draw()
    name = plot_dir + "/lpGBT_eye.pdf"
    c.SaveAs(name)

def main():
    input_file = "data/lpGBT/Rice_EOMScan1505.root"
    plot_dir = "plots/lpGBT"
    plot(input_file, plot_dir)

if __name__ == "__main__":
    main()

