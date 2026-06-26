# Data Dictionary
## Capstone Project I – Mutual Fund Analytics
**Author:** Sanapathi Kalyani | **Date:** June 2026

---

## Table: dim_fund
| Column | Data Type | Description |
|---|---|---|
| scheme_code | INTEGER (PK) | Unique AMFI scheme code |
| scheme_name | TEXT | Full name of the mutual fund scheme |
| fund_house | TEXT | Name of the Asset Management Company (AMC) |
| scheme_type | TEXT | Type: Open-ended / Close-ended |
| scheme_category | TEXT | Category: Equity, Debt, Hybrid, etc. |
| sub_category | TEXT | Sub-category: Large Cap, Mid Cap, etc. |
| risk_grade | TEXT | Risk level: Low, Moderate, High |

---

## Table: fact_nav
| Column | Data Type | Description |
|---|---|---|
| scheme_code | INTEGER (FK) | References dim_fund.scheme_code |
| nav_date | DATE | Date of NAV value |
| nav_value | REAL | Net Asset Value in INR (must be > 0) |

---

## Table: fact_transactions
| Column | Data Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| scheme_code | INTEGER (FK) | References dim_fund.scheme_code |
| transaction_date | DATE | Date of the transaction |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount | REAL | Transaction amount in INR (must be > 0) |
| units | REAL | Number of units purchased/redeemed |
| nav_at_transaction | REAL | NAV at the time of transaction |
| kyc_status | TEXT | KYC status: Verified / Pending / Rejected |
| state | TEXT | Indian state of the investor |

---

## Table: fact_performance
| Column | Data Type | Description |
|---|---|---|
| scheme_code | INTEGER (FK) | References dim_fund.scheme_code |
| as_of_date | DATE | Date of performance measurement |
| return_1yr | REAL | 1-year return percentage |
| return_3yr | REAL | 3-year CAGR return percentage |
| return_5yr | REAL | 5-year CAGR return percentage |
| expense_ratio | REAL | Annual expense ratio % (range: 0.1–2.5%) |
| sharpe_ratio | REAL | Risk-adjusted return measure |
| alpha | REAL | Excess return over benchmark |
| beta | REAL | Volatility relative to market |

---

## Table: fact_aum
| Column | Data Type | Description |
|---|---|---|
| scheme_code | INTEGER (FK) | References dim_fund.scheme_code |
| aum_date | DATE | Date of AUM measurement |
| aum_crores | REAL | Assets Under Management in INR Crores |

---

## Source Files
| File | Source | Records |
|---|---|---|
| 01_fund_master.csv | Bluestock Dataset | 40 |
| 02_nav_history.csv | Bluestock Dataset | 46,000 |
| 03_aum_by_fund_house.csv | Bluestock Dataset | 90 |
| 07_scheme_performance.csv | Bluestock Dataset | 40 |
| 08_investor_transactions.csv | Bluestock Dataset | 32,778 |