-- queries.sql
-- DAY 2 — 10 Analytical SQL Queries
-- Capstone Project I: Mutual Fund Analytics
-- Author: Sanapathi Kalyani

-- ── Query 1: Top 5 Funds by AUM ──────────────────────────
SELECT
    d.scheme_name,
    d.fund_house,
    ROUND(SUM(a.aum_crores), 2) AS total_aum_crores
FROM fact_aum a
JOIN dim_fund d ON a.scheme_code = d.scheme_code
GROUP BY d.scheme_code
ORDER BY total_aum_crores DESC
LIMIT 5;

-- ── Query 2: Average NAV Per Month ───────────────────────
SELECT
    scheme_code,
    strftime('%Y-%m', nav_date) AS month,
    ROUND(AVG(nav_value), 2)   AS avg_nav
FROM fact_nav
GROUP BY scheme_code, month
ORDER BY scheme_code, month;

-- ── Query 3: SIP Year-on-Year Growth ─────────────────────
SELECT
    strftime('%Y', transaction_date) AS year,
    ROUND(SUM(amount), 2)            AS total_sip_amount,
    COUNT(*)                         AS total_transactions
FROM fact_transactions
WHERE transaction_type = 'Sip'
GROUP BY year
ORDER BY year;

-- ── Query 4: Transactions by State ───────────────────────
SELECT
    state,
    COUNT(*)              AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- ── Query 5: Funds with Expense Ratio < 1% ───────────────
SELECT
    d.scheme_name,
    d.fund_house,
    d.scheme_category,
    p.expense_ratio
FROM fact_performance p
JOIN dim_fund d ON p.scheme_code = d.scheme_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- ── Query 6: Top 5 Funds by 3-Year Returns ───────────────
SELECT
    d.scheme_name,
    d.fund_house,
    ROUND(p.return_3yr, 2) AS return_3yr_pct
FROM fact_performance p
JOIN dim_fund d ON p.scheme_code = d.scheme_code
WHERE p.return_3yr IS NOT NULL
ORDER BY p.return_3yr DESC
LIMIT 5;

-- ── Query 7: Monthly SIP Inflow Trend ────────────────────
SELECT
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(*)                             AS sip_count,
    ROUND(SUM(amount), 2)               AS total_inflow
FROM fact_transactions
WHERE transaction_type = 'Sip'
GROUP BY month
ORDER BY month;

-- ── Query 8: KYC Status Distribution ─────────────────────
SELECT
    kyc_status,
    COUNT(*) AS investor_count,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM fact_transactions), 2) AS percentage
FROM fact_transactions
GROUP BY kyc_status;

-- ── Query 9: NAV Growth for HDFC Top 100 ─────────────────
SELECT
    nav_date,
    nav_value,
    ROUND(nav_value - LAG(nav_value) OVER
          (ORDER BY nav_date), 2) AS daily_change
FROM fact_nav
WHERE scheme_code = 125497
ORDER BY nav_date DESC
LIMIT 365;

-- ── Query 10: Category-wise Average Returns ───────────────
SELECT
    d.scheme_category,
    ROUND(AVG(p.return_1yr), 2) AS avg_1yr_return,
    ROUND(AVG(p.return_3yr), 2) AS avg_3yr_return,
    ROUND(AVG(p.return_5yr), 2) AS avg_5yr_return,
    COUNT(*)                     AS fund_count
FROM fact_performance p
JOIN dim_fund d ON p.scheme_code = d.scheme_code
GROUP BY d.scheme_category
ORDER BY avg_3yr_return DESC;