"""SEC EDGAR Submissions Fetcher

Fetches raw submissions data for specified semiconductor companies from SEC EDGAR API.
Complies with SEC rate limits and User-Agent requirements.
"""

import json
import os
import sys
import time
from typing import Any, Dict, Optional
import requests

# CIK Mapping for Target Semiconductor Companies
CIK_MAP: Dict[str, str] = {
    "NVDA": "0001045810",
    "AMD": "0000002488",
    "INTC": "0000050863",
    "QCOM": "0000804328",
    "MU": "0000723125",
}

DEFAULT_USER_AGENT = "SemiconductorAnalytics Ryoma1022@gmail.com"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEC_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "sec")


def fetch_sec_submissions(
    symbol: str = "NVDA",
    save_dir: str = SEC_RAW_DIR,
    user_agent: str = DEFAULT_USER_AGENT,
    max_retries: int = 3,
    timeout: int = 30,
) -> Dict[str, Any]:
    """Fetch raw SEC EDGAR submissions JSON for a given ticker and save to disk.

    Args:
        symbol: Stock ticker symbol (default: NVDA)
        save_dir: Directory path to save raw JSON
        user_agent: SEC compliant User-Agent string
        max_retries: Maximum number of retries upon transient errors
        timeout: Request timeout in seconds

    Returns:
        dict: Parsed raw submissions JSON data
    """
    symbol = symbol.upper()
    if symbol not in CIK_MAP:
        raise ValueError(f"Ticker '{symbol}' not found in CIK_MAP: {list(CIK_MAP.keys())}")

    cik = CIK_MAP[symbol].zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate",
        "Accept": "application/json, text/plain, */*",
    }

    os.makedirs(save_dir, exist_ok=True)
    out_file = os.path.join(save_dir, f"{symbol}_submissions.json")

    print(f"[*] Fetching SEC submissions for {symbol} (CIK: {cik}) from {url}...")

    last_error: Optional[Exception] = None
    data: Optional[Dict[str, Any]] = None

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                print(f"[+] HTTP 200 OK (Attempt {attempt}/{max_retries})")
                break
            elif resp.status_code == 429:
                wait_seconds = 2 * attempt
                print(f"[!] Rate limit encountered (HTTP 429). Retrying in {wait_seconds}s...")
                time.sleep(wait_seconds)
            else:
                print(f"[!] SEC EDGAR returned HTTP status {resp.status_code}: {resp.text[:200]}")
                resp.raise_for_status()
        except requests.RequestException as e:
            last_error = e
            print(f"[!] Request failed on attempt {attempt}/{max_retries}: {e}")
            if attempt < max_retries:
                time.sleep(1.5 * attempt)

    if data is None:
        raise RuntimeError(f"Failed to fetch submissions for {symbol} after {max_retries} attempts: {last_error}")

    # Save exact raw JSON (no modifications or pruning)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[+] Raw JSON successfully saved to: {out_file}")

    # Validation & Acceptance Checks
    validate_submissions_file(out_file, symbol, cik)
    return data


def validate_submissions_file(file_path: str, expected_symbol: str, expected_cik: str) -> None:
    """Validate that the saved submissions JSON meets all acceptance criteria."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Verification failed: File not found at {file_path}")

    if os.path.getsize(file_path) == 0:
        raise ValueError(f"Verification failed: File {file_path} is empty")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    actual_cik = str(data.get("cik", "")).lstrip("0")
    expected_cik_clean = expected_cik.lstrip("0")
    if actual_cik != expected_cik_clean:
        raise ValueError(f"CIK mismatch! Expected {expected_cik_clean}, got {actual_cik}")

    company_name = data.get("name", "")
    if not company_name:
        raise ValueError("Missing company 'name' field in submissions JSON")

    if "filings" not in data or "recent" not in data["filings"]:
        raise ValueError("Missing 'filings.recent' in submissions JSON")

    recent = data["filings"]["recent"]
    required_keys = ["form", "filingDate", "accessionNumber", "primaryDocument"]
    for key in required_keys:
        if key not in recent:
            raise ValueError(f"Missing required field '{key}' in filings.recent")

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    k_count = sum(1 for f in forms if f == "10-K")
    q_count = sum(1 for f in forms if f == "10-Q")

    print("[+] Validation Passed:")
    print(f"    - Symbol / Target: {expected_symbol}")
    print(f"    - Company Name: {company_name}")
    print(f"    - CIK: {actual_cik}")
    print(f"    - Total Filings: {len(forms)}")
    print(f"    - 10-K Filings: {k_count}, 10-Q Filings: {q_count}")
    print("    - Latest 3 filings:")
    for i in range(min(3, len(forms))):
        print(f"        * Form {forms[i]} on {dates[i]}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    fetch_sec_submissions(target)
