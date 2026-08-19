"""Earnings Event Volatility Analyzer

Calculates +1, +3, and +5 trading day price changes and volatility around
SEC 10-Q and 10-K filing events for target semiconductor stocks.
Outputs granular event details and statistical summaries to outputs/tables/.
"""

import os
import sys
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
PRICES_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "prices")
OUTPUT_TABLES_DIR = os.path.join(PROJECT_ROOT, "outputs", "tables")


def load_events(events_path: Optional[str] = None) -> pd.DataFrame:
    """Load cleaned SEC events CSV."""
    if events_path is None:
        events_path = os.path.join(PROCESSED_DATA_DIR, "sec_events.csv")
    if not os.path.exists(events_path):
        raise FileNotFoundError(f"SEC events file not found: {events_path}")
    return pd.read_csv(events_path)


def load_prices(tickers: List[str]) -> Dict[str, pd.DataFrame]:
    """Load daily historical price CSV for each ticker."""
    prices_map = {}
    for ticker in tickers:
        p_path = os.path.join(PRICES_RAW_DIR, f"{ticker}_daily.csv")
        if not os.path.exists(p_path):
            raise FileNotFoundError(f"Price CSV for {ticker} not found: {p_path}")
        df = pd.read_csv(p_path)
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        df = df.sort_values(by="Date", ascending=True).reset_index(drop=True)
        prices_map[ticker] = df
    return prices_map


def calculate_event_volatility(events_df: pd.DataFrame, prices_map: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calculate returns and absolute volatilities for +1, +3, +5 trading days.

    Specification:
    - If filing_date is not a trading day, use the first subsequent trading day.
    - Base price: Close price of the trading day immediately prior to the effective event day.
    - Day +1: Close price of event trading day (Day +0 post announcement / index + 0).
    - Day +3: Close price of event + 2 trading days.
    - Day +5: Close price of event + 4 trading days.
    - If future trading days are not yet available, values remain NaN (never filled with 0).
    """
    records = []

    for _, row in events_df.iterrows():
        symbol = row["symbol"]
        filing_date = str(row["filing_date"])
        form = row["form"]
        report_date = row.get("report_date", "")

        price_df = prices_map[symbol]
        dates = price_df["Date"].tolist()
        closes = price_df["Close"].tolist()

        # Find effective event trading day (on or first after filing_date)
        effective_idx = None
        for idx, d in enumerate(dates):
            if d >= filing_date:
                effective_idx = idx
                break

        if effective_idx is None:
            print(f"[!] Warning: No price data on or after {filing_date} for {symbol}")
            continue

        effective_event_date = dates[effective_idx]

        # Base trading day (T - 1)
        base_idx = effective_idx - 1
        if base_idx < 0:
            print(f"[!] Warning: Insufficient historical price data before {effective_event_date} for {symbol}")
            continue

        base_date = dates[base_idx]
        base_price = closes[base_idx]

        # Day +1, +3, +5 indices relative to base
        # Day +1: effective_idx (+0 trading day relative to event day)
        # Day +3: effective_idx + 2
        # Day +5: effective_idx + 4
        offsets = {1: 0, 3: 2, 5: 4}
        event_res = {
            "symbol": symbol,
            "company_name": row.get("company_name", symbol),
            "form": form,
            "filing_date": filing_date,
            "effective_event_date": effective_event_date,
            "report_date": report_date,
            "base_date": base_date,
            "base_price": round(base_price, 4),
        }

        for n_days, offset in offsets.items():
            target_idx = effective_idx + offset
            if target_idx < len(dates):
                target_date = dates[target_idx]
                target_price = closes[target_idx]
                ret_pct = ((target_price / base_price) - 1.0) * 100.0
                abs_ret_pct = abs(ret_pct)

                event_res[f"date_plus_{n_days}d"] = target_date
                event_res[f"close_plus_{n_days}d"] = round(target_price, 4)
                event_res[f"return_{n_days}d_pct"] = round(ret_pct, 2)
                event_res[f"abs_volatility_{n_days}d_pct"] = round(abs_ret_pct, 2)
            else:
                event_res[f"date_plus_{n_days}d"] = np.nan
                event_res[f"close_plus_{n_days}d"] = np.nan
                event_res[f"return_{n_days}d_pct"] = np.nan
                event_res[f"abs_volatility_{n_days}d_pct"] = np.nan

        records.append(event_res)

    result_df = pd.DataFrame(records)
    return result_df


def generate_company_summaries(details_df: pd.DataFrame) -> pd.DataFrame:
    """Generate aggregate statistics per company across +1, +3, +5 day horizons."""
    summary_rows = []

    for symbol, group in details_df.groupby("symbol"):
        total_events = len(group)

        for n in [1, 3, 5]:
            ret_col = f"return_{n}d_pct"
            abs_col = f"abs_volatility_{n}d_pct"

            valid_returns = group[ret_col].dropna()
            valid_abs = group[abs_col].dropna()
            valid_count = len(valid_returns)

            if valid_count > 0:
                med_ret = valid_returns.median()
                mean_ret = valid_returns.mean()
                med_abs_vol = valid_abs.median()
                mean_abs_vol = valid_abs.mean()
                up_count = (valid_returns > 0).sum()
                down_count = (valid_returns < 0).sum()
                flat_count = (valid_returns == 0).sum()
                win_rate = (up_count / valid_count) * 100.0
                max_gain = valid_returns.max()
                max_loss = valid_returns.min()
            else:
                med_ret = mean_ret = med_abs_vol = mean_abs_vol = win_rate = max_gain = max_loss = np.nan
                up_count = down_count = flat_count = 0

            summary_rows.append({
                "symbol": symbol,
                "horizon": f"+{n}D",
                "events_count": valid_count,
                "median_abs_volatility_pct": round(med_abs_vol, 2),
                "mean_abs_volatility_pct": round(mean_abs_vol, 2),
                "median_return_pct": round(med_ret, 2),
                "mean_return_pct": round(mean_ret, 2),
                "up_count": int(up_count),
                "down_count": int(down_count),
                "win_rate_pct": round(win_rate, 1),
                "max_gain_pct": round(max_gain, 2),
                "max_loss_pct": round(max_loss, 2),
            })

    return pd.DataFrame(summary_rows)


def generate_cross_company_comparison(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Pivot summary metrics into an executive comparison table across tickers."""
    pivoted = summary_df.pivot(index="symbol", columns="horizon", values=["median_abs_volatility_pct", "mean_return_pct", "win_rate_pct"])
    pivoted.columns = [f"{col[1]}_{col[0]}" for col in pivoted.columns]
    pivoted = pivoted.reset_index()
    return pivoted


def run_full_analysis(out_dir: str = OUTPUT_TABLES_DIR) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Execute complete analysis pipeline and export CSV tables."""
    os.makedirs(out_dir, exist_ok=True)

    events_df = load_events()
    tickers = events_df["symbol"].unique().tolist()
    prices_map = load_prices(tickers)

    # 1. Detailed Event Table
    details_df = calculate_event_volatility(events_df, prices_map)
    details_csv = os.path.join(out_dir, "event_details.csv")
    details_df.to_csv(details_csv, index=False, encoding="utf-8")
    print(f"[+] Saved event details table ({len(details_df)} rows) -> {details_csv}")

    # 2. Company Summary Table
    summary_df = generate_company_summaries(details_df)
    summary_csv = os.path.join(out_dir, "company_summary.csv")
    summary_df.to_csv(summary_csv, index=False, encoding="utf-8")
    print(f"[+] Saved company summary table -> {summary_csv}")

    # 3. Cross Company Comparison Table
    comp_df = generate_cross_company_comparison(summary_df)
    comp_csv = os.path.join(out_dir, "overall_comparison.csv")
    comp_df.to_csv(comp_csv, index=False, encoding="utf-8")
    print(f"[+] Saved cross-company comparison table -> {comp_csv}")

    print("\n==================== COMPANY SUMMARY STATISTICS ====================")
    print(summary_df.to_string(index=False))

    return details_df, summary_df, comp_df


if __name__ == "__main__":
    run_full_analysis()
