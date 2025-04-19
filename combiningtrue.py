import ROOT

file_sim1 = ROOT.TFile.Open("simoutputtrue1.root", "READ")
file_sim2 = ROOT.TFile.Open("simoutputtrue2.root", "READ")


hist_names = {"simh_particle_pt", "simh_particle_eta", "simh_particle_phi", "simh_particle_energy", "simh_particle_mass", "simh_particle_leading", "simh_particle_subleading",
              "simh_Z_pt", "simh_Z_eta", "simh_Z_phi", "simh_Z_energy", "simh_Z_mass", "simh_Z_mass_fine",
}

for sim_name in hist_names:
    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas("canvas", "Real vs Simulated", 800, 800)

    hist_sim1 = file_sim1.Get(sim_name)
    hist_sim2 = file_sim2.Get(sim_name)

    hist_sim1.SetLineColor(ROOT.kRed)
    hist_sim1.SetLineWidth(2) 
    hist_sim1.SetYTitle("Entries")
    canvas.SetLogy()
    hist_sim1.SetMinimum(1)

    hist_sim2.SetLineColor(ROOT.kBlue)
    hist_sim2.SetLineWidth(2)

    if sim_name == "simh_muon_pt":
        hist_sim1.SetXTitle("p_{T#mu} (GeV)")
        hist_sim1.SetTitle("Muon transverse momentum")

    elif sim_name == "simh_muon_eta":
        hist_sim1.SetXTitle("#eta_{#mu}")
        hist_sim1.SetTitle("Muon pseudorapidity")

    elif sim_name == "simh_muon_phi":
        hist_sim1.SetXTitle("#phi_{#mu}")
        hist_sim1.SetTitle("Muon azimuthal angle")

    elif sim_name == "simh_muon_energy":
        hist_sim1.SetXTitle("E_{#mu} (GeV)")
        hist_sim1.SetTitle("Muon energy")

    elif sim_name == "simh_muon_mass":
        hist_sim1.SetXTitle("M_{#mu} (GeV)")
        hist_sim1.SetTitle("Muon mass")

    elif sim_name == "simh_muon_leading":
        hist_sim1.SetXTitle("p_{T#mu} (GeV)")
        hist_sim1.SetTitle("Leading muon transverse momentum")

    elif sim_name == "simh_muon_subleading":
        hist_sim1.SetXTitle("p_{T#mu} (GeV)")
        hist_sim1.SetTitle("Subleading muon transverse momentum")

    elif sim_name == "simh_Z_pt":
        hist_sim1.SetXTitle("p_{T#mu#mu} (GeV)")
        hist_sim1.SetTitle("Z boson transverse momentum")

    elif sim_name == "simh_Z_eta":
        hist_sim1.SetXTitle("#eta_{#mu#mu}")
        hist_sim1.SetTitle("Z boson pseudorapidity")

    elif sim_name == "simh_Z_phi":
        hist_sim1.SetXTitle("#phi_{#mu#mu}")
        hist_sim1.SetTitle("Z boson azimuthal angle")

    elif sim_name == "simh_Z_energy":
        hist_sim1.SetXTitle("E_{#mu#mu} (GeV)")
        hist_sim1.SetTitle("Z boson energy")

    elif sim_name == "simh_Z_mass":
        canvas.SetLogx()
        # hist_sim1.GetXaxis().SetRangeUser(10, 100)
        hist_sim1.SetXTitle("M_{#mu#mu} (GeV)")
        hist_sim1.SetTitle("Z boson mass")

    elif sim_name == "simh_Z_mass_fine":
        hist_sim1.GetXaxis().SetRangeUser(80, 100)
        hist_sim1.SetXTitle("M_{#mu#mu} (GeV)")
        hist_sim1.SetTitle("Z boson mass")

  
    hist_sim1.Draw("HIST")
    hist_sim2.Draw("HIST SAME")

    legend = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)
    legend.AddEntry(hist_sim1, "M-50", "l")
    legend.AddEntry(hist_sim2, "M-10to50", "l")
    legend.Draw()

    canvas.SaveAs(f"comb_true_hist/combtrue{sim_name}.png")

file_sim1.Close()
file_sim2.Close()
