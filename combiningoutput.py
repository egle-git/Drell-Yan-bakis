import ROOT

file_real = ROOT.TFile.Open("output.root", "READ")
file_sim1 = ROOT.TFile.Open("simoutputtrue1.root", "READ") #simoutput.root arba simoutputtrue1.root
file_sim2 = ROOT.TFile.Open("simoutputtrue2.root", "READ") #simoutput2.root arba simoutputtrue2.root


# pat::muon
# hist_pairs = {
#     "h_muon_pt": "simh_muon_pt",
#     "h_muon_eta": "simh_muon_eta",
#     "h_muon_phi": "simh_muon_phi",
#     "h_muon_energy": "simh_muon_energy",
#     "h_muon_mass": "simh_muon_mass",
#     "h_muon_leading": "simh_muon_leading",
#     "h_muon_subleading": "simh_muon_subleading",
#     "h_Z_pt": "simh_Z_pt",
#     "h_Z_eta": "simh_Z_eta",
#     "h_Z_phi": "simh_Z_phi",
#     "h_Z_energy": "simh_Z_energy",
#     "h_Z_mass": "simh_Z_mass",
#     "h_Z_mass_fine": "simh_Z_mass_fine",
# }

# true muons
hist_pairs = {
    "h_muon_pt": "simh_particle_pt",
    "h_muon_eta": "simh_particle_eta",
    "h_muon_phi": "simh_particle_phi",
    "h_muon_energy": "simh_particle_energy",
    "h_muon_mass": "simh_particle_mass",
    "h_muon_leading": "simh_particle_leading",
    "h_muon_subleading": "simh_particle_subleading",
    "h_Z_pt": "simh_Z_pt",
    "h_Z_eta": "simh_Z_eta",
    "h_Z_phi": "simh_Z_phi",
    "h_Z_energy": "simh_Z_energy",
    "h_Z_mass": "simh_Z_mass",
    "h_Z_mass_fine": "simh_Z_mass_fine",
}

for real_name, sim_name in hist_pairs.items():
    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas("canvas", "Real vs Simulated", 800, 800)

    pad1 = ROOT.TPad("pad1", "Main Plot", 0, 0.3, 1, 1)
    pad2 = ROOT.TPad("pad2", "Ratio Plot", 0, 0, 1, 0.3)
    pad1.SetBottomMargin(0)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.3)
    pad1.SetGrid()
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    hist_real = file_real.Get(real_name)
    hist_sim1 = file_sim1.Get(sim_name)
    hist_sim2 = file_sim2.Get(sim_name)

    hist_sim_combined = hist_sim1.Clone()
    hist_sim_combined.Add(hist_sim2)

    hist_real.SetMarkerColor(ROOT.kBlack)
    hist_real.SetMarkerSize(0.5)
    hist_real.SetMarkerStyle(20)
    hist_sim_combined.SetLineColor(ROOT.kRed)
    hist_sim_combined.SetLineWidth(2)
    hist_sim_combined.SetFillColor(ROOT.kRed)
    hist_sim_combined.SetFillStyle(3003)   
    hist_real.SetYTitle("Entries")
    pad1.SetLogy()
    hist_real.GetXaxis().SetLabelSize(0)
    hist_real.SetMinimum(1)

    if real_name == "h_Z_mass":
        pad1.SetLogx()

    hist_real.Draw("PE")
    hist_sim_combined.Draw("HIST SAME")

    legend = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)
    legend.AddEntry(hist_real, "data", "p")
    legend.AddEntry(hist_sim_combined, "DY_MC", "l")
    legend.Draw()

    pad2.cd()
    pad2.Clear()

    hist_ratio = hist_real.Clone("hist_ratio")
    hist_ratio.Divide(hist_sim_combined)
    hist_ratio.GetYaxis().SetRangeUser(0, 2)


    if real_name == "h_muon_pt":
        hist_ratio.SetXTitle("p_{T#mu} (GeV)")
        hist_real.SetTitle("Muon transverse momentum")

    elif real_name == "h_muon_eta":
        hist_ratio.SetXTitle("#eta_{#mu}")
        hist_real.SetTitle("Muon pseudorapidity")

    elif real_name == "h_muon_phi":
        hist_ratio.SetXTitle("#phi_{#mu}")
        hist_real.SetTitle("Muon azimuthal angle")

    elif real_name == "h_muon_energy":
        hist_ratio.SetXTitle("E_{#mu} (GeV)")
        hist_real.SetTitle("Muon energy")

    elif real_name == "h_muon_mass":
        hist_ratio.SetXTitle("M_{#mu} (GeV)")
        hist_real.SetTitle("Muon mass")

    elif real_name == "h_muon_leading":
        hist_ratio.SetXTitle("p_{T#mu} (GeV)")
        hist_real.SetTitle("Leading muon transverse momentum")

    elif real_name == "h_muon_subleading":
        hist_ratio.SetXTitle("p_{T#mu} (GeV)")
        hist_real.SetTitle("Subleading muon transverse momentum")

    elif real_name == "h_Z_pt":
        hist_ratio.SetXTitle("p_{T#mu#mu} (GeV)")
        hist_real.SetTitle("Z boson transverse momentum")

    elif real_name == "h_Z_eta":
        hist_ratio.SetXTitle("#eta_{#mu#mu}")
        hist_real.SetTitle("Z boson pseudorapidity")

    elif real_name == "h_Z_phi":
        hist_ratio.SetXTitle("#phi_{#mu#mu}")
        hist_real.SetTitle("Z boson azimuthal angle")

    elif real_name == "h_Z_energy":
        hist_ratio.SetXTitle("E_{#mu#mu} (GeV)")
        hist_real.SetTitle("Z boson energy")

    elif real_name == "h_Z_mass":
        pad2.SetLogx()
        hist_ratio.SetXTitle("M_{#mu#mu} (GeV)")
        hist_real.SetTitle("Z boson mass")

    elif real_name == "h_Z_mass_fine":
        hist_ratio.GetXaxis().SetRangeUser(80, 100)
        hist_ratio.SetXTitle("M_{#mu#mu} (GeV)")
        hist_real.SetTitle("Z boson mass")

  
    hist_ratio.SetLineColor(ROOT.kBlue)
    hist_ratio.SetMarkerStyle(20)
    hist_ratio.SetMarkerSize(0.5)

    hist_ratio.SetTitle("")

    hist_ratio.GetYaxis().SetTitle("Data / DY_MC")
    hist_ratio.GetYaxis().SetNdivisions(505)
    hist_ratio.GetYaxis().SetTitleSize(16)
    hist_ratio.GetYaxis().SetTitleFont(43)
    hist_ratio.GetYaxis().SetTitleOffset(2)
    hist_ratio.GetYaxis().SetLabelFont(43)
    hist_ratio.GetYaxis().SetLabelSize(16)

    hist_ratio.GetXaxis().SetTitleSize(16)
    hist_ratio.GetXaxis().SetTitleFont(43)
    hist_ratio.GetXaxis().SetTitleOffset(2)
    hist_ratio.GetXaxis().SetLabelFont(43)
    hist_ratio.GetXaxis().SetLabelSize(16)

    hist_ratio.Draw()

    if real_name == "h_Z_mass":
        line = ROOT.TLine(0, 1, 1000, 1)

    elif real_name == "h_Z_mass_fine":
        line = ROOT.TLine(80, 1, 100, 1)

    else:
        line = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1, hist_ratio.GetXaxis().GetXmax(), 1)
    
    line.SetLineColor(ROOT.kBlack)
    line.Draw()

    canvas.SaveAs(f"combtrue{real_name}.png") # combpat arba combtrue

file_real.Close()
file_sim1.Close()
file_sim2.Close()
