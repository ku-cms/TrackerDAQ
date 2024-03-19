# analyze_occupancy.py

import ROOT

def main():
    # Input ROOT file name
    # input_file = "example_file.root"
    input_file = "Results/Run000211_Physics.root"

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
    
    # Get list of primitives from canvas
    primitives = list(occ_2d_canvas.GetListOfPrimitives())
    
    print("Canvas:")
    print(f" - occ_2d_canvas: {occ_2d_canvas}")
    print(f" - occ_2d_canvas type: {type(occ_2d_canvas)}")
    print(f" - primitives: {primitives}")
    
    # Print primitives
    print("Primitives:")
    for object in primitives:
        print(f" - {type(object)}: {object}")

    # Load 2D occupancy histogram
    # occ_2d_hist_name = "example_histogram"
    occ_2d_hist_name = "D_B(0)_O(0)_H(0)_Occ2D_Chip(15)"
    occ_2d_hist = occ_2d_canvas.GetPrimitive(occ_2d_hist_name)

    # Check for errors when loading histogram
    if not occ_2d_hist:
        print(f"ERROR: Unable to load this histogram: {occ_2d_hist_name}")
        f.Close()
        return
    
    # Get number of bins (x, y) for 2D histogram
    n_bins_x = occ_2d_hist.GetNbinsX()
    n_bins_y = occ_2d_hist.GetNbinsY()
    n_bins_total = n_bins_x * n_bins_y
    
    print("Histogram:")
    print(f" - occ_2d_hist: {occ_2d_hist}")
    print(f" - occ_2d_hist type: {type(occ_2d_hist)}")
    print(f" - n_bins_x: {n_bins_x}")
    print(f" - n_bins_y: {n_bins_y}")
    print(f" - n_bins_total: {n_bins_total}")

    # Draw canvas
    occ_2d_canvas.Draw()

    # Ask for user input to prevent python from exiting immediately
    user_input = input("Press enter to continue... ")

if __name__ == "__main__":
    main()
