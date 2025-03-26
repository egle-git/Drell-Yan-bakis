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

canvas = ROOT.TCanvas("canvas", "Real vs Simulated", 800, 600)

for real_name, sim_name in hist_pairs.items():
    hist_real = file_real.Get(real_name)
    hist_sim1 = file_sim1.Get(sim_name)
    hist_sim2 = file_sim2.Get(sim_name)

    hist_sim_combined = hist_sim1.Clone()
    hist_sim_combined.Add(hist_sim2)

    #if hist_real.Integral() > 0:
    #    hist_real.Scale(1.0 / hist_real.Integral())
    #if hist_sim.Integral() > 0:
    #    hist_sim.Scale(1.0 / hist_sim.Integral())

    hist_real.SetLineColor(ROOT.kBlack)
    hist_real.SetLineWidth(2)

    hist_sim_combined.SetLineColor(ROOT.kRed)
    hist_sim_combined.SetLineWidth(2)
    
    hist_real.Draw("HIST")
    hist_sim_combined.Draw("HIST SAME")

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.85)
    legend.AddEntry(hist_real, "Real Data", "l")
    legend.AddEntry(hist_sim_combined, "Simulated Data", "l")
    legend.Draw()

    canvas.SaveAs(f"comb{real_name}.png")

file_real.Close()
file_sim1.Close()
file_sim2.Close()
