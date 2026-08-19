# MEMORY.md

## 目前進度

### 做了什麼

- 已建立 GitHub repository (`https://github.com/Ryoma1022/G2`)。
- 已完成 Antigravity 與 GitHub repository 連線。
- 已安裝 Python 環境與相依套件 (`requests`, `pandas`, `yfinance`, `matplotlib`)。
- 已完成專案需求拷問與可行性討論。
- 已完成 `PLAN.md` 規格規劃。
- **已完成 `TASK 01`**：
  - 建立 `src/fetch_sec.py`，支援 SEC EDGAR API 抓取與驗證。
  - 使用合規 User-Agent：`SemiconductorAnalytics Ryoma1022@gmail.com`。
  - 成功抓取 NVDA 原始申報資料並保存為 `data/raw/sec/NVDA_submissions.json`。
  - 通過所有驗收檢查（HTTP 200、CIK 1045810、NVIDIA CORP、完整保留原始 JSON、驗證 filings 結構）。

### 已確定的重要規格

- SEC 事件只保留 10-Q、10-K。
- 事件日期使用 SEC `filingDate`。
- 分析區間為程式執行日往回推兩年。
- 若 filing date 為非交易日，計算時對應其後最近的有效交易日。
- 股價分析使用交易日序列，不使用日曆日直接加 1、3、5 天。
- SEC 與股價原始資料先完整保存，再另行清洗。
- 最新事件若後續交易日不足，缺值保留為空值，不視為 0。
- 專案僅提供歷史波動參考，不預測方向、不提供投資建議。

### 卡在哪

- SEC API 對 `User-Agent` 的 Email 格式有嚴格限制（帶 `+` 或 `noreply` 會被擋 403），已調整為標準 Email 格式解決。

### AI 錯了什麼

- 初次使用 `318083982+Ryoma1022@users.noreply.github.com` 作為 User-Agent 時被 SEC 403 阻擋，隨後排查出格式限制並修復為標準格式。

### 下一步

執行 `TASK 02`：
1. 批次抓取其餘 4 檔標的（AMD, INTC, QCOM, MU）之 SEC 原始 submissions 資料至 `data/raw/sec/`。
2. 建立清洗腳本 `src/clean_sec.py`，篩選近兩年（2024-08 至 2026-08）之 10-Q、10-K 財報事件，輸出 `data/processed/sec_events.csv`。
