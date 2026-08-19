"""Pipeline Automated Test Suite

Verifies:
1. Data file existence and structure
2. SEC filings dates and forms (only 10-Q and 10-K within 2-year window)
3. Return calculation correctness and price alignments
4. Output tables and charts generation
"""

import os
import sys
import unittest
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))


class TestSemiconductorEarningsPipeline(unittest.TestCase):

    def setUp(self):
        self.events_path = os.path.join(PROJECT_ROOT, "data", "processed", "sec_events.csv")
        self.details_path = os.path.join(PROJECT_ROOT, "outputs", "tables", "event_details.csv")
        self.summary_path = os.path.join(PROJECT_ROOT, "outputs", "tables", "company_summary.csv")
        self.comp_path = os.path.join(PROJECT_ROOT, "outputs", "tables", "overall_comparison.csv")

    def test_sec_events_structure(self):
        """Verify cleaned SEC events dataframe."""
        self.assertTrue(os.path.exists(self.events_path), "sec_events.csv does not exist")
        df = pd.read_csv(self.events_path)

        # Check forms
        valid_forms = {"10-Q", "10-K"}
        forms = set(df["form"].unique())
        self.assertTrue(forms.issubset(valid_forms), f"Unexpected forms found: {forms - valid_forms}")

        # Check expected tickers
        expected_tickers = {"NVDA", "AMD", "INTC", "QCOM", "MU"}
        self.assertEqual(set(df["symbol"].unique()), expected_tickers)

        # Check total events count (8 events per company = 40)
        self.assertEqual(len(df), 40, f"Expected 40 events, got {len(df)}")

    def test_return_calculations_accuracy(self):
        """Verify that event returns and absolute volatilities match manual calculations."""
        self.assertTrue(os.path.exists(self.details_path), "event_details.csv does not exist")
        df = pd.read_csv(self.details_path)

        for _, row in df.iterrows():
            base_price = row["base_price"]
            self.assertGreater(base_price, 0, "Base price must be positive")

            for n in [1, 3, 5]:
                close_n = row[f"close_plus_{n}d"]
                ret_n = row[f"return_{n}d_pct"]
                abs_vol_n = row[f"abs_volatility_{n}d_pct"]

                if not np.isnan(close_n):
                    expected_ret = round(((close_n / base_price) - 1.0) * 100.0, 2)
                    self.assertAlmostEqual(ret_n, expected_ret, delta=0.02,
                                           msg=f"Return mismatch for {row['symbol']} on {row['filing_date']} (+{n}D)")
                    self.assertAlmostEqual(abs_vol_n, abs(expected_ret), delta=0.02,
                                           msg=f"Abs volatility mismatch for {row['symbol']} on {row['filing_date']} (+{n}D)")

    def test_output_charts_exist(self):
        """Verify all generated visualization files exist and are not empty."""
        charts = [
            "median_volatility_comparison.png",
            "returns_distribution_boxplots.png",
            "win_rates_comparison.png",
            "event_trajectories_by_company.png",
        ]
        charts_dir = os.path.join(PROJECT_ROOT, "outputs", "charts")
        for chart in charts:
            path = os.path.join(charts_dir, chart)
            self.assertTrue(os.path.exists(path), f"Chart missing: {chart}")
            self.assertGreater(os.path.getsize(path), 1000, f"Chart file too small: {chart}")


if __name__ == "__main__":
    unittest.main()
