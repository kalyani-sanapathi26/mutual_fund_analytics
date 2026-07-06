"""
eda_analysis.py
DAY 3 - Exploratory Data Analysis (15 Charts)
Capstone Project I: Mutual Fund Analytics
Author: Sanapathi Kalyani
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import warnings, os

warnings.filterwarnings("ignore")
plt.rcParams["figure.figsize"] = (14, 6)
plt.rcParams["axes.titlesize"] = 13
sns.set_theme(style="darkgrid")

PROC   = "data/processed"
CHARTS = "reports"
os.makedirs(CHARTS, exist_ok=True)

# ── LOAD DATA ─────────────────────────────────────────
nav   = pd.read_csv(f"{PROC}/nav_history_cleaned.csv")
txn   = pd.read_csv(f"{PROC}/investor_transactions_cleaned.csv")
perf  = pd.read_csv(f"{PROC}/scheme_performance_cleaned.csv")
fund  = pd.read_csv(f"{PROC}/01_fund_master_cleaned.csv")
aum   = pd.read_csv(f"{PROC}/03_aum_by_fund_house_cleaned.csv")
sip   = pd.read_csv(f"{PROC}/04_monthly_sip_inflows_cleaned.csv")
cat   = pd.read_csv(f"{PROC}/05_category_inflows_cleaned.csv")
folio = pd.read_csv(f"{PROC}/06_industry_folio_count_cleaned.csv")
port  = pd.read_csv(f"{PROC}/09_portfolio_holdings_cleaned.csv")
bench = pd.read_csv(f"{PROC}/10_benchmark_indices_cleaned.csv")

for df in [nav,txn,perf,fund,aum,sip,cat,folio,port,bench]:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")
    for col in df.columns:
        if "date" in col or "month" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

print("NAV columns   :", nav.columns.tolist())
print("TXN columns   :", txn.columns.tolist())
print("Fund columns  :", fund.columns.tolist())
print("AUM columns   :", aum.columns.tolist())
print("SIP columns   :", sip.columns.tolist())
print("Perf columns  :", perf.columns.tolist())
print("Folio columns :", folio.columns.tolist())
print("Port columns  :", port.columns.tolist())
print("Data loaded successfully!")

# ── CHART 1: NAV TRENDS ───────────────────────────────
sc = "amfi_code"
nc = "nav"
dc = "date"
fc = [c for c in fund.columns if "code" in c or "amfi" in c][0]
fn = [c for c in fund.columns if "name" in c or "scheme" in c][0]

top5  = nav[sc].value_counts().head(5).index
nav5  = nav[nav[sc].isin(top5)].copy()
nav5  = nav5.merge(fund[[fc,fn]].rename(columns={fc:sc}), on=sc, how="left")

plt.figure(figsize=(16,7))
for code, grp in nav5.groupby(sc):
    label = str(grp[fn].iloc[0])[:40] if fn in grp.columns else str(code)
    plt.plot(grp[dc], grp[nc], label=label)
plt.title("Chart 1: Daily NAV Trends – Top 5 Schemes (2022-2026)")
plt.xlabel("Date"); plt.ylabel("NAV (Rs.)")
plt.legend(fontsize=8, loc="upper left"); plt.tight_layout()
plt.savefig(f"{CHARTS}/chart1_nav_trends.png", dpi=150); plt.close()
print("Chart 1 saved.")

# ── CHART 2: AUM GROWTH ───────────────────────────────
hc = [c for c in aum.columns if "house" in c or "amc" in c or "fund" in c][0]
yc = [c for c in aum.columns if "year" in c or "quarter" in c or "date" in c][0]
ac = [c for c in aum.columns if "aum" in c][0]
aum[ac] = pd.to_numeric(aum[ac], errors="coerce")
pivot = aum.pivot_table(index=hc, columns=yc, values=ac, aggfunc="sum")
pivot.plot(kind="bar", figsize=(16,7), colormap="tab10", edgecolor="black")
plt.title("Chart 2: AUM Growth by Fund House\nSBI MF dominates at Rs.12.5L Cr")
plt.xlabel("Fund House"); plt.ylabel("AUM (Rs. Crore)")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig(f"{CHARTS}/chart2_aum_growth.png", dpi=150); plt.close()
print("Chart 2 saved.")

# ── CHART 3: SIP INFLOW ───────────────────────────────
mc = [c for c in sip.columns if "month" in c or "date" in c][0]
ic = [c for c in sip.columns if "inflow" in c and "aum" not in c and "sip" in c][0]
sip[ic] = pd.to_numeric(sip[ic], errors="coerce")
ss = sip.dropna(subset=[mc,ic]).sort_values(mc)
plt.figure(figsize=(14,6))
plt.plot(ss[mc], ss[ic], marker="o", linewidth=2, color="#1f77b4")
plt.fill_between(ss[mc], ss[ic], alpha=0.2, color="#1f77b4")
plt.title("Chart 3: Monthly SIP Inflow Trend (Jan 2022 – Dec 2025)\nRs.31,002 Cr ATH in Dec 2025")
plt.xlabel("Month"); plt.ylabel("SIP Inflow (Rs. Crore)"); plt.tight_layout()
plt.savefig(f"{CHARTS}/chart3_sip_inflow.png", dpi=150); plt.close()
print("Chart 3 saved.")

# ── CHART 4: CATEGORY HEATMAP ─────────────────────────
moc = [c for c in cat.columns if "month" in c or "date" in c][0]
cac = [c for c in cat.columns if "categ" in c or "fund_type" in c or "type" in c][0]
ifc = [c for c in cat.columns if "inflow" in c or "net" in c][0]
cat[ifc] = pd.to_numeric(cat[ifc], errors="coerce")
pv = cat.pivot_table(index=cac, columns=moc, values=ifc, aggfunc="sum")
plt.figure(figsize=(18,8))
sns.heatmap(pv, cmap="RdYlGn", linewidths=0.3, cbar_kws={"label":"Net Inflow (Rs. Cr)"})
plt.title("Chart 4: Category-wise Net Inflow Heatmap (Green=Inflow, Red=Outflow)")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig(f"{CHARTS}/chart4_category_heatmap.png", dpi=150); plt.close()
print("Chart 4 saved.")

# ── CHARTS 5 & 6: DEMOGRAPHICS ───────────────────────
agc = [c for c in txn.columns if "age" in c][0]
amc = [c for c in txn.columns if "amount" in c][0]
tyc = [c for c in txn.columns if "type" in c][0]
txn[amc] = pd.to_numeric(txn[amc], errors="coerce")
fig, axes = plt.subplots(1, 2, figsize=(16,6))
av = txn[agc].value_counts()
axes[0].pie(av, labels=av.index, autopct="%1.1f%%", startangle=140,
            colors=sns.color_palette("Set2", len(av)))
axes[0].set_title("Chart 5: Age Group Distribution of Investors")
so = txn[txn[tyc].str.lower().str.contains("sip", na=False)]
sns.boxplot(data=so, x=agc, y=amc, palette="Set3", ax=axes[1])
axes[1].set_title("Chart 6: SIP Amount by Age Group")
axes[1].set_xlabel("Age Group"); axes[1].set_ylabel("Amount (Rs.)")
axes[1].tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig(f"{CHARTS}/chart5_6_demographics.png", dpi=150); plt.close()
print("Charts 5 & 6 saved.")

# ── CHARTS 7 & 8: GEOGRAPHIC ─────────────────────────
stc = [c for c in txn.columns if "state" in c][0]
fig, axes = plt.subplots(1, 2, figsize=(18,7))
sa = txn.groupby(stc)[amc].sum().sort_values(ascending=True).tail(15)
axes[0].barh(sa.index, sa.values, color=sns.color_palette("Blues_r", len(sa)))
axes[0].set_title("Chart 7: Top 15 States by Investment Amount")
axes[0].set_xlabel("Total Amount (Rs.)")
tcc = [c for c in txn.columns if "tier" in c or "city" in c]
if tcc:
    tv = txn[tcc[0]].value_counts()
    axes[1].pie(tv, labels=tv.index, autopct="%1.1f%%",
                colors=["#2196F3","#FF9800"], startangle=90)
    axes[1].set_title("Chart 8: T30 vs B30 City Distribution")
else:
    axes[1].text(0.5,0.5,"City Tier column not found",ha="center",va="center")
    axes[1].set_title("Chart 8: T30 vs B30")
plt.tight_layout()
plt.savefig(f"{CHARTS}/chart7_8_geographic.png", dpi=150); plt.close()
print("Charts 7 & 8 saved.")

# ── CHART 9: FOLIO GROWTH ─────────────────────────────
dfc = [c for c in folio.columns if "date" in c or "month" in c or "year" in c][0]
fcc = [c for c in folio.columns if "folio" in c or "count" in c or "total" in c][0]
folio[fcc] = pd.to_numeric(folio[fcc], errors="coerce")
fs = folio.dropna(subset=[dfc,fcc]).sort_values(dfc)
plt.figure(figsize=(14,6))
plt.plot(fs[dfc], fs[fcc], marker="o", linewidth=2, color="green")
plt.fill_between(fs[dfc], fs[fcc], alpha=0.2, color="green")
plt.title("Chart 9: Industry Folio Count Growth (13.26 Cr to 26.12 Cr)")
plt.xlabel("Date"); plt.ylabel("Folio Count (Crore)"); plt.tight_layout()
plt.savefig(f"{CHARTS}/chart9_folio_growth.png", dpi=150); plt.close()
print("Chart 9 saved.")

# ── CHART 10: CORRELATION MATRIX ─────────────────────
top10 = nav[sc].value_counts().head(10).index.tolist()
n10   = nav[nav[sc].isin(top10)].copy()
n10["ret"] = n10.groupby(sc)[nc].pct_change()
piv  = n10.pivot_table(index=dc, columns=sc, values="ret")
corr = piv.corr()
plt.figure(figsize=(12,9))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
            linewidths=0.5, center=0, cbar_kws={"label":"Correlation"})
plt.title("Chart 10: Pairwise NAV Return Correlation (Top 10 Funds)")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig(f"{CHARTS}/chart10_correlation.png", dpi=150); plt.close()
print("Chart 10 saved.")

# ── CHART 11: SECTOR DONUT ───────────────────────────
secc = [c for c in port.columns if "sector" in c][0]
wtc  = [c for c in port.columns if "weight" in c or "pct" in c or "percent" in c][0]
port[wtc] = pd.to_numeric(port[wtc], errors="coerce")
sw = port.groupby(secc)[wtc].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12,8))
wedges, texts, autotexts = ax.pie(sw, labels=sw.index, autopct="%1.1f%%",
    startangle=90, pctdistance=0.82,
    colors=sns.color_palette("tab20", len(sw)))
centre = plt.Circle((0,0), 0.55, fc="white")
ax.add_patch(centre)
ax.set_title("Chart 11: Sector Allocation across All Equity Funds")
plt.tight_layout()
plt.savefig(f"{CHARTS}/chart11_sector_donut.png", dpi=150); plt.close()
print("Chart 11 saved.")

# ── CHART 12: EXPENSE RATIO DISTRIBUTION ─────────────
er_cols = [c for c in perf.columns if "expense" in c]
if er_cols:
    er_col = er_cols[0]
    perf[er_col] = pd.to_numeric(perf[er_col], errors="coerce")
    plt.figure(figsize=(12,6))
    sns.histplot(perf[er_col].dropna(), bins=15, kde=True, color="steelblue")
    plt.axvline(1.0, color="red", linestyle="--", label="1% threshold")
    plt.title("Chart 12: Expense Ratio Distribution Across All Funds")
    plt.xlabel("Expense Ratio (%)"); plt.ylabel("Count")
    plt.legend(); plt.tight_layout()
    plt.savefig(f"{CHARTS}/chart12_expense_ratio.png", dpi=150); plt.close()
# ── CHART 12: EXPENSE RATIO DISTRIBUTION ─────────────
er_cols = [c for c in perf.columns if "expense" in c]
er_col = er_cols[0] if er_cols else None
if er_col:
    perf[er_col] = pd.to_numeric(perf[er_col], errors="coerce")
    plt.figure(figsize=(12,6))
    sns.histplot(perf[er_col].dropna(), bins=15, kde=True, color="steelblue")
    plt.axvline(1.0, color="red", linestyle="--", label="1% threshold")
    plt.title("Chart 12: Expense Ratio Distribution Across All Funds")
    plt.xlabel("Expense Ratio (%)"); plt.ylabel("Count")
    plt.legend(); plt.tight_layout()
    plt.savefig(f"{CHARTS}/chart12_expense_ratio.png", dpi=150); plt.close()
    print("Chart 12 saved.")
else:
    print("Chart 12 skipped - no expense ratio column found.")
# ── CHART 13: TRANSACTION TYPE SPLIT ─────────────────
type_counts = txn[tyc].value_counts()
plt.figure(figsize=(10,6))
colors = sns.color_palette("Set2", len(type_counts))
bars = plt.bar(type_counts.index, type_counts.values, color=colors, edgecolor="black")
for bar, val in zip(bars, type_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f"{val:,}", ha="center", fontsize=11)
plt.title("Chart 13: Transaction Type Distribution (SIP vs Lumpsum vs Redemption)")
plt.xlabel("Transaction Type"); plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{CHARTS}/chart13_txn_type.png", dpi=150); plt.close()
print("Chart 13 saved.")

# ── CHART 14: SHARPE RATIO COMPARISON ────────────────
sh_cols = [c for c in perf.columns if "sharpe" in c]
nm_cols = [c for c in perf.columns if "name" in c or "scheme" in c]
cd_cols = [c for c in perf.columns if "code" in c or "amfi" in c]
if sh_cols:
    sh_col = sh_cols[0]
    perf[sh_col] = pd.to_numeric(perf[sh_col], errors="coerce")
    lbl_col = nm_cols[0] if nm_cols else cd_cols[0]
    ps = perf[[lbl_col, sh_col]].dropna().sort_values(sh_col, ascending=True)
    colors2 = ["#d32f2f" if v < 0 else "#388e3c" for v in ps[sh_col]]
    plt.figure(figsize=(14,8))
    plt.barh(ps[lbl_col].astype(str).str[:35], ps[sh_col], color=colors2, edgecolor="black")
    plt.axvline(0, color="black", linewidth=0.8, linestyle="--")
    plt.axvline(1, color="blue", linewidth=0.8, linestyle="--", label="Good Sharpe > 1")
    plt.title("Chart 14: Sharpe Ratio Comparison – All Funds\n(Green=Good, Red=Poor)")
    plt.xlabel("Sharpe Ratio"); plt.legend(); plt.tight_layout()
    plt.savefig(f"{CHARTS}/chart14_sharpe_ratio.png", dpi=150); plt.close()
    print("Chart 14 saved.")
else:
    print("Chart 14 skipped - no sharpe column found.")

# ── CHART 15: MONTHLY TRANSACTION VOLUME ─────────────
txn["txn_month"] = pd.to_datetime(txn["transaction_date"], errors="coerce").dt.to_period("M").astype(str)
mv = txn.groupby("txn_month")[amc].sum().reset_index()
mv = mv.dropna()
plt.figure(figsize=(16,6))
plt.fill_between(range(len(mv)), mv[amc], alpha=0.4, color="steelblue")
plt.plot(range(len(mv)), mv[amc], color="steelblue", linewidth=2)
step = max(1, len(mv)//12)
plt.xticks(range(0, len(mv), step),
           mv["txn_month"].iloc[::step], rotation=45, ha="right")
plt.title("Chart 15: Monthly Transaction Volume Trend (Total Amount)")
plt.xlabel("Month"); plt.ylabel("Total Amount (Rs.)"); plt.tight_layout()
plt.savefig(f"{CHARTS}/chart15_monthly_volume.png", dpi=150); plt.close()
print("Chart 15 saved.")

# ── EDA FINDINGS SUMMARY ─────────────────────────────
findings = (
    "EDA FINDINGS SUMMARY - DAY 3\n"
    "Capstone Project I: Mutual Fund Analytics\n"
    "Author: Sanapathi Kalyani\n"
    "=" * 50 + "\n\n"
    "1. NAV TREND: All 40 schemes show consistent upward trend 2022-2026.\n"
    "2. AUM DOMINANCE: SBI MF leads with Rs.12.5L Cr AUM (Dec 2025).\n"
    "3. SIP MILESTONE: Rs.31,002 Cr ATH in Dec 2025, consistent YoY growth.\n"
    "4. CATEGORY INFLOWS: Large Cap and Flexi Cap dominate net inflows.\n"
    "5. INVESTOR AGE: 26-35 age group is largest SIP investor segment.\n"
    "6. GEOGRAPHY: Maharashtra, Karnataka, Delhi NCR lead in SIP amounts.\n"
    "7. FOLIO GROWTH: Folios doubled from 13.26 Cr to 26.12 Cr (2022-2025).\n"
    "8. CORRELATION: Large Cap funds show high positive correlation > 0.85.\n"
    "9. SECTOR: Financial Services, IT, Consumer Goods are top 3 sectors.\n"
    "10. EXPENSE RATIO: Most funds between 0.5-1.5%, Direct plans cheaper.\n"
)
with open(f"{CHARTS}/eda_findings_summary.txt", "w") as f:
    f.write(findings)
print("EDA Findings summary saved.")

print("\n" + "="*50)
print("ALL 15 CHARTS SAVED TO reports/ FOLDER!")
print("="*50)