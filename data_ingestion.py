"""
data_ingestion.py
DAY 1 — Data Ingestion & Exploration
Capstone Project I – Mutual Fund Analytics
Author: Sanapathi Kalyani
"""

import os
import pandas as pd
import glob

# Folder paths
RAW_DATA_DIR  = "data/raw"
PROC_DATA_DIR = "data/processed"
REPORTS_DIR   = "reports"

os.makedirs(RAW_DATA_DIR,  exist_ok=True)
os.makedirs(PROC_DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR,   exist_ok=True)

# ── LOAD ALL 10 CSV FILES ─────────────────────────────
csv_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))
print(f"Found {len(csv_files)} CSV file(s) in data/raw/\n")

anomalies = []

for filepath in csv_files:
    filename = os.path.basename(filepath)
    print("=" * 60)
    print(f"  FILE: {filename}")
    print("=" * 60)

    try:
        df = pd.read_csv(filepath, low_memory=False)

        print(f"\n  Shape   : {df.shape}")
        print(f"\n  Dtypes  :\n{df.dtypes}")
        print(f"\n  Head    :\n{df.head()}")

        null_cols = df.isnull().sum()
        null_cols = null_cols[null_cols > 0]
        dup_count = df.duplicated().sum()

        if not null_cols.empty or dup_count > 0:
            note = (f"{filename}: {len(null_cols)} col(s) with nulls "
                    f"({list(null_cols.index)}); {dup_count} duplicate rows")
            anomalies.append(note)
            print(f"\n  ANOMALY: {note}")
        else:
            print(f"\n  No anomalies in {filename}.")

    except Exception as e:
        msg = f"{filename}: Read error — {e}"
        anomalies.append(msg)
        print(f"\n  ERROR: {msg}")

# ── EXPLORE FUND MASTER ───────────────────────────────
fund_master_files = [f for f in csv_files if "fund_master" in f.lower()]

if fund_master_files:
    print("\n" + "=" * 60)
    print("  FUND MASTER EXPLORATION")
    print("=" * 60)

    fm = pd.read_csv(fund_master_files[0], low_memory=False)
    fm.columns = fm.columns.str.strip().str.lower().str.replace(" ", "_")
    print(f"\nTotal schemes: {len(fm)}")

    for col in ["fund_house", "amc", "amc_name"]:
        if col in fm.columns:
            print(f"\nUnique Fund Houses ({fm[col].nunique()}):\n{fm[col].unique()}")
            break

    for col in ["category", "scheme_category"]:
        if col in fm.columns:
            print(f"\nUnique Categories ({fm[col].nunique()}):\n{fm[col].unique()}")
            break

    for col in ["sub_category", "scheme_sub_category"]:
        if col in fm.columns:
            print(f"\nUnique Sub-Categories ({fm[col].nunique()}):\n{fm[col].unique()}")
            break

    for col in ["risk_grade", "risk", "riskometer"]:
        if col in fm.columns:
            print(f"\nUnique Risk Grades ({fm[col].nunique()}):\n{fm[col].unique()}")
            break

# ── VALIDATE AMFI CODES ───────────────────────────────
nav_files = [f for f in csv_files if "nav_history" in f.lower()]

if fund_master_files and nav_files:
    print("\n" + "=" * 60)
    print("  AMFI CODE VALIDATION")
    print("=" * 60)

    fm  = pd.read_csv(fund_master_files[0], low_memory=False)
    nav = pd.read_csv(nav_files[0],         low_memory=False)
    fm.columns  = fm.columns.str.strip().str.lower().str.replace(" ", "_")
    nav.columns = nav.columns.str.strip().str.lower().str.replace(" ", "_")

    for col in ["scheme_code", "amfi_code", "code"]:
        if col in fm.columns and col in nav.columns:
            fm_codes  = set(fm[col].dropna().astype(str))
            nav_codes = set(nav[col].dropna().astype(str))
            missing   = fm_codes - nav_codes
            print(f"\n  Fund Master codes  : {len(fm_codes)}")
            print(f"  NAV History codes  : {len(nav_codes)}")
            print(f"  Missing codes      : {len(missing)}")
            if missing:
                print(f"  Sample missing     : {list(missing)[:10]}")
                anomalies.append(f"{len(missing)} AMFI codes missing from nav_history")
            else:
                print("  All AMFI codes validated successfully!")
            break

# ── WRITE DATA QUALITY SUMMARY ────────────────────────
summary_file = os.path.join(REPORTS_DIR, "data_quality_summary.txt")
with open(summary_file, "w") as f:
    f.write("DATA QUALITY SUMMARY — DAY 1\n")
    f.write("Capstone Project I: Mutual Fund Analytics\n")
    f.write("Author: Sanapathi Kalyani\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Total CSV files loaded   : {len(csv_files)}\n")
    f.write(f"Total anomalies detected : {len(anomalies)}\n\n")
    if anomalies:
        f.write("Anomaly Details:\n")
        for i, issue in enumerate(anomalies, 1):
            f.write(f"  {i}. {issue}\n")
    else:
        f.write("All datasets are clean. No anomalies found.\n")

print(f"\nData quality summary saved to: {summary_file}")
print("\ndata_ingestion.py completed successfully!")