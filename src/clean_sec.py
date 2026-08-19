"""SEC EDGAR Event Cleaner

Extracts and filters 10-Q and 10-K filings for target semiconductor stocks
within a rolling 2-year window from execution date.
Outputs clean structured dataset to data/processed/sec_events.csv.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_sec import CIK_MAP, fetch_sec_submissions, PROJECT_ROOT, SEC_RAW_DIR

PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")


def get_all_target_submissions(tickers: List[str] = None) -> Dict[str, Dict[str, Any]]:
    """Ensure all target tickers' submissions JSON files are available and loaded."""
    if tickers is None:
        tickers = list(CIK_MAP.keys())

    all_data = {}
    for symbol in tickers:
        file_path = os.path.join(SEC_RAW_DIR, f"{symbol}_submissions.json")
        if not os.path.exists(file_path):
            print(f"[*] Raw JSON missing for {symbol}. Fetching now...")
            data = fetch_sec_submissions(symbol)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        all_data[symbol] = data
    return all_data


def extract_filings_dataframe(all_data: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Flatten filings.recent from each company JSON into a combined DataFrame."""
    records = []

    for symbol, data in all_data.items():
        cik = str(data.get("cik", "")).zfill(10)
        company_name = data.get("name", symbol)
        recent = data.get("filings", {}).get("recent", {})

        forms = recent.get("form", [])
        filing_dates = recent.get("filingDate", [])
        report_dates = recent.get("reportDate", [])
        accession_numbers = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])

        n = len(forms)
        for i in range(n):
            records.append({
                "symbol": symbol,
                "cik": cik,
                "company_name": company_name,
                "form": forms[i],
                "filing_date": filing_dates[i] if i < len(filing_dates) else None,
                "report_date": report_dates[i] if i < len(report_dates) else None,
                "accession_number": accession_numbers[i] if i < len(accession_numbers) else None,
                "primary_doc_name": primary_docs[i] if i < len(primary_docs) else None,
            })

    return pd.DataFrame(records)


def filter_earnings_events(
    df: pd.DataFrame,
    rolling_years: int = 2,
    as_of_date: Optional[datetime] = None
) -> pd.DataFrame:
    """Filter for 10-Q and 10-K events within the rolling years window.

    Args:
        df: Combined raw filings DataFrame
        rolling_years: Number of years to look back (default: 2)
        as_of_date: Reference end date (defaults to current date)

    Returns:
        pd.DataFrame: Cleaned and filtered earnings events DataFrame
    """
    if as_of_date is None:
        as_of_date = datetime.now()

    start_date = as_of_date - timedelta(days=rolling_years * 365.25)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = as_of_date.strftime("%Y-%m-%d")

    print(f"[*] Filtering earnings events (10-Q, 10-K) between {start_date_str} and {end_date_str}...")

    # Filter by form type (only 10-Q and 10-K)
    filtered = df[df["form"].isin(["10-Q", "10-K"])].copy()

    # Convert filing_date to string comparison / datetime
    filtered["filing_date"] = pd.to_datetime(filtered["filing_date"])
    filtered = filtered[(filtered["filing_date"] >= start_date_str) & (filtered["filing_date"] <= end_date_str)]

    # Format dates as YYYY-MM-DD
    filtered["filing_date"] = filtered["filing_date"].dt.strftime("%Y-%m-%d")

    # Sort by symbol and filing_date ascending
    filtered = filtered.sort_values(by=["symbol", "filing_date"], ascending=[True, True]).reset_index(drop=True)
    return filtered


def clean_and_export_sec_events(
    tickers: List[str] = None,
    rolling_years: int = 2,
    out_dir: str = PROCESSED_DATA_DIR
) -> pd.DataFrame:
    """Full pipeline: load raw SEC data, filter 2-year 10-Q/10-K events, and save CSV."""
    if tickers is None:
        tickers = list(CIK_MAP.keys())

    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, "sec_events.csv")

    all_data = get_all_target_submissions(tickers)
    raw_df = extract_filings_dataframe(all_data)
    events_df = filter_earnings_events(raw_df, rolling_years=rolling_years)

    events_df.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"[+] Cleaned SEC earnings events successfully exported to: {out_csv}")
    print(f"[+] Total events found: {len(events_df)}")
    print("\n--- Events Summary per Company ---")
    summary = events_df.groupby(["symbol", "form"]).size().unstack(fill_value=0)
    print(summary)
    print("\n--- Event List ---")
    print(events_df[["symbol", "company_name", "form", "filing_date", "report_date"]].to_string(index=False))

    return events_df


if __name__ == "__main__":
    clean_and_export_sec_events()
