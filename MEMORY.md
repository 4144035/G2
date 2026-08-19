# MEMORY.md

## 目前進度

### 做了什麼

- 已完成 GitHub repository 與 Antigravity 環境配置。
- 已完成 `PLAN.md` 規格與完整架構設計。
- **已完成 `TASK 01`**：抓取並保存 NVDA 原始 SEC EDGAR 申報 JSON 檔。
- **已完成 `TASK 02`**：批次抓取 NVDA, AMD, INTC, QCOM, MU 之 SEC submissions，並以 `src/clean_sec.py` 清洗出近兩年滾動期間共 40 筆 10-Q/10-K 財報事件，匯出至 `data/processed/sec_events.csv`。
- **已完成 `TASK 03`**：以 `src/fetch_prices.py` 透過 Yahoo Finance 抓取 5 檔標的之歷史日線股價（各 626 交易日），保存至 `data/raw/prices/`。
- **已完成 `TASK 04`**：以 `src/analyze_events.py` 精確對齊交易日序列，計算基準價與事件後 +1D、+3D、+5D 之報酬率、絕對波動、中位數、平均數、勝率等指標，產出明細與統計表至 `outputs/tables/`。
- **已完成 `TASK 05`**：以 `src/generate_visualizations.py` 產出 4 份高畫質分析圖表至 `outputs/charts/`，撰寫完整分析報告 `outputs/report/semiconductor_earnings_volatility_report.md`，建立 `main.py` 與 `README.md`。

### 已確定的重要規格與邏輯

- SEC 事件只保留 10-Q、10-K。
- 事件日期使用 SEC `filingDate`，遇非交易日自動對齊至後續第一個有效交易日。
- 基準價為有效事件日前一個交易日的收盤價（Close of T-1）。
- 股價分析一律依交易日序列計算（+1D 為當日 Close、+3D 為 index+2、+5D 為 index+4）。
- 原始資料（SEC JSON、價格 CSV）與清洗加工資料分離保存。
- 支援一鍵式全流程自動執行 (`py -3.12 main.py`)。

### 卡在哪

- 無。所有功能模組皆已實作、驗證與產出成果。

### 下一步

- 執行 Git 提交與同步至 GitHub Repository (`origin/main`)。
