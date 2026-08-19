# TASK.md

## TASK 01｜抓取並保存 NVDA 的 SEC EDGAR 原始 submissions 資料（已完成）

### 目標

使用 Python 從 SEC EDGAR submissions API 成功取得 NVIDIA（NVDA）的公司申報資料，並將伺服器回傳的原始 JSON 完整保存至專案。此任務只負責抓取與保存原始資料，暫不清洗、篩選 10-Q／10-K，也不進行股價分析。

### 材料

- Python 3
- Python 套件：`requests`
- NVDA／NVIDIA CIK：`0001045810`
- SEC submissions API：
```text
https://data.sec.gov/submissions/CIK0001045810.json
```
- 輸出位置：
```text
data/raw/sec/NVDA_submissions.json
```
- SEC 要求的 HTTP request header：
```text
User-Agent: SemiconductorAnalytics Ryoma1022@gmail.com
Accept-Encoding: gzip, deflate
Host: data.sec.gov
```

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
- [x] 已更新 `MEMORY.md`，並完成本關卡的 commit 與 push。

---

## TASK 02｜抓取全標的 SEC 原始資料並清洗近兩年 10-Q、10-K 事件

### 目標

1. 擴展抓取 NVDA、AMD、INTC、QCOM、MU 共 5 檔半導體標的的 SEC EDGAR submissions 原始 JSON，分別保存至 `data/raw/sec/{TICKER}_submissions.json`。
2. 撰寫 `src/clean_sec.py`，從原始 JSON 中提取各股票的申報紀錄，篩選出最近兩年（滾動兩年，即 `2024-08-19` 至 `2026-08-19`）的 `10-Q` 與 `10-K` 財報事件。
3. 輸出清洗後之標準化事件表 `data/processed/sec_events.csv`。

### 材料與輸出

- 輸入：`data/raw/sec/{symbol}_submissions.json`
- 標的清單：
  - `NVDA`: CIK 0001045810
  - `AMD`: CIK 0000002488
  - `INTC`: CIK 0000050863
  - `QCOM`: CIK 0000804328
  - `MU`: CIK 0000723125
- 輸出位置：`data/processed/sec_events.csv`
- 輸出欄位：
  - `symbol` (股票代碼)
  - `cik` (CIK 代碼)
  - `company_name` (公司名稱)
  - `form` (10-Q 或 10-K)
  - `filing_date` (申報日期 YYYY-MM-DD)
  - `report_date` (財報期間結束日 YYYY-MM-DD)
  - `accession_number` (申報案號)
  - `primary_doc_name` (主文檔檔名)

### 驗收條件

- [ ] 5 檔股票之原始 submissions JSON 皆已下載至 `data/raw/sec/` 且驗證完整。
- [ ] 執行 `src/clean_sec.py` 成功產出 `data/processed/sec_events.csv`。
- [ ] 事件表僅包含 `10-Q` 與 `10-K`，無其他 Form（如 8-K, 4, 13F 等）。
- [ ] 事件申報日期均在執行日往回推兩年之區間內。
- [ ] 5 檔股票每檔均有 7~9 個有效財報事件（一年 3 次 10-Q + 1 次 10-K）。
- [ ] 資料表依 `filing_date` 與 `symbol` 正確排序，無重複或遺漏記錄。
- [ ] 更新 `MEMORY.md` 並完成 commit / push。
