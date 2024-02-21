void analyze_occupancy()
{
    // Input ROOT file name
    // string input_file = "example_file.root";
    string input_file = "Results/Run000201_Physics.root";
    
    cout << "Running occupancy analysis on this input file: " << input_file << endl;
    
    // Load ROOT file
    TFile *f = new TFile(input_file.c_str(), "READ");

    // Check for errors when loading ROOT file
    if (!f || f->IsZombie())
    {
        cerr << "ERROR: Unable to load this ROOT file: " << input_file << endl;
        return;
    }
    
    // Load 2D occupancy canvas
    // string occ_2d_canvas_name = "example_canvas";
    string occ_2d_canvas_name = "Detector/Board_0/OpticalGroup_0/Hybrid_0/Chip_15/D_B(0)_O(0)_H(0)_Occ2D_Chip(15)";
    TCanvas *occ_2d_canvas = (TCanvas*)f->Get(occ_2d_canvas_name.c_str());

    // Check for errors when loading canvas
    if (!occ_2d_canvas)
    {
        cerr << "ERROR: Unable to load this canvas: " << occ_2d_canvas_name << endl;
        f->Close();
        return;
    }

    cout << "occ_2d_canvas: " << occ_2d_canvas << endl;
    cout << "occ_2d_canvas type: " << typeid(occ_2d_canvas).name() << endl;

    // Int_t n_bins_x = occ_2d_hist->GetNbinsX();
    // Int_t n_bins_y = occ_2d_hist->GetNbinsY();
    // cout << "n_bins_x: " << n_bins_x << endl;
    // cout << "n_bins_y: " << n_bins_y << endl;

    // Draw canvas
    occ_2d_canvas->Draw();
}