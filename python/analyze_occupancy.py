# analyze_occupancy.py

import ROOT

def main():
    # Input ROOT file name
    input_file = "Results/Run000201_Physics.root"

    print(f"Running occupancy analysis on this input file: {input_file}")

    # Load ROOT file
    f = ROOT.TFile(input_file, "READ")
    
    # Check for errors when loading ROOT file
    if not f or f.IsZombie():
        print(f"ERROR: Unable to load this ROOT file: {input_file}")
        return
    
    # Load 2D occupancy histogram
    occ_2d_hist_name = "Detector/Board_0/OpticalGroup_0/Hybrid_0/Chip_15/D_B(0)_O(0)_H(0)_Occ2D_Chip(15)"
    occ_2d_hist = f.Get(occ_2d_hist_name)

    if not occ_2d_hist:
        print(f"ERROR: Unable to load this 2D histogram: {occ_2d_hist_name}")
        f.Close()
        return
    
    print(f"occ_2d_hist: {occ_2d_hist}")
    print(f"occ_2d_hist type: {type(occ_2d_hist)}")

    #n_bins_x = occ_2d_hist.GetNbinsX()
    #n_bins_y = occ_2d_hist.GetNbinsY()
    #print(f"n_bins_x: {n_bins_x}")
    #print(f"n_bins_y: {n_bins_y}")

    occ_2d_hist.Draw()

    user_input = input("Press enter to continue... ")

if __name__ == "__main__":
    main()
