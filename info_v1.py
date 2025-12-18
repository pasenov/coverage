#!/usr/bin/env python3
import pickle
import numpy as np
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 info_v1.py <parent_folder1> [<parent_folder2> ...]")
    sys.exit(1)

parent_folders = sys.argv[1:]

# Get n_events ONCE from an event_counts.json in any provider folder
# Format examples inside event_counts.json: "SomeFile.root\t821232" or "SomeFile.root: 821232"
import re

n_events = 0
unique_providers_list = sorted(set([
    "ele_from_geneles", "ele_from_genpromptphotons", "ele_from_jets",
    "jets", "fake_jets_features", "fat_jets", "fsr_photons_from_muons",
    "met", "muons", "muons_from_jets", "photon_from_geneles",
    "photon_from_genpromptphotons", "photon_from_jets", "sv_from_genjets",
    "sub_jets", "taus_with_GenVisTau", "taus_wo_GenVisTau"
]))

import json

def get_n_events_from_folder(parent_folder):
    n_ev = 0
    # Try to read event_counts.json from the provider folders first
    for provider in unique_providers_list:
        p = os.path.join(parent_folder, provider)
        json_path = os.path.join(p, "event_counts.json")
        if os.path.isfile(json_path):
            try:
                with open(json_path, "r") as fh:
                    try:
                        obj = json.load(fh)
                        if isinstance(obj, dict) and len(obj) > 0:
                            first_val = next(iter(obj.values()))
                            n_ev = int(first_val)
                            return n_ev
                    except Exception:
                        fh.seek(0)
                        text = fh.read()
                        m = re.search(r"\\.root\"?\s*[:\s]*([0-9]+)", text)
                        if m:
                            n_ev = int(m.group(1))
                            return n_ev
            except Exception:
                pass
    return n_ev

print(f"Using n_events = {n_events} from event_counts.json")

# n_events obtained from event_counts.json (no .npy fallback required)
scale = 1

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

unique_providers = sorted(set(providers))

def load_models_for_parent(parent_folder):
    models_local = {}
    for name in unique_providers:
        p = os.path.join(parent_folder, name)
        cfg_path = os.path.join(p, "config.pkl")
        data_path = os.path.join(p, "data.npy")
        if os.path.isfile(cfg_path) and os.path.isfile(data_path):
            try:
                cfg = pickle.load(open(cfg_path, "rb"))
                dat = np.load(data_path)
                all_vars = cfg.get("conditioning_features", []) + cfg.get("target_features", [])
                var2col = {v: i for i, v in enumerate(all_vars)}
                models_local[name] = {"path": p, "config": cfg, "data": dat, "var2col": var2col, "scale": scale}
            except Exception:
                models_local[name] = None
        else:
            models_local[name] = None
    return models_local

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

print("\nVariables and ranges (parents: %s)\n" % ", ".join(parent_folders))
print("====================================\n")

# Build ranges per variable once, to ensure identical row ordering across parents
ranges_per_var = []
for i, var in enumerate(ordered_vars):
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
    ranges_per_var.append((var, providers[i], ranges))

# Total number of rows
rows = sum(len(rngs) for (_, _, rngs) in ranges_per_var)

# For each parent folder, load models and compute column values
all_columns = []
parent_n_events = []
for parent in parent_folders:
    print(f"Processing parent: {parent}")
    models = load_models_for_parent(parent)
    n_events_local = get_n_events_from_folder(parent)
    parent_n_events.append(n_events_local)
    col_values = []
    for var, provider, ranges in ranges_per_var:
        model_info = models.get(provider)
        if model_info is None:
            # provider missing -> append zeros for each range
            for _ in ranges:
                col_values.append(0)
            continue

        var2col = model_info["var2col"]
        data = model_info["data"]
        scale = model_info.get("scale", 1)

        if var not in var2col:
            for _ in ranges:
                col_values.append(0)
            continue

        col = var2col[var]
        x = data[:, col]
        for _label, cond_func in ranges:
            val = int(count_range(x, cond_func) * scale)
            col_values.append(val)

    # if there were no ranges at all for any var, ensure empty list
    all_columns.append(col_values)

# Print header showing n_events per parent (optional)
print('\nn_events per parent:')
for p, n in zip(parent_folders, parent_n_events):
    print(f" {p}: {n}")

# Print tab-separated columns (rows x parents) with leading descriptive columns
num_parents = len(parent_folders)
if rows == 0:
    print("No ranges defined; nothing to output.")
else:
    # Build descriptive left-hand columns
    header = ["Object", "Source/Model", "Conditioning Variable", "Range"]

    # map provider -> object name
    provider_to_object = {
        'ele_from_geneles': 'Electron',
        'ele_from_genpromptphotons': 'Electron',
        'ele_from_jets': 'Electron',
        'jets': 'Jet',
        'fake_jets_features': 'Jet',
        'fat_jets': 'FatJet',
        'fsr_photons_from_muons': 'FSRPhoton',
        'met': 'MET',
        'muons': 'Muon',
        'muons_from_jets': 'Muon',
        'photon_from_geneles': 'Photon',
        'photon_from_genpromptphotons': 'Photon',
        'photon_from_jets': 'Photon',
        'sv_from_genjets': 'Secondary Vertex',
        'sub_jets': 'Subjet',
        'taus_with_GenVisTau': 'Tau',
        'taus_wo_GenVisTau': 'Tau'
    }

    # Prepare textual rows corresponding to ranges_per_var
    text_rows = []
    for var, provider, ranges in ranges_per_var:
        # conditioning variable: drop the first token before the first underscore
        cond = var.split('_', 1)[1] if '_' in var else var
        obj = provider_to_object.get(provider, '')
        for label, _cond in ranges:
            text_rows.append([obj, provider, cond, label])

    # Print to stdout (tab-separated), combining text and numeric columns
    print("\nResults (tab-separated, with descriptive columns A-D):\n")
    print("\t".join(header + list(parent_folders)))
    for r in range(rows):
        left = text_rows[r] if r < len(text_rows) else ["", "", "", ""]
        nums = [str(all_columns[c][r] if r < len(all_columns[c]) else 0) for c in range(num_parents)]
        print("\t".join(left + nums))

    # Write CSV (comma-separated) with A-D columns and parents starting at E
    out_csv = "output_info.csv"
    try:
        with open(out_csv, "w") as fh:
            # header: A-D are labels, E+ are full input directories
            fh.write(",".join(header + list(parent_folders)) + "\n")
            for r in range(rows):
                left = text_rows[r] if r < len(text_rows) else ["", "", "", ""]
                nums = [str(all_columns[c][r] if r < len(all_columns[c]) else 0) for c in range(num_parents)]
                fh.write(",".join(left + nums) + "\n")
        print(f"\nWrote results to {out_csv}")
    except Exception as e:
        print(f"Failed to write {out_csv}: {e}")

# Finished: print a short summary and per-parent n_events (if available)
print("\nDone. Results written to output_info.csv (tabular counts).")
print("n_events per parent (if available):")
for p, n in zip(parent_folders, parent_n_events):
    print(f" {p}: {n}")

