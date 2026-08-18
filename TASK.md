# TASK.md

## TASK 01｜抓取並保存 NVDA 的 SEC EDGAR 原始 submissions 資料

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
User-Agent: 專案名稱 聯絡信箱
Accept-Encoding: gzip, deflate
Host: data.sec.gov
```

執行前需將「聯絡信箱」換成組員可用的真實聯絡信箱。

### 執行步驟

1. 在專案根目錄建立 `data/raw/sec/` 資料夾。
2. 建立第一支 SEC 抓取程式，例如 `src/fetch_sec.py`。
3. 以 `requests.get()` 呼叫 NVDA submissions API，設定合規的 request headers 與合理 timeout。
4. 檢查 HTTP 狀態碼；成功時解析 JSON，失敗時輸出清楚的錯誤訊息。
5. 將回傳內容以 UTF-8 JSON 完整保存為 `data/raw/sec/NVDA_submissions.json`。
6. 重新開啟存檔，確認它是有效 JSON，並檢查關鍵欄位。
7. 將執行結果、錯誤與解法記錄到 `MEMORY.md`。

### 驗收

以下條件全部符合才算完成 TASK 01：

- [ ] 程式執行完成，HTTP 回應狀態為 200。
- [ ] 已建立 `data/raw/sec/NVDA_submissions.json`。
- [ ] 檔案不是空檔，且可被 Python 正常解析為 JSON。
- [ ] JSON 中的公司名稱為 NVIDIA 相關名稱。
- [ ] JSON 中的 CIK 對應 NVIDIA（1045810）。
- [ ] JSON 含有 `filings` 與 `filings.recent`。
- [ ] `filings.recent` 中可找到 `form`、`filingDate`、`accessionNumber`、`primaryDocument` 等欄位。
- [ ] 原始 JSON 未做刪欄、篩選或改寫。
- [ ] request 使用包含專案名稱與真實聯絡信箱的 `User-Agent`。
- [ ] 錯誤處理至少涵蓋連線失敗、逾時與非 200 回應。
- [ ] 已更新 `MEMORY.md`，並完成本關卡的 commit 與 push。

### 本任務不做

- 不抓取其他 4 檔股票。
- 不篩選 10-Q 或 10-K。
- 不限制近兩年資料。
- 不抓 Yahoo Finance 股價。
- 不計算報酬率或製作圖表。

### 完成後下一步

建立 TASK 02：清洗 NVDA submissions，篩選近兩年的 10-Q、10-K 財報事件並另存分析用資料。

