"""
live_nav_fetch.py
DAY 1 — Fetch Live NAV Data from mfapi.in
Capstone Project I – Mutual Fund Analytics
Author: Sanapathi Kalyani
"""

import os
import requests
import pandas as pd
from datetime import datetime

# Folder to save fetched CSVs
RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

BASE_URL = "https://api.mfapi.in/mf"

# All 6 schemes required by the task
SCHEMES = {
    "HDFC_Top_100_Direct": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}


def fetch_nav(scheme_name, scheme_code):
    url = f"{BASE_URL}/{scheme_code}"
    print(f"\n  Fetching: {scheme_name} (code={scheme_code})")
    print(f"  URL: {url}")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        meta = data.get("meta", {})
        nav_data = data.get("data", [])

        print(f"  Fund     : {meta.get('scheme_name', 'N/A')}")
        print(f"  Records  : {len(nav_data)}")

        if nav_data:
            print(f"  Latest   : Rs.{nav_data[0]['nav']} on {nav_data[0]['date']}")
        else:
            print("  WARNING: No NAV data returned!")
            return None

        df = pd.DataFrame(nav_data)
        df.rename(columns={"date": "nav_date", "nav": "nav_value"}, inplace=True)
        df["nav_date"] = pd.to_datetime(df["nav_date"], format="%d-%m-%Y")
        df["nav_value"] = pd.to_numeric(df["nav_value"], errors="coerce")
        df["scheme_code"] = scheme_code
        df["scheme_name"] = meta.get("scheme_name", scheme_name)
        df["fund_house"] = meta.get("fund_house", "")
        df["scheme_type"] = meta.get("scheme_type", "")
        df["scheme_category"] = meta.get("scheme_category", "")
        df = df.sort_values("nav_date").reset_index(drop=True)
        return df

    except requests.exceptions.ConnectionError:
        print(f"  ERROR: No internet / mfapi.in is unreachable.")
        return None
    except requests.exceptions.Timeout:
        print(f"  ERROR: Request timed out.")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main():
    print("=" * 60)
    print("  LIVE NAV FETCHER — mfapi.in")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total schemes to fetch: {len(SCHEMES)}")
    print("=" * 60)

    all_dfs = []
    fetch_log = []

    for scheme_name, scheme_code in SCHEMES.items():
        df = fetch_nav(scheme_name, scheme_code)

        if df is not None:
            filename = f"nav_{scheme_name.lower()}.csv"
            out_path = os.path.join(RAW_DATA_DIR, filename)
            df.to_csv(out_path, index=False)
            print(f"  SAVED: {out_path}")
            all_dfs.append(df)
            fetch_log.append({
                "Scheme": scheme_name,
                "Code": scheme_code,
                "Status": "SUCCESS",
                "Records": len(df)
            })
        else:
            fetch_log.append({
                "Scheme": scheme_name,
                "Code": scheme_code,
                "Status": "FAILED",
                "Records": 0
            })

    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined_path = os.path.join(RAW_DATA_DIR, "all_nav_combined.csv")
        combined.to_csv(combined_path, index=False)
        print(f"\n  Combined file saved: {combined_path}")
        print(f"  Total rows: {len(combined)}")

    print("\n" + "=" * 60)
    print("  FETCH SUMMARY")
    print("=" * 60)
    print(pd.DataFrame(fetch_log).to_string(index=False))

    success = sum(1 for r in fetch_log if r["Status"] == "SUCCESS")
    print(f"\n  Fetched: {success}/{len(SCHEMES)} schemes successfully")
    print("\n  live_nav_fetch.py completed!")


if __name__ == "__main__":
    main()