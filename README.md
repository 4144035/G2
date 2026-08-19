# 美股半導體財報事件波動分析系統 (Semiconductor Earnings Volatility Analyzer)

本專案為一套自動化資料分析工具，針對 5 檔美國半導體指標股（**NVDA**、**AMD**、**INTC**、**QCOM**、**MU**），自動串接 **SEC EDGAR API** 申報資料與 **Yahoo Finance** 日線股價，計算並統計財報事件後 **+1、+3、+5 個交易日** 的價格反應與波動度。

---

## 📌 功能特色

1. **合規自動化抓取**：符合 SEC EDGAR API 存取規範（合規 `User-Agent`、速率限制、重試機制）。
2. **滾動兩年分析**：自動依當前執行時間往回推兩年，精確篩選期間內的 `10-Q` 與 `10-K` 事件。
3. **交易日精準對齊**：
   - 申報日遇週末或休市日，自動對齊至後續第一個有效交易日。
   - 基準價採事件日前一交易日收盤價。
   - 計算 +1D、+3D、+5D 交易日序列，絕不使用日曆日直接加減。
   - 未來交易日不足之最新事件保持 `NaN` 空值，不誤填為 0。
4. **完整統計與視覺化**：
   - 計算絕對波動中位數、平均數、漲跌比例（勝率）、最大漲跌幅。
   - 自動產出逐事件明細表、彙總表、跨公司比較表與高畫質圖表。

---

## 📁 專案目錄結構

```text
├── main.py                    # 一鍵執行端到端完整分析流程
├── requirements.txt           # Python 相依套件清單
├── PLAN.md                    # 專案架構與規範說明書
├── TASK.md                    # 任務關卡定義與驗收記錄
├── MEMORY.md                  # 進度追蹤與重要規格備忘錄
├── README.md                  # 專案說明文件
├── src/                       # 核心程式模組
│   ├── fetch_sec.py           # 抓取 SEC EDGAR submissions JSON
│   ├── clean_sec.py           # 清洗與篩選 2 年 10-Q/10-K 事件
│   ├── fetch_prices.py        # 抓取 Yahoo Finance 日線股價
│   ├── analyze_events.py      # 計算 +1D, +3D, +5D 波動與統計指標
│   └── generate_visualizations.py # 繪製分析圖表
├── data/
│   ├── raw/
│   │   ├── sec/               # SEC 原始 JSON 申報檔案
│   │   └── prices/            # 各股票歷史日線 CSV 檔案
│   └── processed/
│       └── sec_events.csv     # 清洗後之財報事件清單
└── outputs/
    ├── tables/                # 統計輸出表格 (CSV)
    │   ├── event_details.csv
    │   ├── company_summary.csv
    │   └── overall_comparison.csv
    ├── charts/                # 高解析度視覺化圖表 (PNG)
    │   ├── median_volatility_comparison.png
    │   ├── returns_distribution_boxplots.png
    │   ├── win_rates_comparison.png
    │   └── event_trajectories_by_company.png
    └── report/                # 完整分析結論報告 (Markdown)
        └── semiconductor_earnings_volatility_report.md
```

---

## 🚀 快速開始與執行方式

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 2. 一鍵執行完整分析流程

```bash
python main.py
```

或使用 Python 3.12：

```bash
py -3.12 main.py
```

### 3. 單獨執行個別模組

- **抓取 SEC 申報資料**：
  ```bash
  py -3.12 src/fetch_sec.py NVDA
  ```
- **清洗 SEC 事件資料**：
  ```bash
  py -3.12 src/clean_sec.py
  ```
- **抓取歷史股價**：
  ```bash
  py -3.12 src/fetch_prices.py
  ```
- **執行事件分析**：
  ```bash
  py -3.12 src/analyze_events.py
  ```
- **產出圖表**：
  ```bash
  py -3.12 src/generate_visualizations.py
  ```

---

## 📊 主要分析產出物一覽

1. **[逐事件明細表](file:///C:/Users/USER/Desktop/1/outputs/tables/event_details.csv)**：列出 40 場財報事件之基準價、+1D/+3D/+5D 價格、報酬率與絕對波動。
2. **[公司彙總統計表](file:///C:/Users/USER/Desktop/1/outputs/tables/company_summary.csv)**：各公司在各週期的中位數、平均數與勝率。
3. **[跨公司比較表](file:///C:/Users/USER/Desktop/1/outputs/tables/overall_comparison.csv)**：橫向比較五檔標的之波動特徵。
4. **[分析結論報告](file:///C:/Users/USER/Desktop/1/outputs/report/semiconductor_earnings_volatility_report.md)**：包含核心結論、觀察摘要與限制說明。
