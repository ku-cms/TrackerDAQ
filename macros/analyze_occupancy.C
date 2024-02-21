void analyze_occupancy()
{
    // Input ROOT file name
    //string input_file = "example_file.root";
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
    
    // Load 2D occupancy histogram
    //string occ_2d_hist_name = "example_histogram";
    string occ_2d_hist_name = "Detector/Board_0/OpticalGroup_0/Hybrid_0/Chip_15/D_B(0)_O(0)_H(0)_Occ2D_Chip(15)";
    TH2F *occ_2d_hist = (TH2F*) f->Get(occ_2d_hist_name.c_str());

    // Check for errors when loading histogram
    if (!occ_2d_hist)
    {
        cerr << "ERROR: Unable to load this 2D histogram: " << occ_2d_hist_name << endl;
        f->Close();
        return;
    }

    cout << "occ_2d_hist: " << occ_2d_hist << endl;
    cout << "occ_2d_hist type: " << typeid(occ_2d_hist).name() << endl;

    Int_t n_bins_x = occ_2d_hist->GetNbinsX();
    Int_t n_bins_y = occ_2d_hist->GetNbinsY();
    cout << "n_bins_x: " << n_bins_x << endl;
    cout << "n_bins_y: " << n_bins_y << endl;
    //occ_2d_hist->Draw();
}