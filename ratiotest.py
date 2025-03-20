import ROOT

file_real = ROOT.TFile.Open("output.root", "READ")
file_sim = ROOT.TFile.Open("simoutput.root", "READ")

real_name = "h_Z_mass_fine"
sim_name = "simh_Z_mass_fine"

hist_real = file_real.Get(real_name)
hist_sim = file_sim.Get(sim_name)

if hist_real.Integral() > 0:
    hist_real.Scale(1.0 / hist_real.Integral())
if hist_sim.Integral() > 0:
    hist_sim.Scale(1.0 / hist_sim.Integral())

canvas = ROOT.TCanvas("canvas", "Z Boson Mass", 800, 800)
pad1 = ROOT.TPad("pad1", "Main Plot", 0, 0.3, 1, 1)
pad2 = ROOT.TPad("pad2", "Ratio Plot", 0, 0, 1, 0.3)

pad1.SetBottomMargin(1)
pad2.SetTopMargin(0.02)
pad2.SetBottomMargin(0.3)

pad1.Draw()
pad2.Draw()

pad1.cd()
hist_real.SetLineColor(ROOT.kBlack)
hist_real.SetLineWidth(2)

hist_sim.SetLineColor(ROOT.kRed)
hist_sim.SetLineWidth(2)

hist_real.Draw("HIST")
hist_sim.Draw("HIST SAME")

legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.85)
legend.AddEntry(hist_real, "Real", "l")
legend.AddEntry(hist_sim, "Simulated", "l")
legend.Draw()

pad2.cd()

hist_ratio = hist_real.Clone("hist_ratio")
hist_ratio.Divide(hist_sim)

hist_ratio.SetLineColor(ROOT.kBlue)
hist_ratio.SetMarkerStyle(20)
hist_ratio.SetMarkerSize(0.8)

hist_ratio.SetTitle("")
hist_ratio.GetYaxis().SetTitle("Data / Sim")
hist_ratio.GetYaxis().SetNdivisions(505)
hist_ratio.GetYaxis().SetTitleSize(14)
hist_ratio.GetYaxis().SetTitleFont(43)
hist_ratio.GetYaxis().SetTitleOffset(1.2)
hist_ratio.GetYaxis().SetLabelFont(43)
hist_ratio.GetYaxis().SetLabelSize(12)

hist_ratio.GetXaxis().SetTitle("Invariant Mass M(Z) [GeV]")
hist_ratio.GetXaxis().SetTitleSize(14)
hist_ratio.GetXaxis().SetTitleFont(43)
hist_ratio.GetXaxis().SetTitleOffset(3)
hist_ratio.GetXaxis().SetLabelFont(43)
hist_ratio.GetXaxis().SetLabelSize(12)

hist_ratio.Draw()

line = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1, hist_ratio.GetXaxis().GetXmax(), 1)
line.SetLineColor(ROOT.kBlack)
line.Draw()

canvas.SaveAs("Z_mass_fine_comparison_with_ratio.png")

file_real.Close()
file_sim.Close()
