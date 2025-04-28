import ROOT
import sys
from array import array

file = ROOT.TFile("outputnew.root", "READ")

histograms = [
    "h_muon_pt", "h_muon_eta", "h_muon_phi", "h_muon_energy", 
    "h_muon_mass", "h_muon_leading", "h_muon_subleading", 
    "h_Z_pt", "h_Z_eta", "h_Z_phi", "h_Z_energy", "h_Z_mass", "h_Z_mass_eq", "h_Z_mass_fine"
]

ROOT.gStyle.SetOptStat(0)

z_mass_bin_edges = [40,45,50,55,60,64,68,72,76,81,86,91,96,101,106,110,115,120,126,133,141,150,160,171,185,200,220,243,273,320,380,440,510,600,700,830,1000]
n_bins_z_mass = len(z_mass_bin_edges) - 1

for hist_name in histograms:
    hist = file.Get(hist_name)

    hist.SetLineWidth(2)
    hist.SetLineColor(ROOT.kBlue)

    canvas = ROOT.TCanvas(f"c_{hist_name}", f"{hist_name} Canvas", 800, 600)

    if hist_name == "h_muon_pt":
        hist.SetXTitle("p_{T#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Muon transverse momentum")

    elif hist_name == "h_muon_eta":
        hist.SetXTitle("#eta_{#mu}")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Muon pseudorapidity")

    elif hist_name == "h_muon_phi":
        hist.SetXTitle("#phi_{#mu}")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Muon azimuthal angle")

    elif hist_name == "h_muon_energy":
        hist.SetXTitle("E_{#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Muon energy")

    elif hist_name == "h_muon_mass":
        hist.SetXTitle("M_{#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Muon mass")

    elif hist_name == "h_muon_leading":
        hist.SetXTitle("p_{T#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Leading muon transverse momentum")

    elif hist_name == "h_muon_subleading":
        hist.SetXTitle("p_{T#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Subleading muon transverse momentum")

    elif hist_name == "h_Z_pt":
        hist.SetXTitle("p_{T#mu#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Z boson transverse momentum")

    elif hist_name == "h_Z_eta":
        hist.SetXTitle("#eta_{#mu#mu}")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Z boson pseudorapidity")

    elif hist_name == "h_Z_phi":
        hist.SetXTitle("#phi_{#mu#mu}")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Z boson azimuthal angle")

    elif hist_name == "h_Z_energy":
        hist.SetXTitle("E_{#mu#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetMinimum(1)
        hist.SetTitle("Z boson energy")

    elif hist_name == "h_Z_mass":
        hist.SetXTitle("M_{#mu#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        canvas.SetLogx()
        hist.SetMinimum(1)
        hist.SetTitle("Z boson mass")
        h_Z_mass_rebinned = ROOT.TH1D("h_Z_mass_rebinned", "Z boson mass;M_{#mu#mu} (GeV);Entries", n_bins_z_mass, array('d', z_mass_bin_edges))
        for bin_idx in range(1, hist.GetNbinsX() + 1):
            bin_center = hist.GetBinCenter(bin_idx)
            bin_content = hist.GetBinContent(bin_idx)
            bin_error = hist.GetBinError(bin_idx)
            h_Z_mass_rebinned.Fill(bin_center, bin_content)
            h_Z_mass_rebinned.SetBinError(h_Z_mass_rebinned.FindBin(bin_center), bin_error)
        h_Z_mass_rebinned.SetLineColor(ROOT.kBlue)
        h_Z_mass_rebinned.Draw("HIST")
        # h_Z_mass_rebinned.Write()
        canvas.SaveAs(f"hist_real_data_hist/{hist_name}_variable_bins.png")

    elif hist_name == "h_Z_mass_eq":
        hist.SetXTitle("M_{#mu#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        canvas.SetLogx()
        hist.SetMinimum(1)
        hist.SetTitle("Z boson mass")

    elif hist_name == "h_Z_mass_fine":
        hist.SetXTitle("M_{#mu#mu} (GeV)")
        hist.SetYTitle("Entries")
        canvas.SetLogy()
        hist.SetTitle("Z boson mass")
        combined_func = ROOT.TF1("combined_func", "[0]/((x*x - [1]*[1])^2 + ([1]*[2])^2) + [3] + [4]*x + [5]*x*x", 80, 100)
        combined_func.SetParameters(1e10, 91.2, 2.5, 1e3, -1.0, 0.1)
        combined_func.SetParNames("Norm", "M (Mass)", "Gamma (Width)", "Cheb_T0", "Cheb_T1", "Cheb_T2")
        hist.GetXaxis().SetRangeUser(80, 100)
        fit_result = hist.Fit(combined_func, "S, R", "", 85, 95)
        print(f"Resonance Mass (M): {combined_func.GetParameter(1)} GeV")
        print(f"Width (Gamma): {combined_func.GetParameter(2)} GeV")
        print(f"Normalization (Parameter 0): {combined_func.GetParameter(0)}")
        ndf = fit_result.Ndf()
        chi2 = fit_result.Chi2()
        print(f"Chi2/NDF: {chi2 / ndf}")
        combined_func.Draw("SAME")
        canvas.Modified()
        canvas.Update()


    print(f"Histogram: {hist_name}")
    hist.Print()
    
    
    hist.Draw()

    canvas.SaveAs(f"hist_real_data_hist/{hist_name}.png")
    canvas.Close()

file.Close()

