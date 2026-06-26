"""
data_cleaning.py
DAY 2 — Data Cleaning
Capstone Project I – Mutual Fund Analytics
Author: Sanapathi Kalyani
"""

import os
import pandas as pd
import numpy as np

RAW_DIR  = "data/raw"
PROC_DIR = "data/processed"
os.makedirs(PROC_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────
# HELPER — save cleaned file
# ─────────────────────────────────────────────────────
def save_cleaned(df, filename):
    path = os.path.join(PROC_DIR, filename)
    df.to_csv(path, index=False)
    print(f"  SAVED: {path}  ({len(df)} rows)")


# ─────────────────────────────────────────────────────
# 1. CLEAN nav_history.csv
# ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("  CLEANING: nav_history.csv")
print("="*60)

nav = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"), low_memory=False)
nav.columns = nav.columns.str.strip().str.lower().str.replace(" ", "_")
print(f"  Original shape : {nav.shape}")

# Parse date column
date_col = [c for c in nav.columns if "date" in c][0]
nav[date_col] = pd.to_datetime(nav[date_col], dayfirst=True, errors="coerce")

# Sort by scheme_code + date
code_col = [c for c in nav.columns if "code" in c][0]
nav = nav.sort_values([code_col, date_col]).reset_index(drop=True)

# Remove duplicates
nav = nav.drop_duplicates(subset=[code_col, date_col])

# NAV column — find it
nav_col = [c for c in nav.columns if "nav" in c][0]
nav[nav_col] = pd.to_numeric(nav[nav_col], errors="coerce")

# Forward-fill missing NAV (for holidays/weekends)
nav[nav_col] = nav.groupby(code_col)[nav_col].ffill()

# Validate NAV > 0
before = len(nav)
nav = nav[nav[nav_col] > 0]
print(f"  Removed {before - len(nav)} rows with NAV <= 0")

print(f"  Cleaned shape  : {nav.shape}")
save_cleaned(nav, "nav_history_cleaned.csv")


# ─────────────────────────────────────────────────────
# 2. CLEAN investor_transactions.csv
# ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("  CLEANING: investor_transactions.csv")
print("="*60)

txn = pd.read_csv(os.path.join(RAW_DIR, "08_investor_transactions.csv"), low_memory=False)
txn.columns = txn.columns.str.strip().str.lower().str.replace(" ", "_")
print(f"  Original shape : {txn.shape}")

# Standardize transaction_type
txn_col = [c for c in txn.columns if "type" in c or "transaction" in c][0]
txn[txn_col] = txn[txn_col].str.strip().str.title()
# Print actual values to understand the data
print(f"  All unique values in {txn_col}: {txn[txn_col].unique()[:10]}")

# Extended valid types
valid_types = ["Sip", "Lumpsum", "Redemption", "Purchase", "Switch", "Dividend"]
before = len(txn)
filtered = txn[txn[txn_col].isin(valid_types)]

# If filtering removes all rows, keep original data as-is
if len(filtered) == 0:
    print(f"  WARNING: No matching transaction types. Keeping all {before} rows.")
else:
    txn = filtered
    print(f"  Kept {len(txn)} rows after transaction type filter.")

# Fix date formats
for col in txn.columns:
    if "date" in col:
        txn[col] = pd.to_datetime(txn[col], dayfirst=True, errors="coerce")

# Validate amount > 0
amt_col = [c for c in txn.columns if "amount" in c][0]
txn[amt_col] = pd.to_numeric(txn[amt_col], errors="coerce")
before = len(txn)
txn = txn[txn[amt_col] > 0]
print(f"  Removed {before - len(txn)} rows with amount <= 0")

# Check KYC status enum
if "kyc_status" in txn.columns:
    valid_kyc = ["Verified", "Pending", "Rejected"]
    txn["kyc_status"] = txn["kyc_status"].str.strip().str.title()
    print(f"  KYC values: {txn['kyc_status'].unique()}")

# Remove duplicates
txn = txn.drop_duplicates()
print(f"  Cleaned shape  : {txn.shape}")
save_cleaned(txn, "investor_transactions_cleaned.csv")


# ─────────────────────────────────────────────────────
# 3. CLEAN scheme_performance.csv
# ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("  CLEANING: scheme_performance.csv")
print("="*60)

perf = pd.read_csv(os.path.join(RAW_DIR, "07_scheme_performance.csv"), low_memory=False)
perf.columns = perf.columns.str.strip().str.lower().str.replace(" ", "_")
print(f"  Original shape : {perf.shape}")

# Validate return columns are numeric
return_cols = [c for c in perf.columns if "return" in c or "1yr" in c or "3yr" in c or "5yr" in c]
for col in return_cols:
    perf[col] = pd.to_numeric(perf[col], errors="coerce")

# Flag anomalies (returns outside -100% to +200%)
for col in return_cols:
    anomalies = perf[(perf[col] < -100) | (perf[col] > 200)]
    if len(anomalies) > 0:
        print(f"  FLAG: {len(anomalies)} anomalies in {col}")

# Validate expense_ratio range 0.1% to 2.5%
if "expense_ratio" in perf.columns:
    perf["expense_ratio"] = pd.to_numeric(perf["expense_ratio"], errors="coerce")
    out_of_range = perf[(perf["expense_ratio"] < 0.1) | (perf["expense_ratio"] > 2.5)]
    print(f"  Expense ratio out of range (0.1–2.5%): {len(out_of_range)} rows")
    perf = perf[(perf["expense_ratio"] >= 0.1) & (perf["expense_ratio"] <= 2.5)]

# Remove duplicates
perf = perf.drop_duplicates()
print(f"  Cleaned shape  : {perf.shape}")
save_cleaned(perf, "scheme_performance_cleaned.csv")


# ─────────────────────────────────────────────────────
# 4. COPY REMAINING CSVs TO PROCESSED (cleaned as-is)
# ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("  COPYING remaining CSVs to data/processed/")
print("="*60)

already_cleaned = ["02_nav_history.csv", "08_investor_transactions.csv", "07_scheme_performance.csv"]
all_raw = [f for f in os.listdir(RAW_DIR) if f.endswith(".csv") and f not in already_cleaned
           and not f.startswith("nav_")]

for fname in all_raw:
    df = pd.read_csv(os.path.join(RAW_DIR, fname), low_memory=False)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.drop_duplicates()
    save_cleaned(df, fname.replace(".csv", "_cleaned.csv"))

print("\ndata_cleaning.py completed successfully!")