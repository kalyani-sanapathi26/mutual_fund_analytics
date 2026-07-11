# 📊 Bluestock Mutual Fund Analytics — Capstone Project I

> **Bluestock Fintech Internship | Data Science Intern**  
> Duration: 20 June 2026 – 14 July 2026 | Intern: Kalyani Sanapathi

---

## 🧭 Project Overview

End-to-end **Mutual Fund Intelligence Platform** covering the complete data lifecycle — from raw NAV ingestion via the `mfapi.in` API, through ETL and SQLite storage, exploratory analysis with 15+ charts, fund performance metrics (Sharpe Ratio, Beta, VaR/CVaR), advanced risk analytics, a 4-page interactive Power BI dashboard, and a rule-based fund recommender system.

---

## 🗂️ Repository Structure

---

## ⚙️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Database | SQLite (via sqlite3) |
| Dashboard | Power BI Desktop |
| Notebooks | Jupyter Notebook |
| Version Control | Git & GitHub |
| Data Source | [mfapi.in](https://mfapi.in) |

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/kalyani-sanapathi26/mutual_fund_analytics.git
cd mutual_fund_analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run ETL pipeline
python data_ingestion.py
python data_cleaning.py
python db_loader.py

# 4. Run notebooks in order (Jupyter)
# EDA_Analysis.ipynb → Fund_Performance_Analytics.ipynb → Advanced_Analytics.ipynb

# 5. Open Power BI dashboard
# Open: dashboard/bluestock_mf_dashboard.pbix in Power BI Desktop
```

---

## 📋 Deliverables Status

| ID | Deliverable | File | Status |
|---|---|---|---|
| D1 | ETL Pipeline | `data_ingestion.py`, `data_cleaning.py`, `db_loader.py` | ✅ |
| D2 | SQLite Database | `sql/schema.sql` + `bluestock_mf.db` | ✅ |
| D3 | EDA Notebook (15+ charts) | `notebooks/EDA_Analysis.ipynb` | ✅ |
| D4 | Performance Metrics | `notebooks/Fund_Performance_Analytics.ipynb` + CSVs | ✅ |
| D5 | Interactive Dashboard (4 pages) | `dashboard/bluestock_mf_dashboard.pbix` | ✅ |
| D6 | Advanced Analytics | `advanced_analytics/Advanced_Analytics.ipynb` | ✅ |
| D7 | Final Report + Slides | `reports/Final_Report.pdf` + `reports/Presentation.pptx` | ✅ |

---

## 📊 Power BI Dashboard — 4 Pages

| Page | Title | Slicers |
|---|---|---|
| 1 | Industry Overview | Fund Category, Fund House |
| 2 | Fund Performance | Date Range, Fund Category |
| 3 | Investor Analytics | Fund Category, Risk Level |
| 4 | SIP & Market Trends | SIP Amount, Investment Period |

---

## 📈 Key Findings

- Large-cap equity funds delivered Sharpe Ratios above 1.2 over a 3-year period
- Debt funds showed Beta < 0.3 vs. Small-cap funds with Beta > 1.1
- At 95% confidence, equity VaR ranged -1.8% to -3.2% daily; debt capped at -0.5%
- SIP in multi-cap funds outperformed lump-sum investments initiated at market peaks
- Funds with expense ratio > 1.5% showed measurably lower net CAGR
- Recommender classified 45% Moderate, 35% Aggressive, 20% Conservative funds

---

## 👩‍💻 Author

**Kalyani Sanapathi** — Data Science Intern, Bluestock Fintech  
GitHub: [@kalyani-sanapathi26](https://github.com/kalyani-sanapathi26)  
Period: 20 June 2026 – 14 July 2026
