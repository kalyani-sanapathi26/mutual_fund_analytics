-- schema.sql
-- DAY 2 — SQLite Star Schema
-- Capstone Project I: Mutual Fund Analytics
-- Author: Sanapathi Kalyani

-- ─────────────────────────────────────────
-- DIMENSION TABLES
-- ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS dim_fund (
    scheme_code     INTEGER PRIMARY KEY,
    scheme_name     TEXT    NOT NULL,
    fund_house      TEXT,
    scheme_type     TEXT,
    scheme_category TEXT,
    sub_category    TEXT,
    risk_grade      TEXT,
    benchmark       TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date       DATE    NOT NULL UNIQUE,
    day             INTEGER,
    month           INTEGER,
    month_name      TEXT,
    quarter         INTEGER,
    year            INTEGER,
    is_weekend      INTEGER  -- 0 = weekday, 1 = weekend
);

-- ─────────────────────────────────────────
-- FACT TABLES
-- ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code     INTEGER NOT NULL,
    nav_date        DATE    NOT NULL,
    nav_value       REAL    NOT NULL CHECK (nav_value > 0),
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT,
    scheme_code         INTEGER NOT NULL,
    transaction_date    DATE,
    transaction_type    TEXT    CHECK (transaction_type IN ('Sip','Lumpsum','Redemption')),
    amount              REAL    CHECK (amount > 0),
    units               REAL,
    nav_at_transaction  REAL,
    kyc_status          TEXT    CHECK (kyc_status IN ('Verified','Pending','Rejected')),
    state               TEXT,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code     INTEGER NOT NULL,
    as_of_date      DATE,
    return_1yr      REAL,
    return_3yr      REAL,
    return_5yr      REAL,
    expense_ratio   REAL    CHECK (expense_ratio BETWEEN 0.1 AND 2.5),
    sharpe_ratio    REAL,
    alpha           REAL,
    beta            REAL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code     INTEGER NOT NULL,
    aum_date        DATE,
    aum_crores      REAL    CHECK (aum_crores >= 0),
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);