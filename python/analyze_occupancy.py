# analyze_occupancy.py

import ROOT

def main():
    # Input ROOT file name
    # input_file = "example_file.root"
    input_file = "Results/Run000201_Physics.root"

    print(f"Running occupancy analysis on this input file: {input_file}")

    # Load ROOT file
    f = ROOT.TFile(input_file, "READ")
    
    # Check for errors when loading ROOT file
    if not f or f.IsZombie():
        print(f"ERROR: Unable to load this ROOT file: {input_file}")
        return
    
    # Load 2D occupancy canvas
    # occ_2d_canvas_name = "example_canvas"
    occ_2d_canvas_name = "Detector/Board_0/OpticalGroup_0/Hybrid_0/Chip_15/D_B(0)_O(0)_H(0)_Occ2D_Chip(15)"
    occ_2d_canvas = f.Get(occ_2d_canvas_name)

    # Check for errors when loading canvas
    if not occ_2d_canvas:
        print(f"ERROR: Unable to load this canvas: {occ_2d_canvas_name}")
        f.Close()
        return
    
    print(f"occ_2d_canvas: {occ_2d_canvas}")
    print(f"occ_2d_canvas type: {type(occ_2d_canvas)}")

    # n_bins_x = occ_2d_hist.GetNbinsX()
    # n_bins_y = occ_2d_hist.GetNbinsY()
    # print(f"n_bins_x: {n_bins_x}")
    # print(f"n_bins_y: {n_bins_y}")

    # Draw canvas
    occ_2d_canvas.Draw()

    # Ask for user input to prevent python from exiting immediately
    user_input = input("Press enter to continue... ")

if __name__ == "__main__":
    main()
