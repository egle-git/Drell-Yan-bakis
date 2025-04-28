import ROOT
import sys
from array import array

file_real = ROOT.TFile.Open("outputnew.root", "READ")
file_sim1 = ROOT.TFile.Open("simoutput.root", "READ")
file_sim2 = ROOT.TFile.Open("simoutput2.root", "READ")
file_tt = ROOT.TFile.Open("simoutputtt.root", "READ")
file_twtop = ROOT.TFile.Open("simoutputtwtop.root", "READ")
file_twantitop = ROOT.TFile.Open("simoutputtwantitop.root", "READ")
#file_tchantop = ROOT.TFile.Open("simoutputtchantop.root", "READ")
file_tchanantitop = ROOT.TFile.Open("simoutputtchanantitop.root", "READ")
file_ww = ROOT.TFile.Open("simoutputww.root", "READ")
file_wz = ROOT.TFile.Open("simoutputwz.root", "READ")
file_zz = ROOT.TFile.Open("simoutputzz.root", "READ")


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
    hist_tt = file_tt.Get(sim_name)
    hist_twtop = file_twtop.Get(sim_name)
    hist_twantitop = file_twantitop.Get(sim_name)
    #hist_tchantop = file_tchantop.Get(sim_name)
    hist_tchanantitop = file_tchanantitop.Get(sim_name)
    hist_ww = file_ww.Get(sim_name)
    hist_wz = file_wz.Get(sim_name)
    hist_zz = file_zz.Get(sim_name)
    

    hist_sim_combined = hist_sim1.Clone()
    hist_sim_combined.Add(hist_sim2)
    hist_tt_combined = hist_tt.Clone()
    hist_tt_combined.Add(hist_twtop)
    hist_tt_combined.Add(hist_twantitop)
    #hist_tt_combined.Add(hist_tchantop)
    hist_tt_combined.Add(hist_tchanantitop)
    hist_ew_combined = hist_ww.Clone()
    hist_ew_combined.Add(hist_wz)
    hist_ew_combined.Add(hist_zz)


    hist_real.SetMarkerColor(ROOT.kBlack)
    hist_real.SetMarkerSize(0.5)
    hist_real.SetMarkerStyle(20)
    hist_sim_combined.SetLineColor(ROOT.kRed)
    hist_sim_combined.SetLineWidth(2)
    hist_sim_combined.SetFillColor(ROOT.kRed)
    hist_sim_combined.SetFillStyle(3003)
    hist_tt_combined.SetLineColor(ROOT.kBlue)
    hist_tt_combined.SetLineWidth(2)
    hist_tt_combined.SetFillColor(ROOT.kBlue)
    hist_tt_combined.SetFillStyle(3003)
    hist_ew_combined.SetLineColor(ROOT.kGreen)
    hist_ew_combined.SetLineWidth(2)
    hist_ew_combined.SetFillColor(ROOT.kGreen)
    hist_ew_combined.SetFillStyle(3003)

    hist_real.SetYTitle("Entries")
    pad1.SetLogy()
    hist_real.GetXaxis().SetLabelSize(0)
    

    stack = ROOT.THStack("stack", "")
    stack.Add(hist_ew_combined)
    stack.Add(hist_tt_combined)
    stack.Add(hist_sim_combined)

    stack.SetMinimum(1)

    if real_name == "h_Z_mass":
        pad1.SetLogx()

    if real_name == "h_Z_mass_eq":
        pad1.SetLogx()

    stack.Draw("HIST")
    hist_real.Draw("PE SAME")

    legend = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)
    legend.AddEntry(hist_real, "data", "p")
    legend.AddEntry(hist_tt, "TT", "f")
    legend.AddEntry(hist_sim_combined, "DY_MC", "f")
    legend.Draw()

    pad2.cd()
    pad2.Clear()

    hist_mc_total = hist_ew_combined.Clone()
    hist_mc_total.Add(hist_tt_combined)
    hist_mc_total.Add(hist_sim_combined)
    hist_ratio = hist_real.Clone("hist_ratio")
    hist_ratio.Divide(hist_mc_total)
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

    elif real_name == "h_Z_mass_eq":
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

    elif real_name == "h_Z_mass_eq":
        line = ROOT.TLine(40, 1, 1000, 1)

    elif real_name == "h_Z_mass_fine":
        line = ROOT.TLine(80, 1, 100, 1)

    else:
        line = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1, hist_ratio.GetXaxis().GetXmax(), 1)
    
    line.SetLineColor(ROOT.kBlack)
    line.Draw()

    canvas.SaveAs(f"hist_comb_data_hist/comb{real_name}.png")


# z_mass_bin_edges = [40,45,50,55,60,64,68,72,76,81,86,91,96,101,106,110,115,120,126,133,141,150,160,171,185,200,220,243,273,320,380,440,510,600,700,830,1000]


# for real_name, sim_name in hist_pairs.items():

#     if real_name == "h_Z_mass":

#         canvas_binned = ROOT.TCanvas(f"canvas_{real_name}_binned", "Z mass rebinned", 800, 800)
#         pad1_b = ROOT.TPad("pad1_b", "Main Plot", 0, 0.3, 1, 1)
#         pad2_b = ROOT.TPad("pad2_b", "Ratio Plot", 0, 0, 1, 0.3)
#         pad1_b.SetBottomMargin(0)
#         pad2_b.SetTopMargin(0)
#         pad2_b.SetBottomMargin(0.3)
#         pad1_b.SetGrid()
#         pad1_b.Draw()
#         pad2_b.Draw()

#         z_mass_bin_edges_arr = array('d', z_mass_bin_edges)
#         n_bins_z_mass = len(z_mass_bin_edges) - 1
#         print(n_bins_z_mass)

#         hist_real_rebinned = ROOT.TH1D("h_Z_mass_real_rebinned", "Z mass;M_{#mu#mu} (GeV);Entries", n_bins_z_mass, z_mass_bin_edges_arr)
#         for bin_idx in range(1, hist_real.GetNbinsX() + 1):
#             bin_center = hist_real.GetBinCenter(bin_idx)
#             bin_content = hist_real.GetBinContent(bin_idx)
#             bin_error = hist_real.GetBinError(bin_idx)
#             hist_real_rebinned.Fill(bin_center, bin_content)
#             hist_real_rebinned.SetBinError(hist_real_rebinned.FindBin(bin_center), bin_error)


#         hist_sim_rebinned = ROOT.TH1D("h_Z_mass_sim_rebinned", "Z mass (MC);M_{#mu#mu} (GeV);Entries", n_bins_z_mass, z_mass_bin_edges_arr)
#         for bin_idx in range(1, hist_sim_combined.GetNbinsX() + 1):
#             bin_center = hist_sim_combined.GetBinCenter(bin_idx)
#             bin_content = hist_sim_combined.GetBinContent(bin_idx)
#             bin_error = hist_sim_combined.GetBinError(bin_idx)
#             hist_sim_rebinned.Fill(bin_center, bin_content)
#             hist_sim_rebinned.SetBinError(hist_sim_rebinned.FindBin(bin_center), bin_error)


#         hist_real_rebinned.SetMarkerColor(ROOT.kBlack)
#         hist_real_rebinned.SetMarkerSize(0.5)
#         hist_real_rebinned.SetMarkerStyle(20)
#         hist_sim_rebinned.SetLineColor(ROOT.kRed)
#         hist_sim_rebinned.SetLineWidth(2)
#         hist_sim_rebinned.SetFillColor(ROOT.kRed)
#         hist_sim_rebinned.SetFillStyle(3003)
#         hist_real_rebinned.SetYTitle("Entries")
#         hist_real_rebinned.SetMinimum(1)

#         pad1_b.cd()
#         pad1_b.SetLogx()
#         pad1_b.SetLogy()
#         hist_real_rebinned.Draw("PE")
#         hist_sim_rebinned.Draw("HIST SAME")
#         legend_b = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)
#         legend_b.AddEntry(hist_real_rebinned, "data", "p")
#         legend_b.AddEntry(hist_sim_rebinned, "DY_MC", "l")
#         legend_b.Draw()

#         pad2_b.cd()
#         pad2_b.SetLogx()
#         hist_ratio_binned = hist_real_rebinned.Clone("hist_ratio_binned")
#         hist_ratio_binned.Divide(hist_sim_rebinned)
#         hist_ratio_binned.SetXTitle("M_{#mu#mu} (GeV)")
#         hist_ratio_binned.SetYTitle("Data / DY_MC")
#         hist_ratio_binned.GetYaxis().SetRangeUser(0, 2)
#         hist_ratio_binned.SetLineColor(ROOT.kBlue)
#         hist_ratio_binned.SetMarkerStyle(20)
#         hist_ratio_binned.SetMarkerSize(0.5)

#         for axis in [hist_ratio_binned.GetXaxis(), hist_ratio_binned.GetYaxis()]:
#             axis.SetTitleSize(16)
#             axis.SetTitleFont(43)
#             axis.SetLabelFont(43)
#             axis.SetLabelSize(16)
#         hist_ratio_binned.GetYaxis().SetTitleOffset(2)

#         hist_ratio_binned.Draw()
#         line_binned = ROOT.TLine(z_mass_bin_edges[0], 1, z_mass_bin_edges[-1], 1)
#         line_binned.SetLineColor(ROOT.kBlack)
#         line_binned.Draw()

#         canvas_binned.SaveAs("comb_pat_hist/combpath_Z_mass_variable_bins.png")


# file_real.Close()
# file_sim1.Close()
# file_sim2.Close()
