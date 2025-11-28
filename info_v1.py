#!/usr/bin/env python3
import pickle
import numpy as np
import sys
import os

folder = sys.argv[1]

# Load data and config
config = pickle.load(open(os.path.join(folder, "config.pkl"), "rb"))
data = np.load(os.path.join(folder, "data.npy"))

n_events = data.shape[0]
scale = 1e6 / n_events

# Map variable names to column indices
all_vars = config["conditioning_features"] + config["target_features"]
var2col = {v: i for i, v in enumerate(all_vars)}

# EXACT required variable order
ordered_vars = [
    "GenElectron_pt",
    "GenPromptPhoton_pt",
    "Jet_pt",
    "Jet_mass",
    "GenElectron_ClosestGenJet_DeltaR",
    "GenPromptPhoton_ClosestGenJet_DeltaR",
    "Jet_GenElectronDr",
    "Jet_GenPromptPhotonDr",
    "GenElectron_ClosestGenJet_pt",
    "GenElectron_ClosestGenJet_mass",
    "GenPromptPhoton_ClosestGenJet_pt",
    "GenPromptPhoton_ClosestGenJet_mass",
    "GenJet_pt",
    "GenJet_mass",
    "GenJet_closestGVTau_pt",
    "GenJet_Pileup_nPU",
    "GenJet_SV_mass",
    "FakeJet_pt",
    "GenJetAK8_pt",
    "GenJetAK8_mass",
    "GenJetAK8_SubGenJetAK8_pt1",
    "GenJetAK8_SubGenJetAK8_pt2",
    "GenJetAK8_SubGenJetAK8_mass1",
    "GenJetAK8_SubGenJetAK8_mass2",
    "Muon_pt",
    "Muon_mass",
    "Muon_genMuonPt",
    "Muon_FSRPt",
    "GenJet_pt",
    "GenJet_mass",
    "GenJet_closestMuon_dr",
    "GenJet_closestMuon_pt",
    "GenJet_closestGVTau_pt",
    "GenJet_Pileup_nPU",
    "GenJet_SV_mass",
    "GenMET_pt",
    "Pileup_nPU",
    "GenHT",
    "JetHT",
    "Recoil_pt",
    "Ref_pt",
    "GenMuon_pt",
    "GenMuon_ClosestGenJet_DeltaR",
    "GenMuon_ClosestGenJet_pt",
    "GenMuon_ClosestGenJet_mass",
    "GenMuon_Pileup_nPU",
    "Jet_pt",
    "Jet_mass",
    "Jet_GenMuonDr",
    "Duplicate_pt",
    "GenElectron_pt",
    "GenPromptPhoton_pt",
    "Jet_pt",
    "Jet_mass",
    "GenElectron_ClosestGenJet_DeltaR",
    "GenPromptPhoton_ClosestGenJet_DeltaR",
    "Jet_GenElectronDr",
    "Jet_GenPromptPhotonDr",
    "GenElectron_ClosestGenJet_pt",
    "GenElectron_ClosestGenJet_mass",
    "GenPromptPhoton_ClosestGenJet_pt",
    "GenPromptPhoton_ClosestGenJet_mass",
    "TrackGenJetAK4_pt",
    "PileUpSV_nPU",
    "GenJet_pt",
    "SubGenJetAK8_pt",
    "SubGenJetAK8_mass",
    "SubGenJetAK8_ReconstructedFatJet_pt",
    "SubGenJetAK8_ReconstructedFatJet_mass",
    "MatchedJet_pt",
    "MatchedJet_mass",
    "MatchedJet_SV_mass",
    "MatchedJet_ClosestGenVisTau_DeltaR",
    "MatchedJet_ClosestGenVisTau_mass",
    "MatchedJet_ClosestGenVisTau_pt",
    "UnmatchedJet_pt",
    "UnmatchedJet_mass",
    "UnmatchedJet_SV_mass"
]

# Variable categories
pt_mass_vars = {
    "GenElectron_pt", "GenPromptPhoton_pt", "Jet_pt", "Jet_mass",
    "GenElectron_ClosestGenJet_pt", "GenElectron_ClosestGenJet_mass",
    "GenPromptPhoton_ClosestGenJet_pt", "GenPromptPhoton_ClosestGenJet_mass",
    "GenJet_pt", "GenJet_mass", "GenJet_closestGVTau_pt",
    "GenJet_SV_mass", "FakeJet_pt", "GenJetAK8_pt", "GenJetAK8_mass",
    "GenJetAK8_SubGenJetAK8_pt1", "GenJetAK8_SubGenJetAK8_pt2",
    "GenJetAK8_SubGenJetAK8_mass1", "GenJetAK8_SubGenJetAK8_mass2",
    "Muon_pt", "Muon_mass", "Muon_genMuonPt", "Muon_FSRPt",
    "GenJet_closestMuon_pt", "GenMET_pt", "GenHT", "JetHT", "Recoil_pt",
    "Ref_pt", "GenMuon_pt", "GenMuon_ClosestGenJet_pt", "GenMuon_ClosestGenJet_mass",
    "Jet_pt", "Jet_mass", "Duplicate_pt", "TrackGenJetAK4_pt",
    "SubGenJetAK8_pt", "SubGenJetAK8_mass", "SubGenJetAK8_ReconstructedFatJet_pt",
    "SubGenJetAK8_ReconstructedFatJet_mass", "MatchedJet_pt", "MatchedJet_mass",
    "MatchedJet_SV_mass", "MatchedJet_ClosestGenVisTau_mass",
    "MatchedJet_ClosestGenVisTau_pt", "UnmatchedJet_pt", "UnmatchedJet_mass",
    "UnmatchedJet_SV_mass"
}

dr_vars = {
    "GenElectron_ClosestGenJet_DeltaR", "GenPromptPhoton_ClosestGenJet_DeltaR",
    "Jet_GenElectronDr", "Jet_GenPromptPhotonDr", "GenJet_closestMuon_dr",
    "GenMuon_ClosestGenJet_DeltaR", "Jet_GenMuonDr", "MatchedJet_ClosestGenVisTau_DeltaR"
}

pu_vars = {"GenJet_Pileup_nPU", "Pileup_nPU", "GenMuon_Pileup_nPU", "PileUpSV_nPU"}

def count_range(arr, cond):
    return np.sum(cond(arr))

print("\nVariables and ranges:\n")
print("====================================\n")

spreadsheet_output = []

for var in ordered_vars:
    print(f"=== {var} ===")

    # determine ranges for this variable (same as ROOT script)
    if var in pt_mass_vars:
        ranges = [
            ("0-100",  lambda x: (x >= 0) & (x <= 100)),
            ("101-1000", lambda x: (x > 100) & (x <= 1000)),
            (">1000", lambda x: x > 1000)
        ]
    elif var in dr_vars:
        ranges = [
            ("<0.4", lambda x: x < 0.4),
            ("≥0.4", lambda x: x >= 0.4)
        ]
    elif var in pu_vars:
        ranges = [
            ("0-40", lambda x: (x >= 0) & (x <= 40)),
            ("41-60", lambda x: (x > 40) & (x <= 60)),
            (">60", lambda x: x > 60)
        ]
    else:
        ranges = []

    # If variable not present, emit "Not found" once per range (like ROOT)
    if var not in var2col:
        if not ranges:
            print(" Not found in the dataset\n")
            spreadsheet_output.append("Not found in the dataset")
        else:
            for _label, _cond in ranges:
                print(f" {'Not found in the dataset'}")
                spreadsheet_output.append("Not found in the dataset")
        print()
        continue

    # otherwise compute counts
    col = var2col[var]
    x = data[:, col]

    if not ranges:
        # variable present but not in any category: nothing to print/append
        print()
        continue

    for label, cond_func in ranges:
        val = count_range(x, cond_func) * scale
        print(f" {label:12}: {val:.2f}")
        spreadsheet_output.append(f"{val:.2f}")

    print()

# ------------------------------------------
# Final spreadsheet output
# ------------------------------------------
print("\nResults (to be pasted on the spreadsheet):\n")
for line in spreadsheet_output:
    print(line)

