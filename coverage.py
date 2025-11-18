#!/usr/bin/env python3
import ROOT
import sys

ROOT.ROOT.EnableImplicitMT()

# Provide filename by pasting the full path (no quotes) when prompted,
# or pass it as the first command-line argument.
if len(sys.argv) > 1:
    filename = sys.argv[1].strip()
else:
    filename = input("Paste full filename (no quotes), then press Enter: ").strip()

if not filename:
    raise SystemExit("No filename provided. Exiting.")

df = ROOT.RDataFrame("Events", filename)

# Total events
n_events = df.Count().GetValue()
scale = 1e6 / n_events

# ------------------------------------------
# Helpers
# ------------------------------------------

def branch_exists(df, branch):
    return branch in df.GetColumnNames()

def count_vector(df, varname, condition):
    if not branch_exists(df, varname):
        return None
    # Try vector-style per-event Sum (works if x is an RVec)
    try:
        return df.Define("x", varname) \
                 .Define("cnt", f"Sum({condition})") \
                 .Sum("cnt").GetValue()
    except Exception:
        # Fallback: define a per-event boolean/int and sum over events (works for scalars)
        return df.Define("x", varname) \
                 .Define("cnt", condition) \
                 .Sum("cnt").GetValue()

# ------------------------------------------
# EXACT required variable order
# ------------------------------------------

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
    "GenElectron_pt", 
    "GenPromptPhoton_pt", 
    "Jet_pt", 
    "Jet_mass",
    "GenElectron_ClosestGenJet_pt", 
    "GenElectron_ClosestGenJet_mass",
    "GenPromptPhoton_ClosestGenJet_pt", 
    "GenPromptPhoton_ClosestGenJet_mass",
    "GenJet_pt", "GenJet_mass", 
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
    "GenJet_closestMuon_pt", 
    "GenMET_pt", 
    "GenHT", 
    "JetHT", 
    "Recoil_pt", 
    "Ref_pt",
    "GenMuon_pt",                            
    "GenMuon_ClosestGenJet_pt",             
    "GenMuon_ClosestGenJet_mass", 
    "Jet_pt",
    "Jet_mass",        
    "Duplicate_pt",
    "GenElectron_pt",
    "GenPromptPhoton_pt",
    "Jet_pt",
    "Jet_mass",
    "GenElectron_ClosestGenJet_pt",
    "GenElectron_ClosestGenJet_mass",
    "GenPromptPhoton_ClosestGenJet_pt",
    "GenPromptPhoton_ClosestGenJet_mass",
    "TrackGenJetAK4_pt",
    "GenJet_pt",
    "SubGenJetAK8_pt",
    "SubGenJetAK8_mass",
    "SubGenJetAK8_ReconstructedFatJet_pt",
    "SubGenJetAK8_ReconstructedFatJet_mass",
    "MatchedJet_pt",
    "MatchedJet_mass",
    "MatchedJet_SV_mass",
    "MatchedJet_ClosestGenVisTau_mass",
    "MatchedJet_ClosestGenVisTau_pt",
    "UnmatchedJet_pt",
    "UnmatchedJet_mass",
    "UnmatchedJet_SV_mass"
}

dr_vars = {
    "GenElectron_ClosestGenJet_DeltaR",
    "GenPromptPhoton_ClosestGenJet_DeltaR",
    "Jet_GenElectronDr",
    "Jet_GenPromptPhotonDr",
    "GenJet_closestMuon_dr",
    "GenMuon_ClosestGenJet_DeltaR",
    "Jet_GenMuonDr",
    "GenElectron_ClosestGenJet_DeltaR",
    "GenPromptPhoton_ClosestGenJet_DeltaR",
    "Jet_GenElectronDr",
    "Jet_GenPromptPhotonDr",
    "MatchedJet_ClosestGenVisTau_DeltaR"
}

pu_vars = {
    "GenJet_Pileup_nPU", 
    "Pileup_nPU",
    "GenMuon_Pileup_nPU",
    "PileUpSV_nPU"
}

# ------------------------------------------
# Spreadsheet output list
# ------------------------------------------
spreadsheet_output = []

# ------------------------------------------
# PRINT RANGES + COMPUTE RESULTS
# ------------------------------------------

print("\nVariables and ranges:\n")
print("====================================\n")

for var in ordered_vars:

    print(f"=== {var} ===")

    # PT / MASS VARIABLES
    if var in pt_mass_vars:
        ranges = [
            ("0-100",  "x >= 0 && x <= 100"),
            ("101-1000", "x > 100 && x <= 1000"),
            (">1000", "x > 1000")
        ]
        for label, cond in ranges:
            c = count_vector(df, var, cond)
            if c is None:
                print(f" {label:12}: Not found in the dataset")
                spreadsheet_output.append("Not found in the dataset")
            else:
                val = c * scale
                print(f" {label:12}: {val:.2f}")
                spreadsheet_output.append(f"{val:.2f}")

    # ΔR VARIABLES
    elif var in dr_vars:
        ranges = [
            ("<0.4", "x < 0.4"),
            ("≥0.4", "x >= 0.4")
        ]
        for label, cond in ranges:
            c = count_vector(df, var, cond)
            if c is None:
                print(f" {label:12}: Not found in the dataset")
                spreadsheet_output.append("Not found in the dataset")
            else:
                val = c * scale
                print(f" {label:12}: {val:.2f}")
                spreadsheet_output.append(f"{val:.2f}")

    # PU VARIABLES
    elif var in pu_vars:
        ranges = [
            ("0-40",   "x >= 0 && x <= 40"),
            ("41-60",  "x > 40 && x <= 60"),
            (">60",    "x > 60")
        ]
        for label, cond in ranges:
            c = count_vector(df, var, cond)
            if c is None:
                print(f" {label:12}: Not found in the dataset")
                spreadsheet_output.append("Not found in the dataset")
            else:
                val = c * scale
                print(f" {label:12}: {val:.2f}")
                spreadsheet_output.append(f"{val:.2f}")

    print()  # Blank line between variables

# ------------------------------------------
# Final spreadsheet output
# ------------------------------------------
print("\nResults (to be pasted on the spreadsheet):\n")
for line in spreadsheet_output:
    print(line)
