import ROOT

file_real = ROOT.TFile.Open("output.root", "READ")
file_sim1 = ROOT.TFile.Open("simoutput.root", "READ")
file_sim2 = ROOT.TFile.Open("simoutput2.root", "READ")

hist_pairs = {
    "h_Z_mass": "simh_Z_mass",
    "h_Z_mass_fine": "simh_Z_mass_fine",
}

for real_name, sim_name in hist_pairs.items():

    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas("canvas", "Z Boson Mass", 800, 800)
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
    hist_real.SetTitle("Z boson mass")
    hist_real.GetXaxis().SetLabelSize(0)

    if real_name == "h_Z_mass":
        pad1.SetLogx()
        hist_real.SetMinimum(1)

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

    if real_name == "h_Z_mass":
        pad2.SetLogx()
        hist_ratio.GetYaxis().SetRangeUser(0, 2)

    elif real_name == "h_Z_mass_fine":
        hist_ratio.GetXaxis().SetRangeUser(80, 100)
        hist_ratio.GetYaxis().SetRangeUser(0, 2)


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

    hist_ratio.GetXaxis().SetTitle("M_{#mu#mu} (GeV)")
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

    line.SetLineColor(ROOT.kBlack)
    line.Draw()

    canvas.SaveAs(f"combratio{real_name}.png")

file_real.Close()
file_sim1.Close()
file_sim2.Close()
