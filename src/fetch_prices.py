"""Yahoo Finance Historical Price Fetcher

Fetches daily OHLCV price history for target semiconductor companies.
Saves raw price data to data/raw/prices/{ticker}_daily.csv.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd
import yfinance as yf

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICES_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "prices")
DEFAULT_TICKERS = ["NVDA", "AMD", "INTC", "QCOM", "MU"]


def fetch_historical_prices(
    tickers: Optional[List[str]] = None,
    lookback_years: float = 2.5,
    save_dir: str = PRICES_RAW_DIR
) -> dict:
    """Fetch daily stock price history from Yahoo Finance and save to CSV.

    Args:
        tickers: List of stock symbols (default: NVDA, AMD, INTC, QCOM, MU)
        lookback_years: Years of history to fetch (covers pre-event baseline & post-event +5 days)
        save_dir: Output directory for price CSV files

    Returns:
        dict: Mapping of ticker -> DataFrame of daily prices
    """
    if tickers is None:
        tickers = DEFAULT_TICKERS

    os.makedirs(save_dir, exist_ok=True)
    today = datetime.now()
    start_date = (today - timedelta(days=int(lookback_years * 365.25))).strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"[*] Fetching Yahoo Finance daily prices from {start_date} to {end_date} for: {', '.join(tickers)}")

    prices_dict = {}

    for symbol in tickers:
        out_file = os.path.join(save_dir, f"{symbol}_daily.csv")
        print(f"[*] Downloading {symbol}...")

        ticker_obj = yf.Ticker(symbol)
        df = ticker_obj.history(start=start_date, end=end_date, auto_adjust=True)

        if df.empty:
            raise RuntimeError(f"No price data returned for {symbol} from Yahoo Finance.")

        # Reset index and clean date formatting
        df = df.reset_index()
        # Handle timezone in Date column
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None).dt.strftime("%Y-%m-%d")

        # Standardize column names
        required_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column '{col}' for {symbol}")

        df = df[required_cols].copy()
        df = df.sort_values(by="Date", ascending=True).reset_index(drop=True)

        # Save to CSV
        df.to_csv(out_file, index=False, encoding="utf-8")
        prices_dict[symbol] = df

        first_date = df["Date"].iloc[0]
        last_date = df["Date"].iloc[-1]
        print(f"[+] Saved {symbol} prices ({len(df)} trading days, {first_date} ~ {last_date}) -> {out_file}")

    return prices_dict


if __name__ == "__main__":
    fetch_historical_prices()
