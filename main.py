"""Semiconductor Earnings Volatility Analysis System - Main Pipeline Runner

Runs the complete end-to-end analytics workflow:
1. Fetch raw SEC EDGAR submissions (NVDA, AMD, INTC, QCOM, MU)
2. Clean and filter 2-year rolling 10-Q and 10-K events
3. Fetch daily historical prices from Yahoo Finance
4. Calculate +1D, +3D, +5D returns and volatility statistics
5. Generate high-resolution presentation charts
"""

import os
import sys
import time

# Ensure src/ is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from clean_sec import clean_and_export_sec_events
from fetch_prices import fetch_historical_prices
from analyze_events import run_full_analysis
from generate_visualizations import generate_all_charts
from generate_dashboard import export_dashboard


def run_pipeline():
    print("=" * 70)
    print("   SEMICONDUCTOR EARNINGS EVENT VOLATILITY ANALYSIS PIPELINE")
    print("=" * 70)
    start_time = time.time()

    print("\n>>> STEP 1 & 2: Fetching & Cleaning SEC Submissions (Rolling 2 Years)...")
    clean_and_export_sec_events()

    print("\n>>> STEP 3: Fetching Daily Stock Prices from Yahoo Finance...")
    fetch_historical_prices()

    print("\n>>> STEP 4: Computing Event Volatility & Aggregate Statistics (+1D, +3D, +5D)...")
    run_full_analysis()

    print("\n>>> STEP 5: Generating Visualization Charts...")
    generate_all_charts()

    print("\n>>> STEP 6: Generating Interactive HTML Dashboard...")
    export_dashboard()

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f" [+] Pipeline execution finished successfully in {elapsed:.2f} seconds!")
    print(" Outputs generated:")
    print("   - Raw SEC Data:       data/raw/sec/")
    print("   - Cleaned Events:     data/processed/sec_events.csv")
    print("   - Raw Prices:         data/raw/prices/")
    print("   - Statistical Tables: outputs/tables/")
    print("   - Visual Charts:      outputs/charts/")
    print("   - HTML Dashboard:     dashboard.html & outputs/dashboard.html")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
