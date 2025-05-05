z_mass_bin_edges = [40,45,50,55,60,64,68,72,76,81,86,91,96,101,106,110,115,120,126,133,141,150,160,171,185,200,220,243,273,320,380,440,510,600,700,830,1000]


for real_name, sim_name in hist_pairs.items():

    if real_name == "h_Z_mass":

        canvas_binned = ROOT.TCanvas(f"canvas_{real_name}_binned", "Z mass rebinned", 800, 800)
        pad1_b = ROOT.TPad("pad1_b", "Main Plot", 0, 0.3, 1, 1)
        pad2_b = ROOT.TPad("pad2_b", "Ratio Plot", 0, 0, 1, 0.3)
        pad1_b.SetBottomMargin(0)
        pad2_b.SetTopMargin(0)
        pad2_b.SetBottomMargin(0.3)
        pad1_b.SetGrid()
        pad1_b.Draw()
        pad2_b.Draw()

        z_mass_bin_edges_arr = array('d', z_mass_bin_edges)
        n_bins_z_mass = len(z_mass_bin_edges) - 1
        print(n_bins_z_mass)

        hist_real_rebinned = ROOT.TH1D("h_Z_mass_real_rebinned", "Z mass;M_{#mu#mu} (GeV);Entries", n_bins_z_mass, z_mass_bin_edges_arr)
        for bin_idx in range(1, hist_real.GetNbinsX() + 1):
            bin_center = hist_real.GetBinCenter(bin_idx)
            bin_content = hist_real.GetBinContent(bin_idx)
            bin_error = hist_real.GetBinError(bin_idx)
            hist_real_rebinned.Fill(bin_center, bin_content)
            hist_real_rebinned.SetBinError(hist_real_rebinned.FindBin(bin_center), bin_error)


        hist_sim_rebinned = ROOT.TH1D("h_Z_mass_sim_rebinned", "Z mass (MC);M_{#mu#mu} (GeV);Entries", n_bins_z_mass, z_mass_bin_edges_arr)
        for bin_idx in range(1, hist_sim_combined.GetNbinsX() + 1):
            bin_center = hist_sim_combined.GetBinCenter(bin_idx)
            bin_content = hist_sim_combined.GetBinContent(bin_idx)
            bin_error = hist_sim_combined.GetBinError(bin_idx)
            hist_sim_rebinned.Fill(bin_center, bin_content)
            hist_sim_rebinned.SetBinError(hist_sim_rebinned.FindBin(bin_center), bin_error)


        hist_real_rebinned.SetMarkerColor(ROOT.kBlack)
        hist_real_rebinned.SetMarkerSize(0.5)
        hist_real_rebinned.SetMarkerStyle(20)
        hist_sim_rebinned.SetLineColor(ROOT.kRed)
        hist_sim_rebinned.SetLineWidth(2)
        hist_sim_rebinned.SetFillColor(ROOT.kRed)
        hist_sim_rebinned.SetFillStyle(3003)
        hist_real_rebinned.SetYTitle("Entries")
        hist_real_rebinned.SetMinimum(1)

        pad1_b.cd()
        pad1_b.SetLogx()
        pad1_b.SetLogy()
        hist_real_rebinned.Draw("PE")
        hist_sim_rebinned.Draw("HIST SAME")
        legend_b = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)
        legend_b.AddEntry(hist_real_rebinned, "data", "p")
        legend_b.AddEntry(hist_sim_rebinned, "DY_MC", "l")
        legend_b.Draw()

        pad2_b.cd()
        pad2_b.SetLogx()
        hist_ratio_binned = hist_real_rebinned.Clone("hist_ratio_binned")
        hist_ratio_binned.Divide(hist_sim_rebinned)
        hist_ratio_binned.SetXTitle("M_{#mu#mu} (GeV)")
        hist_ratio_binned.SetYTitle("Data / DY_MC")
        hist_ratio_binned.GetYaxis().SetRangeUser(0, 2)
        hist_ratio_binned.SetLineColor(ROOT.kBlue)
        hist_ratio_binned.SetMarkerStyle(20)
        hist_ratio_binned.SetMarkerSize(0.5)

        for axis in [hist_ratio_binned.GetXaxis(), hist_ratio_binned.GetYaxis()]:
            axis.SetTitleSize(16)
            axis.SetTitleFont(43)
            axis.SetLabelFont(43)
            axis.SetLabelSize(16)
        hist_ratio_binned.GetYaxis().SetTitleOffset(2)

        hist_ratio_binned.Draw()
        line_binned = ROOT.TLine(z_mass_bin_edges[0], 1, z_mass_bin_edges[-1], 1)
        line_binned.SetLineColor(ROOT.kBlack)
        line_binned.Draw()

        canvas_binned.SaveAs("comb_pat_hist/combpath_Z_mass_variable_bins.png")


file_real.Close()
file_sim1.Close()
file_sim2.Close()
