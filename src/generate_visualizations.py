"""Earnings Event Volatility Visualization Generator

Generates high-resolution publication-quality charts for semiconductor
earnings event price reactions across +1D, +3D, +5D horizons.
Saves PNG charts to outputs/charts/.
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_TABLES_DIR = os.path.join(PROJECT_ROOT, "outputs", "tables")
OUTPUT_CHARTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "charts")

# Set matplotlib parameters for clean presentation
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300


def plot_median_volatility(summary_df: pd.DataFrame, out_dir: str):
    """Plot Median Absolute Volatility (%) across companies and horizons."""
    pivoted = summary_df.pivot(index="symbol", columns="horizon", values="median_abs_volatility_pct")
    pivoted = pivoted[["+1D", "+3D", "+5D"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(pivoted.index))
    width = 0.25

    rects1 = ax.bar(x - width, pivoted["+1D"], width, label="+1D Post Event", color="#2b5c8f", alpha=0.9)
    rects2 = ax.bar(x, pivoted["+3D"], width, label="+3D Post Event", color="#e27c38", alpha=0.9)
    rects3 = ax.bar(x + width, pivoted["+5D"], width, label="+5D Post Event", color="#3b9a60", alpha=0.9)

    ax.set_ylabel("Median Absolute Volatility (%)", fontsize=12, fontweight="bold")
    ax.set_title("Median Absolute Price Volatility by Horizon (2-Year Rolling SEC Filings)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(pivoted.index, fontsize=11, fontweight="bold")
    ax.legend(frameon=True, facecolor="white", edgecolor="none")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # Add value labels
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            if not np.isnan(height):
                ax.annotate(f"{height:.1f}%",
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha="center", va="bottom", fontsize=8, fontweight="bold")

    plt.tight_layout()
    out_path = os.path.join(out_dir, "median_volatility_comparison.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved: {out_path}")


def plot_returns_distribution(details_df: pd.DataFrame, out_dir: str):
    """Plot boxplots of returns across 1D, 3D, 5D for each stock."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 6), sharey=True)
    horizons = [(1, "+1D Returns"), (3, "+3D Returns"), (5, "+5D Returns")]
    symbols = sorted(details_df["symbol"].unique())

    colors = ["#2b5c8f", "#e27c38", "#3b9a60", "#c23838", "#7b5294"]

    for i, (n, title) in enumerate(horizons):
        ax = axes[i]
        ret_col = f"return_{n}d_pct"
        data_by_sym = [details_df[details_df["symbol"] == s][ret_col].dropna().values for s in symbols]

        bp = ax.boxplot(data_by_sym, tick_labels=symbols, patch_artist=True,
                        boxprops=dict(facecolor="#d9e2ec", color="#102a43"),
                        medianprops=dict(color="#d64545", linewidth=2),
                        whiskerprops=dict(color="#102a43"),
                        capprops=dict(color="#102a43"))

        for box, col in zip(bp["boxes"], colors):
            box.set_facecolor(col)
            box.set_alpha(0.65)

        ax.axhline(0, color="gray", linestyle="--", alpha=0.7)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_ylabel("Return (%)" if i == 0 else "", fontsize=11)
        ax.grid(axis="y", linestyle=":", alpha=0.5)

    fig.suptitle("Post-Earnings Stock Return Distributions (+1D, +3D, +5D)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    out_path = os.path.join(out_dir, "returns_distribution_boxplots.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved: {out_path}")


def plot_win_rate_and_direction(summary_df: pd.DataFrame, out_dir: str):
    """Plot Positive Return Frequency (Win Rate %) by Company and Horizon."""
    pivoted = summary_df.pivot(index="symbol", columns="horizon", values="win_rate_pct")
    pivoted = pivoted[["+1D", "+3D", "+5D"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(pivoted.index))
    width = 0.25

    ax.bar(x - width, pivoted["+1D"], width, label="+1D Win Rate", color="#1f77b4", alpha=0.85)
    ax.bar(x, pivoted["+3D"], width, label="+3D Win Rate", color="#ff7f0e", alpha=0.85)
    ax.bar(x + width, pivoted["+5D"], width, label="+5D Win Rate", color="#2ca02c", alpha=0.85)

    ax.axhline(50, color="red", linestyle=":", linewidth=1.5, label="50% Benchmark (Even Chance)")
    ax.set_ylabel("Positive Return Probability / Win Rate (%)", fontsize=12, fontweight="bold")
    ax.set_title("Post-Earnings Positive Return Ratio (%) by Horizon", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(pivoted.index, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 100)
    ax.legend(frameon=True, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    out_path = os.path.join(out_dir, "win_rates_comparison.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved: {out_path}")


def plot_all_event_trajectories(details_df: pd.DataFrame, out_dir: str):
    """Plot return evolution trajectory for each event across 1D -> 3D -> 5D."""
    symbols = sorted(details_df["symbol"].unique())
    fig, axes = plt.subplots(len(symbols), 1, figsize=(11, 14), sharex=True, sharey=True)

    days = [1, 3, 5]

    for idx, sym in enumerate(symbols):
        ax = axes[idx]
        sym_events = details_df[details_df["symbol"] == sym]

        for _, ev in sym_events.iterrows():
            rets = [ev["return_1d_pct"], ev["return_3d_pct"], ev["return_5d_pct"]]
            date_label = ev["filing_date"]
            form = ev["form"]
            c = "green" if rets[0] > 0 else "crimson"
            ax.plot([1, 3, 5], rets, marker="o", linewidth=1.5, alpha=0.75, label=f"{date_label} ({form})", color=c)

        ax.axhline(0, color="black", linestyle="--", alpha=0.5, linewidth=1)
        ax.set_ylabel(f"{sym}\nReturn (%)", fontsize=10, fontweight="bold")
        ax.set_xticks([1, 3, 5])
        ax.set_xticklabels(["+1D", "+3D", "+5D"], fontsize=10)
        ax.grid(True, linestyle=":", alpha=0.5)

    axes[-1].set_xlabel("Trading Days Post Filing Event", fontsize=11, fontweight="bold")
    fig.suptitle("Individual Event Price Return Trajectories by Company", fontsize=14, fontweight="bold", y=0.99)
    plt.tight_layout()
    out_path = os.path.join(out_dir, "event_trajectories_by_company.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved: {out_path}")


def generate_all_charts(out_dir: str = OUTPUT_CHARTS_DIR):
    """Generate all visualization assets."""
    os.makedirs(out_dir, exist_ok=True)

    summary_path = os.path.join(OUTPUT_TABLES_DIR, "company_summary.csv")
    details_path = os.path.join(OUTPUT_TABLES_DIR, "event_details.csv")

    summary_df = pd.read_csv(summary_path)
    details_df = pd.read_csv(details_path)

    plot_median_volatility(summary_df, out_dir)
    plot_returns_distribution(details_df, out_dir)
    plot_win_rate_and_direction(summary_df, out_dir)
    plot_all_event_trajectories(details_df, out_dir)
    print("[+] All visualizations generated successfully.")


if __name__ == "__main__":
    generate_all_charts()
