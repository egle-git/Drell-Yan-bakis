import ROOT

file_real = ROOT.TFile.Open("output.root", "READ")
file_sim1 = ROOT.TFile.Open("simoutput.root", "READ")
file_sim2 = ROOT.TFile.Open("simoutput2.root", "READ")

hist_pairs = {
    "h_muon_pt": "simh_muon_pt",
    "h_muon_eta": "simh_muon_eta",
    "h_muon_phi": "simh_muon_phi",
    "h_muon_energy": "simh_muon_energy",
    "h_muon_mass": "simh_muon_mass",
    "h_muon_leading": "simh_muon_leading",
    "h_muon_subleading": "simh_muon_subleading",
    "h_Z_pt": "simh_Z_pt",
    "h_Z_eta": "simh_Z_eta",
    "h_Z_phi": "simh_Z_phi",
    "h_Z_energy": "simh_Z_energy",
    "h_Z_mass": "simh_Z_mass",
    "h_Z_mass_fine": "simh_Z_mass_fine",
}

ROOT.gStyle.SetOptStat(0)

canvas = ROOT.TCanvas("canvas", "Real vs Simulated", 800, 600)

for real_name, sim_name in hist_pairs.items():
    hist_real = file_real.Get(real_name)
    hist_sim1 = file_sim1.Get(sim_name)
    hist_sim2 = file_sim2.Get(sim_name)

    hist_sim_combined = hist_sim1.Clone()
    hist_sim_combined.Add(hist_sim2)

    if real_name == "h_muon_pt":
        hist_real.SetXTitle("p_{T#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Muon transverse momentum")

    elif real_name == "h_muon_eta":
        hist_real.SetXTitle("#eta_{#mu}")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Muon pseudorapidity")

    elif real_name == "h_muon_phi":
        hist_real.SetXTitle("#phi_{#mu}")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Muon azimuthal angle")

    elif real_name == "h_muon_energy":
        hist_real.SetXTitle("E_{#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Muon energy")

    elif real_name == "h_muon_mass":
        hist_real.SetXTitle("M_{#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Muon mass")

    elif real_name == "h_muon_leading":
        hist_real.SetXTitle("p_{T#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Leading muon transverse momentum")

    elif real_name == "h_muon_subleading":
        hist_real.SetXTitle("p_{T#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Subleading muon transverse momentum")

    elif real_name == "h_Z_pt":
        hist_real.SetXTitle("p_{T#mu#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Z boson transverse momentum")

    elif real_name == "h_Z_eta":
        hist_real.SetXTitle("#eta_{#mu#mu}")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Z boson pseudorapidity")

    elif real_name == "h_Z_phi":
        hist_real.SetXTitle("#phi_{#mu#mu}")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Z boson azimuthal angle")

    elif real_name == "h_Z_energy":
        hist_real.SetXTitle("E_{#mu#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Z boson energy")



    elif real_name == "h_Z_mass":
        hist_real.SetXTitle("M_{#mu#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        canvas.SetLogx()
        hist_real.SetMinimum(1)
        hist_real.SetTitle("Z boson mass")


    elif real_name == "h_Z_mass_fine":
        hist_real.SetXTitle("M_{#mu#mu} (GeV)")
        hist_real.SetYTitle("Entries")
        canvas.SetLogy()
        hist_real.SetTitle("Z boson mass")

        combined_func = ROOT.TF1("combined_func", "[0]/((x*x - [1]*[1])^2 + ([1]*[2])^2) + [3] + [4]*x + [5]*x*x", 80, 100)
        combined_func.SetParameters(1e10, 91.2, 2.5, 1e3, -1.0, 0.1)
        combined_func.SetParNames("Norm", "M (Mass)", "Gamma (Width)", "Cheb_T0", "Cheb_T1", "Cheb_T2")
        hist_real.GetXaxis().SetRangeUser(80, 100)
        fit_result = hist_real.Fit(combined_func, "S, R", "", 85, 95)
        print(f"Resonance Mass (M): {combined_func.GetParameter(1)} GeV")
        print(f"Width (Gamma): {combined_func.GetParameter(2)} GeV")
        print(f"Normalization (Parameter 0): {combined_func.GetParameter(0)}")
        ndf = fit_result.Ndf()
        chi2 = fit_result.Chi2()
        print(f"Chi2/NDF: {chi2 / ndf}")
        combined_func.Draw("SAME")
        canvas.Modified()
        canvas.Update()



    hist_real.SetMarkerColor(ROOT.kBlack)
    hist_real.SetMarkerSize(0.5)
    hist_real.SetMarkerStyle(20)

    hist_sim_combined.SetLineColor(ROOT.kRed)
    hist_sim_combined.SetLineWidth(2)
    hist_sim_combined.SetFillColor(ROOT.kRed)
    hist_sim_combined.SetFillStyle(3003)   
    
    hist_real.Draw("PE")
    hist_sim_combined.Draw("HIST SAME")

    legend = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)
    legend.AddEntry(hist_real, "data", "p")
    legend.AddEntry(hist_sim_combined, "DY_MC", "l")
    legend.Draw()

    canvas.SaveAs(f"comb{real_name}.png")

file_real.Close()
file_sim1.Close()
file_sim2.Close()
