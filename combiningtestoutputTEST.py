import ROOT
import sys
from array import array


lumi = 16494
xsec_shears = {
    "sim1": 6019.939,
    "sim2": 21037.59,
    "tt": 88.51,
    "twtop": 39.65,
    "twantitop": 39.65,
    "tchantop": 134.2,
    "tchanantitop": 80.0,
    "ww": 75.87,
    "wz": 27.59,
    "zz": 12.17,
}

xsec_genXsecAnalyzer = {
    "sim1": 6419,
    "sim2": 20480,
    "tt": 687.069813,
    "twtop": 32.445772,
    "twantitop": 32.507616,
    "tchantop": 119.708866,
    "tchanantitop": 71.742864,
    "ww": 75.87,
    "wz": 27.56,
    "zz": 12.14,
}

wsum_genXsecAnalyzer = {
    "sim1": 49693940,
    "sim2": 36942843,
    "tt": 43277246,
    "twtop": 6735428,
    "twantitop": 7307629,
    "tchantop": 110921410,
    "tchanantitop": 58466418,
    "ww": 15821000,
    "wz": 7584000,
    "zz": 1151000,
}

wsum_count = {
    "sim1": 4.96939e+07,
    "sim2": 3.69428e+07,
    "tt": 4.32772e+07,
    "twtop": 3.36824e+06,
    "twantitop": 3.65433e+06,
    "tchantop": 5.54612e+07,
    "tchanantitop": 2.92337e+07,
    "ww": 1.5821e+07,
    "wz": 7.584e+06,
    "zz": 1.151e+06,
}

weight_sum_files = {
    "sim1": "weight_sumtest.txt",
    "sim2": "weight_sumtest2.txt",
    "tt": "weight_sumtestTT.txt",
    "ww": "weight_sumtestww.txt",
    "wz": "weight_sumtestwz.txt",
    "zz": "weight_sumtestzz.txt",
    "twtop": "weight_sumtesttwtop.txt",
    "twantitop": "weight_sumtesttwantitop.txt",
    "tchantop": "weight_sumtesttchantop.txt",
    "tchanantitop": "weight_sumtesttchanantitop.txt",
}


file_real = ROOT.TFile.Open("outputnew.root", "READ")
file_sim1 = ROOT.TFile.Open("TESTsimoutputtest.root", "READ")
file_sim2 = ROOT.TFile.Open("TESTsimoutputtest2.root", "READ")
file_tt = ROOT.TFile.Open("TESTsimoutputtestTT.root", "READ")
file_twtop = ROOT.TFile.Open("TESTsimoutputtesttwtop.root", "READ")
file_twantitop = ROOT.TFile.Open("TESTsimoutputtesttwantitop.root", "READ")
file_tchantop = ROOT.TFile.Open("TESTsimoutputtesttchantop.root", "READ")
file_tchanantitop = ROOT.TFile.Open("TESTsimoutputtesttchanantitop.root", "READ")
file_ww = ROOT.TFile.Open("TESTsimoutputtestww.root", "READ")
file_wz = ROOT.TFile.Open("TESTsimoutputtestwz.root", "READ")
file_zz = ROOT.TFile.Open("TESTsimoutputtestzz.root", "READ")

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
    "h_Z_mass_eq": "simh_Z_mass_eq",
    "h_Z_mass_fine": "simh_Z_mass_fine",
}

for real_name, sim_name in hist_pairs.items():
    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas("canvas_"+real_name, "Real vs Simulated", 800, 800)

    pad1 = ROOT.TPad("pad1", "Main Plot", 0, 0.3, 1, 1)
    pad2 = ROOT.TPad("pad2", "Ratio Plot", 0, 0, 1, 0.3)
    pad1.SetBottomMargin(0)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.3)
    pad1.SetGrid()
    pad2.SetGrid()
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    hist_real = file_real.Get(real_name)

    hist_sim1 = file_sim1.Get(sim_name)
    hist_sim1.Scale(xsec_genXsecAnalyzer["sim1"]*lumi/wsum_count["sim1"])
    hist_sim2 = file_sim2.Get(sim_name)
    hist_sim2.Scale(xsec_genXsecAnalyzer["sim2"]*lumi/wsum_count["sim2"])


    sim_name_DYtau = sim_name.replace("simh_", "simh_DYtau_")
    hist_sim1_DYtau = file_sim1.Get(sim_name_DYtau)
    hist_sim1_DYtau.Scale(xsec_genXsecAnalyzer["sim1"]*lumi/wsum_count["sim1"])
    hist_sim2_DYtau = file_sim2.Get(sim_name_DYtau)
    hist_sim2_DYtau.Scale(xsec_genXsecAnalyzer["sim2"]*lumi/wsum_count["sim2"])

    hist_sim_combined = hist_sim1.Clone("hist_sim_combined")
    hist_sim_combined.Add(hist_sim2)
    hist_sim_DYtau_combined = hist_sim1_DYtau.Clone("hist_sim_DYtau_combined")
    hist_sim_DYtau_combined.Add(hist_sim2_DYtau)

    hist_tt = file_tt.Get(sim_name)
    print(hist_tt.Integral())
    hist_tt.Scale(xsec_genXsecAnalyzer["tt"]*lumi/wsum_count["tt"]/2)
    hist_twtop = file_twtop.Get(sim_name)
    hist_twtop.Scale(xsec_genXsecAnalyzer["twtop"]*lumi/wsum_count["twtop"])
    hist_twantitop = file_twantitop.Get(sim_name)
    hist_twantitop.Scale(xsec_genXsecAnalyzer["twantitop"]*lumi/wsum_count["twantitop"])
    hist_tchantop = file_tchantop.Get(sim_name)
    hist_tchantop.Scale(xsec_genXsecAnalyzer["tchantop"]*lumi/wsum_count["tchantop"])
    hist_tchanantitop = file_tchanantitop.Get(sim_name)
    hist_tchanantitop.Scale(xsec_genXsecAnalyzer["tchanantitop"]*lumi/wsum_count["tchanantitop"])
    hist_ww = file_ww.Get(sim_name)
    hist_ww.Scale(xsec_genXsecAnalyzer["ww"]*lumi/wsum_count["ww"])
    hist_wz = file_wz.Get(sim_name)
    hist_wz.Scale(xsec_genXsecAnalyzer["wz"]*lumi/wsum_count["wz"])
    hist_zz = file_zz.Get(sim_name)
    hist_zz.Scale(xsec_genXsecAnalyzer["zz"]*lumi/wsum_count["zz"])

    hist_st_combined = hist_twtop.Clone("hist_st_combined")
    hist_st_combined.Add(hist_twantitop)
    hist_st_combined.Add(hist_tchantop)
    hist_st_combined.Add(hist_tchanantitop)

    hist_ew_combined = hist_ww.Clone("hist_ew_combined")
    hist_ew_combined.Add(hist_wz)
    hist_ew_combined.Add(hist_zz)

    pad1.SetLogy()
    hist_real.SetMarkerColor(ROOT.kBlack)
    hist_real.SetLineColor(ROOT.kBlack)
    hist_real.SetMarkerSize(0.65)
    hist_real.SetMarkerStyle(20)

    hist_sim_combined.SetLineColor(ROOT.kRed)
    hist_sim_combined.SetLineWidth(2)
    hist_sim_combined.SetFillColor(ROOT.kRed)
    hist_sim_combined.SetFillStyle(3003)

    hist_sim_DYtau_combined.SetLineColor(ROOT.kOrange)
    hist_sim_DYtau_combined.SetLineWidth(2)
    hist_sim_DYtau_combined.SetFillColor(ROOT.kOrange)
    hist_sim_DYtau_combined.SetFillStyle(3003)
    
    hist_tt.SetLineColor(ROOT.kBlue)
    hist_tt.SetLineWidth(2)
    hist_tt.SetFillColor(ROOT.kBlue)
    hist_tt.SetFillStyle(3003)

    hist_st_combined.SetLineColor(ROOT.kTeal)
    hist_st_combined.SetLineWidth(2)
    hist_st_combined.SetFillColor(ROOT.kTeal)
    hist_st_combined.SetFillStyle(3003)

    hist_ew_combined.SetLineColor(ROOT.kGreen)
    hist_ew_combined.SetLineWidth(2)
    hist_ew_combined.SetFillColor(ROOT.kGreen)
    hist_ew_combined.SetFillStyle(3003)

    stack = ROOT.THStack("stack", "")
    stack.Add(hist_ew_combined)
    stack.Add(hist_st_combined)
    stack.Add(hist_tt)
    stack.Add(hist_sim_DYtau_combined)
    stack.Add(hist_sim_combined)
    stack.SetMinimum(1)

    if real_name in ["h_Z_mass", "h_Z_mass_eq"]:
        pad1.SetLogx()

    hist_real.Draw("PE")
    stack.Draw("HIST")
    hist_real.Draw("PE SAME")
    hist_real.Draw("SAMEAXIS")
    
    stack.GetYaxis().SetTitle("Number of Events")
    stack.GetYaxis().SetTitleSize(20)
    stack.GetYaxis().SetTitleFont(43)
    stack.GetYaxis().SetTitleOffset(1.5)
    stack.GetYaxis().SetLabelSize(20)
    stack.GetYaxis().SetLabelFont(43)

    legend = ROOT.TLegend(0.65, 0.65, 0.9, 0.9)
    legend.AddEntry(hist_real, "Data", "pl")
    legend.AddEntry(hist_sim_combined, "DY #rightarrow #mu#mu", "f")
    legend.AddEntry(hist_sim_DYtau_combined, "DY #rightarrow #tau#tau", "f")
    legend.AddEntry(hist_tt, "t#bar{t}", "f")
    legend.AddEntry(hist_st_combined, "Single top", "f")
    legend.AddEntry(hist_ew_combined, "EW", "f")
    legend.Draw()

    pad2.cd()
    pad2.Clear()

    hist_mc_total = hist_ew_combined.Clone("hist_mc_total")
    hist_mc_total.Add(hist_tt)
    hist_mc_total.Add(hist_st_combined)
    hist_mc_total.Add(hist_sim_DYtau_combined)
    hist_mc_total.Add(hist_sim_combined)

    hist_ratio = hist_real.Clone("hist_ratio")
    hist_ratio.Divide(hist_mc_total)
    hist_ratio.GetYaxis().SetRangeUser(0.5, 1.5)

    titles = {
        "h_muon_pt": ("p_{T#mu} (GeV)", "Muon transverse momentum"),
        "h_muon_eta": ("#eta_{#mu}", "Muon pseudorapidity"),
        "h_muon_phi": ("#phi_{#mu}", "Muon azimuthal angle"),
        "h_muon_energy": ("E_{#mu} (GeV)", "Muon energy"),
        "h_muon_mass": ("M_{#mu} (GeV)", "Muon mass"),
        "h_muon_leading": ("p_{T#mu} (GeV)", "Leading muon transverse momentum"),
        "h_muon_subleading": ("p_{T#mu} (GeV)", "Subleading muon transverse momentum"),
        "h_Z_pt": ("p_{T#mu#mu} (GeV)", "Z boson transverse momentum"),
        "h_Z_eta": ("#eta_{#mu#mu}", "Z boson pseudorapidity"),
        "h_Z_phi": ("#phi_{#mu#mu}", "Z boson azimuthal angle"),
        "h_Z_energy": ("E_{#mu#mu} (GeV)", "Z boson energy"),
        "h_Z_mass": ("M_{#mu#mu} (GeV)", "Z boson mass"),
        "h_Z_mass_eq": ("M_{#mu#mu} (GeV)", "Z boson mass"),
        "h_Z_mass_fine": ("M_{#mu#mu} (GeV)", "Z boson mass"),
    }

    xtitle, title = titles.get(real_name, ("", ""))
    hist_ratio.SetXTitle(xtitle)
    hist_real.SetTitle(title)

    if real_name == "h_Z_mass_eq":
        pad2.SetLogx()
    if real_name == "h_Z_mass":
        pad2.SetLogx()
    if real_name == "h_Z_mass_fine":
        hist_ratio.GetXaxis().SetRangeUser(80, 100)

    hist_ratio.SetLineColor(ROOT.kBlack)
    hist_ratio.SetMarkerColor(ROOT.kBlack)
    hist_ratio.SetMarkerStyle(20)
    hist_ratio.SetMarkerSize(0.65)
    hist_ratio.SetTitle("")

    hist_ratio.GetYaxis().SetTitle("Data / MC")
    hist_ratio.GetYaxis().CenterTitle()
    hist_ratio.GetYaxis().SetNdivisions(505)
    hist_ratio.GetYaxis().SetTitleSize(20)
    hist_ratio.GetYaxis().SetTitleFont(43)
    hist_ratio.GetYaxis().SetTitleOffset(1.5)
    hist_ratio.GetYaxis().SetLabelFont(43)
    hist_ratio.GetYaxis().SetLabelSize(20)
    hist_ratio.GetXaxis().SetTitleSize(25)
    hist_ratio.GetXaxis().SetTitleFont(43)
    hist_ratio.GetXaxis().SetTitleOffset(1)
    hist_ratio.GetXaxis().SetLabelFont(43)
    hist_ratio.GetXaxis().SetLabelSize(20)

    hist_ratio.Draw("PE")

    if real_name == "h_Z_mass":
        line = ROOT.TLine(0, 1, 1000, 1)
    elif real_name == "h_Z_mass_eq":
        line = ROOT.TLine(30, 1, 1000, 1)
    elif real_name == "h_Z_mass_fine":
        line = ROOT.TLine(80, 1, 100, 1)
    else:
        line = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1, hist_ratio.GetXaxis().GetXmax(), 1)

    line.SetLineColor(ROOT.kBlack)
    line.Draw()

    canvas.SaveAs(f"TESTtestcomb{real_name}.png")