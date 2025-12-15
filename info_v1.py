#!/usr/bin/env python3
import pickle
import numpy as np
import sys
import os

parent_folder = sys.argv[1]

# EXACT required variable order (kept as-is)
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
    "GenJet_closestMuon_dr",
    "GenJet_closestMuon_pt",
    "GenJet_closestGVTau_pt",
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
    "GenMET_pt",
    "GenHT",
    "JetHT",
    "Recoil_pt",
    "Ref_pt",
    "GenMuon_pt",
    "GenMuon_ClosestGenJet_DeltaR",
    "GenMuon_ClosestGenJet_pt",
    "GenMuon_ClosestGenJet_mass",
    "Jet_pt",
    "Jet_mass",
    "Jet_GenMuonDr",
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

# Provider folder for each ordered_vars entry (aligned by index).
# Use the exact subfolder names you specified.
providers = [
    "ele_from_geneles",                # GenElectron_pt
    "ele_from_genpromptphotons",       # GenPromptPhoton_pt
    "ele_from_jets",                   # Jet_pt
    "ele_from_jets",                   # Jet_mass
    "ele_from_geneles",                # GenElectron_ClosestGenJet_DeltaR
    "ele_from_genpromptphotons",       # GenPromptPhoton_ClosestGenJet_DeltaR
    "ele_from_jets",                   # Jet_GenElectronDr
    "ele_from_jets",                   # Jet_GenPromptPhotonDr
    "ele_from_geneles",                # GenElectron_ClosestGenJet_pt
    "ele_from_geneles",                # GenElectron_ClosestGenJet_mass
    "ele_from_genpromptphotons",       # GenPromptPhoton_ClosestGenJet_pt
    "ele_from_genpromptphotons",       # GenPromptPhoton_ClosestGenJet_mass
    "jets",                            # GenJet_pt
    "jets",                            # GenJet_mass
    "jets",                            # GenJet_closestMuon_dr
    "jets",                            # GenJet_closestMuon_pt
    "jets",                            # GenJet_closestGVTau_pt
    "jets",                            # GenJet_SV_mass
    "fake_jets_features",              # FakeJet_pt
    "fat_jets",                        # GenJetAK8_pt
    "fat_jets",                        # GenJetAK8_mass
    "fat_jets",                        # GenJetAK8_SubGenJetAK8_pt1
    "fat_jets",                        # GenJetAK8_SubGenJetAK8_pt2
    "fat_jets",                        # GenJetAK8_SubGenJetAK8_mass1
    "fat_jets",                        # GenJetAK8_SubGenJetAK8_mass2
    "fsr_photons_from_muons",          # Muon_pt
    "fsr_photons_from_muons",          # Muon_mass
    "fsr_photons_from_muons",          # Muon_genMuonPt
    "fsr_photons_from_muons",          # Muon_FSRPt
    "met",                             # GenMET_pt
    "met",                             # GenHT
    "met",                             # JetHT
    "met",                             # Recoil_pt
    "met",                             # Ref_pt
    "muons",                           # GenMuon_pt
    "muons",                           # GenMuon_ClosestGenJet_DeltaR
    "muons",                           # GenMuon_ClosestGenJet_pt
    "muons",                           # GenMuon_ClosestGenJet_mass
    "muons_from_jets",                 # Jet_pt
    "muons_from_jets",                 # Jet_mass
    "muons_from_jets",                 # Jet_GenMuonDr
    "photon_from_geneles",             # GenElectron_pt  (second block)
    "photon_from_genpromptphotons",    # GenPromptPhoton_pt (second block)
    "photon_from_jets",                # Jet_pt (second block)
    "photon_from_jets",                # Jet_mass (second block)
    "photon_from_geneles",             # GenElectron_ClosestGenJet_DeltaR
    "photon_from_genpromptphotons",    # GenPromptPhoton_ClosestGenJet_DeltaR
    "photon_from_jets",                # Jet_GenElectronDr
    "photon_from_jets",                # Jet_GenPromptPhotonDr
    "photon_from_geneles",             # GenElectron_ClosestGenJet_pt
    "photon_from_geneles",             # GenElectron_ClosestGenJet_mass
    "photon_from_genpromptphotons",    # GenPromptPhoton_ClosestGenJet_pt
    "photon_from_genpromptphotons",    # GenPromptPhoton_ClosestGenJet_mass
    "sv_from_genjets",                 # GenJet_pt (again)
    "sub_jets",                        # SubGenJetAK8_pt
    "sub_jets",                        # SubGenJetAK8_mass
    "sub_jets",                        # SubGenJetAK8_ReconstructedFatJet_pt
    "sub_jets",                        # SubGenJetAK8_ReconstructedFatJet_mass
    "taus_with_GenVisTau",             # MatchedJet_pt
    "taus_with_GenVisTau",             # MatchedJet_mass
    "taus_with_GenVisTau",             # MatchedJet_SV_mass
    "taus_with_GenVisTau",             # MatchedJet_ClosestGenVisTau_DeltaR
    "taus_with_GenVisTau",             # MatchedJet_ClosestGenVisTau_mass
    "taus_with_GenVisTau",             # MatchedJet_ClosestGenVisTau_pt
    "taus_wo_GenVisTau",               # UnmatchedJet_pt
    "taus_wo_GenVisTau",               # UnmatchedJet_mass
    "taus_wo_GenVisTau"                # UnmatchedJet_SV_mass
]

# Preload only the folders we will consult (skip missing)
unique_providers = sorted(set(providers))
models = {}
for name in unique_providers:
    p = os.path.join(parent_folder, name)
    cfg_path = os.path.join(p, "config.pkl")
    data_path = os.path.join(p, "data.npy")
    if os.path.isfile(cfg_path) and os.path.isfile(data_path):
        cfg = pickle.load(open(cfg_path, "rb"))
        dat = np.load(data_path)
        all_vars = cfg.get("conditioning_features", []) + cfg.get("target_features", [])
        var2col = {v: i for i, v in enumerate(all_vars)}
        n_events = dat.shape[0] if getattr(dat, "ndim", 0) > 0 else 0
        scale = 1e6 / n_events if n_events > 0 else 0.0
        models[name] = {"path": p, "config": cfg, "data": dat, "var2col": var2col, "scale": scale, "n_events": n_events}
    else:
        # mark as not available
        models[name] = None

# Variable categories
pt_mass_vars = {
    "GenElectron_pt", "GenPromptPhoton_pt", "Jet_pt", "Jet_mass",
    "GenElectron_ClosestGenJet_pt", "GenElectron_ClosestGenJet_mass",
    "GenPromptPhoton_ClosestGenJet_pt", "GenPromptPhoton_ClosestGenJet_mass",
    "GenJet_pt", "GenJet_mass", "GenJet_closestGVTau_pt",
    "GenJetAK8_pt", "GenJetAK8_mass",
    "GenJetAK8_SubGenJetAK8_pt1", "GenJetAK8_SubGenJetAK8_pt2",
    "GenJetAK8_SubGenJetAK8_mass1", "GenJetAK8_SubGenJetAK8_mass2",
    "Muon_pt", "Muon_mass", "Muon_genMuonPt", "Muon_FSRPt",
    "GenJet_closestMuon_pt", "GenMET_pt", "GenHT", "JetHT", "Recoil_pt",
    "Ref_pt", "GenMuon_pt", "GenMuon_ClosestGenJet_pt", "GenMuon_ClosestGenJet_mass",
    "SubGenJetAK8_pt", "SubGenJetAK8_mass", "SubGenJetAK8_ReconstructedFatJet_pt",
    "SubGenJetAK8_ReconstructedFatJet_mass", "MatchedJet_pt", "MatchedJet_mass",
    "MatchedJet_ClosestGenVisTau_pt", "UnmatchedJet_pt", "UnmatchedJet_mass"
}

sv_vars = {
    "GenJet_SV_mass", "MatchedJet_SV_mass", "UnmatchedJet_SV_mass"
}

fake_jet_pt_vars = {
    "FakeJet_pt"
}

ClosestGenVisTau_mass_vars = {
    "MatchedJet_ClosestGenVisTau_mass"
}

dr_vars = {
    "GenElectron_ClosestGenJet_DeltaR", "GenPromptPhoton_ClosestGenJet_DeltaR",
    "Jet_GenElectronDr", "Jet_GenPromptPhotonDr", "GenJet_closestMuon_dr",
    "GenMuon_ClosestGenJet_DeltaR", "Jet_GenMuonDr", "MatchedJet_ClosestGenVisTau_DeltaR"
}

def count_range(arr, cond):
    return np.sum(cond(arr))

print("\nVariables and ranges (parent: %s)\n" % parent_folder)
print("====================================\n")

spreadsheet_output = []

for i, var in enumerate(ordered_vars):
    provider = providers[i]
    model_info = models.get(provider)
    print(f"=== {var} (from {provider}) ===")

    # determine ranges for this variable
    if var in pt_mass_vars:
        ranges = [
            ("0-100",  lambda x: (x >= 0) & (x <= 100)),
            ("100-1000", lambda x: (x > 100) & (x <= 1000)),
            (">1000", lambda x: x > 1000)
        ]
    elif var in sv_vars:
        ranges = [
            ("0-1",  lambda x: (x >= 0) & (x <= 1)), # Light flavor-ish
            ("1-2", lambda x: (x > 1) & (x <= 2)), # Charm-ish
            ("2-4", lambda x: (x > 2) & (x <= 4)), # Bottom-ish (peak)
            ("4-6", lambda x: (x > 4) & (x <= 6)), # Bottom-ish (tail)
            ("6-10", lambda x: (x > 6) & (x <= 10)), # Mostly unknown
            (">10", lambda x: x > 10) # Mythological
        ]
    elif var in fake_jet_pt_vars:
        ranges = [
            ("0-100",  lambda x: (x >= 0) & (x <= 100)),
            ("100-1000", lambda x: (x > 100) & (x <= 1000)),
            (">1000", lambda x: x > 1000)
        ]
    elif var in ClosestGenVisTau_mass_vars:
        ranges = [
            ("<1.2",  lambda x: x <= 1.2), # 1-prong decays
            ("1.2-2", lambda x: (x > 1.2) & (x <= 2)), # pi0s
            ("2-5", lambda x: (x > 2) & (x <= 5)), # Multi-prong visible decays
            (">5", lambda x: x > 5)
        ]
    elif var in dr_vars:
        ranges = [
            ("<0.4", lambda x: x < 0.4),
            ("≥0.4", lambda x: x >= 0.4)
        ]
    else:
        ranges = []

    if model_info is None:
        # provider folder missing or missing files
        if not ranges:
            print(" Not found in the provided folder\n")
            spreadsheet_output.append("Not found in the provided folder")
        else:
            for _ in ranges:
                print(" Not found in the provided folder")
                spreadsheet_output.append("Not found in the provided folder")
        print()
        continue

    var2col = model_info["var2col"]
    data = model_info["data"]
    scale = model_info["scale"]

    if var not in var2col:
        if not ranges:
            print(" Not found in the dataset in that folder\n")
            spreadsheet_output.append("Not found in the dataset")
        else:
            for _ in ranges:
                print(" Not found in the dataset")
                spreadsheet_output.append("Not found in the dataset")
        print()
        continue

    col = var2col[var]
    x = data[:, col]

    if not ranges:
        print()
        continue

    for label, cond_func in ranges:
        val = count_range(x, cond_func) * scale
        print(f" {label:12}: {val:.2f}")
        spreadsheet_output.append(f"{val:.2f}")

    print()

# Compute total events (take the maximum n_events across available provider files)
total_events = max((m.get("n_events", 0) for m in models.values() if m), default=0)

# Convert to millions and format (trim trailing zeros)
n_m = total_events / 1e6 if total_events > 0 else 0.0
n_m_str = f"{n_m:.2f}".rstrip('0').rstrip('.')

print("\nResults (to be pasted on the spreadsheet):\n")
print(n_m_str)
for line in spreadsheet_output:
    print(line)

