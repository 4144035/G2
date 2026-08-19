# TASK.md

## TASK 01｜抓取並保存 NVDA 的 SEC EDGAR 原始 submissions 資料（已完成）

### 目標

使用 Python 從 SEC EDGAR submissions API 成功取得 NVIDIA（NVDA）的公司申報資料，並將伺服器回傳的原始 JSON 完整保存至專案。

### 驗收結果

- [x] 程式執行完成，HTTP 回應狀態為 200。
- [x] 已建立 `data/raw/sec/NVDA_submissions.json`。
- [x] 檔案不是空檔，且可被 Python 正常解析為 JSON。
- [x] JSON 中的公司名稱為 NVIDIA CORP。
- [x] JSON 中的 CIK 對應 NVIDIA（1045810）。
- [x] JSON 含有 `filings` 與 `filings.recent`。
- [x] `filings.recent` 中可找到 `form`、`filingDate`、`accessionNumber`、`primaryDocument` 等欄位。
- [x] 原始 JSON 未做刪欄、篩選或改寫。
- [x] request 使用包含專案名稱與真實聯絡信箱的 `User-Agent`。
- [x] 錯誤處理至少涵蓋連線失敗、逾時與非 200 回應。
- [x] 已更新 `MEMORY.md`，並完成 commit。

---

## TASK 02｜抓取全標的 SEC 原始資料並清洗近兩年 10-Q、10-K 事件（已完成）

### 目標

1. 擴展抓取 NVDA、AMD、INTC、QCOM、MU 共 5 檔半導體標的的 SEC EDGAR submissions 原始 JSON。
2. 撰寫 `src/clean_sec.py`，篩選近兩年滾動期間之 `10-Q` 與 `10-K` 財報事件，產出 `data/processed/sec_events.csv`。

### 驗收結果

- [x] 5 檔股票之原始 submissions JSON 皆已下載至 `data/raw/sec/` 且驗證完整。
- [x] 執行 `src/clean_sec.py` 成功產出 `data/processed/sec_events.csv`。
- [x] 事件表僅包含 `10-Q` 與 `10-K`，無其他 Form。
- [x] 事件申報日期均在執行日往回推兩年之區間內（共 40 筆事件，每檔各 8 筆）。
- [x] 5 檔股票每檔均有 8 個有效財報事件（6 次 10-Q + 2 次 10-K）。
- [x] 資料表依 `filing_date` 與 `symbol` 正確排序，無重複或遺漏記錄。

---

## TASK 03｜抓取 Yahoo Finance 股價資料（已完成）

### 目標

使用 `yfinance` 抓取 5 檔標的歷史日線股價（涵蓋事件日前後交易日序列），保存至 `data/raw/prices/{symbol}_daily.csv`。

### 驗收結果

- [x] 建立 `src/fetch_prices.py`。
- [x] 5 檔股票日線資料皆成功抓取（每檔各 626 交易日，2024-02 至 2026-08）。
- [x] 涵蓋基準日（T-1）與事件後第 5 個交易日。
- [x] 欄位格式標準化（Date, Open, High, Low, Close, Volume）。

---

## TASK 04｜計算事件後 1, 3, 5 日波動與統計分析（已完成）

### 目標

建立 `src/analyze_events.py`，計算各事件後第 1、3、5 個交易日報酬率與絕對波動，並計算中位數、平均數、勝率與跨公司比較表。

### 驗收結果

- [x] 事件日遇非交易日正確對應至其後第一個交易日。
- [x] 基準價採事件前一交易日收盤價。
- [x] 第 1、3、5 日依交易日序列計算。
- [x] 產出 `outputs/tables/event_details.csv`。
- [x] 產出 `outputs/tables/company_summary.csv`。
- [x] 產出 `outputs/tables/overall_comparison.csv`。

---

## TASK 05｜視覺化圖表與結論報告（已完成）

### 目標

建立 `src/generate_visualizations.py` 產出圖表，撰寫結論報告與一鍵執行腳本 `main.py`。

### 驗收結果

- [x] 產出 `outputs/charts/median_volatility_comparison.png`。
- [x] 產出 `outputs/charts/returns_distribution_boxplots.png`。
- [x] 產出 `outputs/charts/win_rates_comparison.png`。
- [x] 產出 `outputs/charts/event_trajectories_by_company.png`。
- [x] 產出 `outputs/report/semiconductor_earnings_volatility_report.md`。
- [x] 建立 `main.py` 與 `README.md`。
