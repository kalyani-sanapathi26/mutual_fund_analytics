"""
db_loader.py
DAY 2 — Load Cleaned Data into SQLite
Capstone Project I – Mutual Fund Analytics
Author: Sanapathi Kalyani
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text

PROC_DIR = "data/processed"
DB_PATH  = "bluestock_mf.db"
SQL_FILE = "sql/schema.sql"

# Create SQLite engine
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
print(f"Connected to SQLite: {DB_PATH}")

# ── Run schema.sql to create tables ──────────────────
with open(SQL_FILE, "r") as f:
    schema_sql = f.read()

with engine.connect() as conn:
    for statement in schema_sql.split(";"):
        stmt = statement.strip()
        if stmt:
            conn.execute(text(stmt))
    conn.commit()
print("Schema created successfully.")

# ── Load cleaned CSVs into SQLite ─────────────────────
table_map = {
    "nav_history_cleaned.csv"              : "fact_nav",
    "investor_transactions_cleaned.csv"    : "fact_transactions",
    "scheme_performance_cleaned.csv"       : "fact_performance",
    "01_fund_master_cleaned.csv"           : "dim_fund",
    "03_aum_by_fund_house_cleaned.csv"     : "fact_aum",
}

for filename, table_name in table_map.items():
    filepath = os.path.join(PROC_DIR, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, low_memory=False)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"  Loaded {len(df):,} rows into table '{table_name}' from {filename}")
    else:
        print(f"  SKIPPED (file not found): {filename}")

# ── Verify row counts ────────────────────────────────
print("\n" + "="*50)
print("  ROW COUNT VERIFICATION")
print("="*50)
tables = ["dim_fund", "fact_nav", "fact_transactions", "fact_performance", "fact_aum"]
with engine.connect() as conn:
    for table in tables:
        try:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            print(f"  {table:<25}: {count:,} rows")
        except Exception as e:
            print(f"  {table:<25}: ERROR — {e}")

print("\ndb_loader.py completed successfully!")
# ── POPULATE dim_date TABLE ───────────────────────────
import sqlite3
from datetime import date, timedelta

print("\nPopulating dim_date table...")
start = date(2022, 1, 1)
end   = date(2026, 6, 30)
dates = []
current = start
while current <= end:
    dates.append({
        "full_date"  : str(current),
        "day"        : current.day,
        "month"      : current.month,
        "month_name" : current.strftime("%B"),
        "quarter"    : (current.month - 1) // 3 + 1,
        "year"       : current.year,
        "is_weekend" : 1 if current.weekday() >= 5 else 0
    })
    current += timedelta(days=1)

dim_date_df = pd.DataFrame(dates)
dim_date_df.to_sql("dim_date", con=engine, if_exists="replace", index=False)
print(f"  dim_date populated: {len(dim_date_df)} rows")