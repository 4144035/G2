# MEMORY.md

## 目前進度

### 做了什麼

- 已建立 GitHub repository。
- 已完成 Antigravity 與 GitHub repository 連線。
- 已安裝 Python 環境。
- 已完成專案需求拷問與可行性討論。
- 已完成 `PLAN.md`。
- 已建立第一張任務 `TASK 01`。
- 已確定分析標的為 NVDA、AMD、INTC、QCOM、MU。
- 已確定使用 SEC EDGAR 財報申報資料與 Yahoo Finance 日線股價。
- 已確定分析財報事件後第 1、3、5 個交易日的波動。
- 已確定以中位數為主要參考、平均數為輔助，並保留正負報酬及漲跌比例。

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

目前無。

### AI 錯了什麼

目前無。

### 下一步

執行 `TASK 01`：使用 SEC EDGAR submissions API 抓取 NVDA 原始資料，保存為 `data/raw/sec/NVDA_submissions.json`，完成驗收後更新本檔案並 commit、push。

