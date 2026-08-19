"""Interactive HTML Dashboard Generator for Classroom Presentation

Generates a standalone, feature-rich, interactive HTML presentation dashboard:
1. Problem Motivation & Flowchart
2. Development Process & AI Collaboration (Real Development Experience)
3. KPI Metric Cards (Revised terminology)
4. Interactive Dynamic Charts (Chart.js)
5. Summary Metrics Matrix & Event Explorer (Historical Positive Return Ratio)
6. Research Limitations & Future Extensions
Saves to outputs/dashboard.html and dashboard.html in project root.
"""

import json
import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_TABLES_DIR = os.path.join(PROJECT_ROOT, "outputs", "tables")
OUTPUT_HTML_PATH = os.path.join(PROJECT_ROOT, "outputs", "dashboard.html")
ROOT_HTML_PATH = os.path.join(PROJECT_ROOT, "dashboard.html")


def build_dashboard_html() -> str:
    # Load processed data
    events_path = os.path.join(OUTPUT_TABLES_DIR, "event_details.csv")
    summary_path = os.path.join(OUTPUT_TABLES_DIR, "company_summary.csv")

    if not os.path.exists(events_path) or not os.path.exists(summary_path):
        raise FileNotFoundError("Required output tables not found. Please run analyze_events.py first.")

    events_df = pd.read_csv(events_path)
    summary_df = pd.read_csv(summary_path)

    # Convert data to JSON for embedding
    events_json = events_df.to_json(orient="records")
    summary_json = summary_df.to_json(orient="records")

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>美股半導體財報事件波動分析 ｜ 課堂報告儀表板</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    body {{
      font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #0b1120;
      color: #f1f5f9;
    }}
    .glass-card {{
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 1rem;
    }}
    .glass-card-hover:hover {{
      border-color: rgba(56, 189, 248, 0.35);
      transform: translateY(-2px);
      transition: all 0.2s ease-in-out;
    }}
    .badge-pos {{
      background-color: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .badge-neg {{
      background-color: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    .badge-neutral {{
      background-color: rgba(148, 163, 184, 0.15);
      color: #cbd5e1;
      border: 1px solid rgba(148, 163, 184, 0.3);
    }}
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0b1120;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 4px;
    }}
    @media print {{
      body {{
        background-color: #ffffff !important;
        color: #000000 !important;
      }}
      .glass-card {{
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #000000 !important;
      }}
    }}
  </style>
</head>
<body class="min-h-screen p-4 md:p-8">
  <div class="max-w-7xl mx-auto space-y-8">
    
    <!-- HEADER -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
      <div>
        <div class="flex flex-wrap items-center gap-2 md:gap-3">
          <span class="px-3 py-1 text-xs font-bold tracking-wider text-cyan-400 uppercase bg-cyan-950/70 border border-cyan-800 rounded-full">
            課堂專題報告 (5–8 min)
          </span>
          <span class="px-3 py-1 text-xs font-semibold text-slate-300 bg-slate-800 rounded-full border border-slate-700">
            SEC EDGAR + Yahoo Finance
          </span>
          <span class="text-xs text-slate-400">近兩年滾動分析 (2024~2026)</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight text-white mt-2">
          美股半導體財報事件波動分析儀表板
        </h1>
        <p class="text-slate-400 text-sm md:text-base mt-1">
          量化分析 <strong class="text-cyan-400">NVDA</strong>、<strong class="text-cyan-400">AMD</strong>、<strong class="text-cyan-400">INTC</strong>、<strong class="text-cyan-400">QCOM</strong>、<strong class="text-cyan-400">MU</strong> 在 10-Q / 10-K 申報後第 1、3、5 交易日之歷史波動與報酬分佈
        </p>
      </div>
      <div class="flex items-center gap-3">
        <button onclick="window.print()" class="px-4 py-2 text-xs md:text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 transition">
          🖨️ 列印 / 匯出 PDF
        </button>
        <a href="tables/event_details.csv" download class="px-4 py-2 text-xs md:text-sm font-medium bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition shadow-lg shadow-cyan-900/30">
          📥 下載 CSV 數據
        </a>
      </div>
    </header>

    <!-- SECTION 1: 專案想法與問題意識 -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2 h-6 bg-cyan-500 rounded-full"></div>
        <h2 class="text-xl md:text-2xl font-bold text-white tracking-tight">一、專案想法與問題意識</h2>
      </div>

      <!-- Core Question Banner -->
      <div class="bg-gradient-to-r from-cyan-950/60 via-slate-900/80 to-slate-900/40 p-5 rounded-xl border border-cyan-800/50 space-y-2">
        <div class="text-xs font-bold uppercase tracking-wider text-cyan-400">核心探討問題 (Core Research Question)</div>
        <div class="text-lg md:text-xl font-semibold text-white leading-relaxed">
          「半導體公司發布財報後，未來 <span class="text-amber-400 underline decoration-amber-400/50 underline-offset-4">1、3、5 個交易日</span> 通常會移動多大？方向是否存在歷史特徵？」
        </div>
        <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
          半導體產業兼具高資本支出與高景氣循環特性，每逢財報公布常伴隨劇烈的市場重定價。本專案透過自動化數據管道，量化近兩年各標的在財報申報後的絕對價格反應與歷史正負報酬分佈，建立可量化追溯的歷史波動基準。
        </p>
      </div>

      <!-- Process Flowchart -->
      <div>
        <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">資料分析與處理流程 (Pipeline Flowchart)</div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          
          <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 flex flex-col justify-between">
            <div>
              <div class="text-xs text-cyan-400 font-bold mb-1">步驟 1 ｜ 申報資料</div>
              <div class="text-sm font-semibold text-white">SEC EDGAR 10-Q/10-K</div>
              <div class="text-xs text-slate-400 mt-1">抓取 5 家公司原始 submissions JSON，篩選近兩年 10-Q/10-K</div>
            </div>
            <div class="text-right text-slate-500 font-bold mt-2 text-xs">01 ➔</div>
          </div>

          <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 flex flex-col justify-between">
            <div>
              <div class="text-xs text-cyan-400 font-bold mb-1">步驟 2 ｜ 股價資料</div>
              <div class="text-sm font-semibold text-white">Yahoo Finance 股價</div>
              <div class="text-xs text-slate-400 mt-1">抓取 626 交易日之日線 Close 序列，涵蓋基準日與 +5D 區間</div>
            </div>
            <div class="text-right text-slate-500 font-bold mt-2 text-xs">02 ➔</div>
          </div>

          <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 flex flex-col justify-between">
            <div>
              <div class="text-xs text-cyan-400 font-bold mb-1">步驟 3 ｜ 日期對齊</div>
              <div class="text-sm font-semibold text-white">交易日對齊與基準價</div>
              <div class="text-xs text-slate-400 mt-1">遇非交易日向後對齊有效交易日；基準價採事件前一交易日收盤價 (T-1)</div>
            </div>
            <div class="text-right text-slate-500 font-bold mt-2 text-xs">03 ➔</div>
          </div>

          <div class="bg-slate-800/80 p-4 rounded-lg border border-slate-700 flex flex-col justify-between">
            <div>
              <div class="text-xs text-cyan-400 font-bold mb-1">步驟 4 ｜ 波動計算</div>
              <div class="text-sm font-semibold text-white">+1D / +3D / +5D 報酬與波動</div>
              <div class="text-xs text-slate-400 mt-1">依交易日序列計算報酬率與絕對值，缺值嚴格保留為空值不填 0</div>
            </div>
            <div class="text-right text-slate-500 font-bold mt-2 text-xs">04 ➔</div>
          </div>

          <div class="bg-slate-800/80 p-4 rounded-lg border border-cyan-800/80 bg-cyan-950/30 flex flex-col justify-between">
            <div>
              <div class="text-xs text-cyan-400 font-bold mb-1">步驟 5 ｜ 橫向比較</div>
              <div class="text-sm font-semibold text-white">五家公司統計矩陣</div>
              <div class="text-xs text-slate-400 mt-1">彙總中位數、平均數、歷史正報酬比例與視覺化圖表</div>
            </div>
            <div class="text-right text-cyan-400 font-bold mt-2 text-xs">✓ 完成</div>
          </div>

        </div>
      </div>
    </section>

    <!-- SECTION 2: 開發流程與 AI 協作經驗 -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2 h-6 bg-purple-500 rounded-full"></div>
        <h2 class="text-xl md:text-2xl font-bold text-white tracking-tight">二、開發流程與 AI 協作經驗</h2>
      </div>

      <!-- 4 Collaboration Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div class="bg-slate-800/60 p-5 rounded-xl border border-slate-700 space-y-2">
          <div class="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-sm">1</div>
          <h3 class="text-base font-bold text-white">規劃與需求拷問</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            確立 5 檔標的、鎖定 10-Q/10-K、限定近兩年滾動區間與 T-1 基準價對齊規則；建立 <code>PLAN.md</code> 與 <code>TASK.md</code> 關卡規範。
          </p>
        </div>

        <div class="bg-slate-800/60 p-5 rounded-xl border border-slate-700 space-y-2">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-sm">2</div>
          <h3 class="text-base font-bold text-white">資料抓取 (Ingestion)</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            克服 SEC EDGAR 的 User-Agent 格式限制（排查 403 阻擋），成功下載 5 檔標的 40 筆原始 JSON 與 626 交易日股價。
          </p>
        </div>

        <div class="bg-slate-800/60 p-5 rounded-xl border border-slate-700 space-y-2">
          <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm">3</div>
          <h3 class="text-base font-bold text-white">資料整理與計算</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            以純交易日序列推算 +1D、+3D、+5D 價格；計算中位數、平均數與正負報酬次數，產出逐事件明細與彙總表。
          </p>
        </div>

        <div class="bg-slate-800/60 p-5 rounded-xl border border-purple-800/80 bg-purple-950/20 space-y-2">
          <div class="w-8 h-8 rounded-lg bg-purple-500/30 text-purple-300 flex items-center justify-center font-bold text-sm">4</div>
          <h3 class="text-base font-bold text-white">AI 協作與嚴謹驗收</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            不直接信任 AI 的完成宣告；實作自動化單元測試 (<code>unittest</code>) 與公式反算，雙重核對資料一致性與邊界條件。
          </p>
        </div>

      </div>

      <!-- Real Development Reflection Box -->
      <div class="bg-slate-900/90 p-5 rounded-xl border border-slate-700/80 space-y-2">
        <div class="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider">
          <span>💡</span> 真實開發經驗與反思 (Real Development Insight)
        </div>
        <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
          原先專案規劃採「逐 TASK 分階段實作與人工審查」；但在實作時，AI 助理一度一次性建立了完整的端到端 pipeline。為確保資料品質與計算嚴謹性，團隊<strong>並未直接採信 AI 的完成宣告</strong>，而是切換至驗證模式：
          <br />
          1. <strong>實際終端機執行</strong>：真實運行 <code>py -3.12 main.py</code> 確認各模組依序跑通；
          <br />
          2. <strong>撰寫自動化測試</strong>：透過 <code>tests/test_pipeline.py</code> 抽樣反算 40 場財報事件之報酬率公式；
          <br />
          3. <strong>跨表一致性檢查</strong>：確認圖表、彙總表與逐事件原始明細數值 100% 吻合，落實「以驗證代替盲信」的 AI 協作原則。
        </p>
      </div>
    </section>

    <!-- SECTION 3: 核心數據指標 (KPI CARDS) -->
    <section>
      <div class="flex items-center gap-3 mb-4">
        <div class="w-2 h-6 bg-emerald-500 rounded-full"></div>
        <h2 class="text-xl md:text-2xl font-bold text-white tracking-tight">三、核心指標與重要發現</h2>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">總分析財報事件</div>
          <div class="text-3xl font-extrabold text-white mt-2">40 <span class="text-sm font-normal text-slate-400">場</span></div>
          <div class="text-xs text-slate-400 mt-1">5 檔標的 × 各 8 次 (6 次 10-Q + 2 次 10-K)</div>
        </div>

        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">+1D 絕對波動最高</div>
          <div class="text-3xl font-extrabold text-amber-400 mt-2">INTC <span class="text-lg">7.26%</span></div>
          <div class="text-xs text-slate-400 mt-1">中位數絕對波動 (+5D 達 9.75%)</div>
        </div>

        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">+1D 歷史正報酬比例最高</div>
          <div class="text-3xl font-extrabold text-emerald-400 mt-2">QCOM <span class="text-lg">75.0%</span></div>
          <div class="text-xs text-slate-400 mt-1">8 次事件中 6 次 +1D 為正報酬</div>
        </div>

        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">NVDA +3D 歷史現象</div>
          <div class="text-3xl font-extrabold text-rose-400 mt-2">0.0% <span class="text-sm font-normal text-slate-400">正報酬</span></div>
          <div class="text-xs text-slate-400 mt-1">近兩年 8 次事件在 +3D 皆為負報酬 (樣本有限)</div>
        </div>
      </div>
    </section>

    <!-- SECTION 4: 互動圖表區塊 (INTERACTIVE CHARTS) -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- Chart 1: Median Volatility -->
      <div class="glass-card p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-lg font-bold text-white">各公司絕對波動度比較 (中位數)</h2>
            <p class="text-xs text-slate-400">衡量財報公布後市場的絕對重定價幅度</p>
          </div>
          <span class="text-xs px-2 py-1 bg-slate-800 rounded text-slate-300">單位: %</span>
        </div>
        <div class="h-72">
          <canvas id="chartVolatility"></canvas>
        </div>
      </div>

      <!-- Chart 2: Positive Return Ratio (Win Rate) -->
      <div class="glass-card p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-lg font-bold text-white">財報後歷史上漲比例對比 (Positive Return Ratio)</h2>
            <p class="text-xs text-slate-400">歷史正報酬次數佔比 (紅虛線為 50% 多空分界，非未來機率)</p>
          </div>
          <span class="text-xs px-2 py-1 bg-slate-800 rounded text-slate-300">基準: 50%</span>
        </div>
        <div class="h-72">
          <canvas id="chartWinRate"></canvas>
        </div>
      </div>

      <!-- Chart 3: Mean Return -->
      <div class="glass-card p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-lg font-bold text-white">各天期平均報酬率 (+1D / +3D / +5D)</h2>
            <p class="text-xs text-slate-400">反映整體方向性歷史平均值</p>
          </div>
          <span class="text-xs px-2 py-1 bg-slate-800 rounded text-slate-300">單位: %</span>
        </div>
        <div class="h-72">
          <canvas id="chartMeanReturn"></canvas>
        </div>
      </div>

      <!-- Chart 4: Interactive Trajectory Simulator -->
      <div class="glass-card p-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h2 class="text-lg font-bold text-white">個別財報事件走勢軌跡 (+1D → +5D)</h2>
            <p class="text-xs text-slate-400">點選標的切換單一公司的各場事件走勢曲線</p>
          </div>
          <select id="trajectorySymbolSelect" class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded px-3 py-1.5 focus:outline-none focus:border-cyan-500">
            <option value="ALL">全部標的彙總</option>
            <option value="NVDA">NVDA (NVIDIA)</option>
            <option value="AMD">AMD</option>
            <option value="INTC">INTC (Intel)</option>
            <option value="QCOM">QCOM (Qualcomm)</option>
            <option value="MU">MU (Micron)</option>
          </select>
        </div>
        <div class="h-72">
          <canvas id="chartTrajectory"></canvas>
        </div>
      </div>

    </section>

    <!-- SECTION 5: 彙總統計矩陣表 (SUMMARY TABLE) -->
    <section class="glass-card p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-lg font-bold text-white">五大半導體指標股彙總統計矩陣</h2>
          <p class="text-xs text-slate-400">近兩年歷史 10-Q / 10-K 申報後反應總覽</p>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-300">
          <thead class="text-xs uppercase bg-slate-800/80 text-slate-400 border-b border-slate-700">
            <tr>
              <th class="px-4 py-3 font-semibold">股票代碼</th>
              <th class="px-4 py-3 font-semibold">天期</th>
              <th class="px-4 py-3 font-semibold text-right">絕對波動 (中位數)</th>
              <th class="px-4 py-3 font-semibold text-right">平均報酬率</th>
              <th class="px-4 py-3 font-semibold text-right">中位數報酬率</th>
              <th class="px-4 py-3 font-semibold text-center">漲 / 跌次數</th>
              <th class="px-4 py-3 font-semibold text-right">歷史上漲比例</th>
              <th class="px-4 py-3 font-semibold text-right">歷史最大漲幅</th>
              <th class="px-4 py-3 font-semibold text-right">歷史最大跌幅</th>
            </tr>
          </thead>
          <tbody id="summaryTableBody" class="divide-y divide-slate-800">
            <!-- Rendered by JavaScript -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 6: 逐事件明細搜尋器 (EVENT EXPLORER) -->
    <section class="glass-card p-6">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h2 class="text-xl font-bold text-white">財報事件詳細明細搜尋器 (Event Explorer)</h2>
          <p class="text-xs text-slate-400 mt-0.5">點擊表頭可排序，支援公司、申報類別與日期搜尋</p>
        </div>
        <div class="flex flex-wrap items-center gap-3">
          <!-- Filter Symbol -->
          <select id="filterSymbol" class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500">
            <option value="">所有股票 (All Symbols)</option>
            <option value="NVDA">NVDA</option>
            <option value="AMD">AMD</option>
            <option value="INTC">INTC</option>
            <option value="QCOM">QCOM</option>
            <option value="MU">MU</option>
          </select>
          <!-- Filter Form -->
          <select id="filterForm" class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500">
            <option value="">所有表格 (All Forms)</option>
            <option value="10-Q">10-Q (季報)</option>
            <option value="10-K">10-K (年報)</option>
          </select>
          <!-- Search Input -->
          <input type="text" id="filterSearch" placeholder="搜尋日期或關鍵字..." class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 w-44 focus:outline-none focus:border-cyan-500" />
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-300">
          <thead class="text-xs uppercase bg-slate-800/80 text-slate-400 border-b border-slate-700">
            <tr>
              <th class="px-4 py-3 font-semibold">標的</th>
              <th class="px-4 py-3 font-semibold">Form</th>
              <th class="px-4 py-3 font-semibold">SEC 申報日</th>
              <th class="px-4 py-3 font-semibold">有效交易日</th>
              <th class="px-4 py-3 font-semibold text-right">基準價 (T-1)</th>
              <th class="px-4 py-3 font-semibold text-right">+1D 報酬</th>
              <th class="px-4 py-3 font-semibold text-right">+3D 報酬</th>
              <th class="px-4 py-3 font-semibold text-right">+5D 報酬</th>
              <th class="px-4 py-3 font-semibold text-right">+5D 絕對波動</th>
            </tr>
          </thead>
          <tbody id="eventsTableBody" class="divide-y divide-slate-800 font-mono text-xs">
            <!-- Rendered by JavaScript -->
          </tbody>
        </table>
      </div>
      <div id="noEventsMessage" class="hidden text-center py-8 text-slate-500 text-sm">
        查無符合條件的財報事件。
      </div>
    </section>

    <!-- SECTION 7: 限制與未來擴充 -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2 h-6 bg-rose-500 rounded-full"></div>
        <h2 class="text-xl md:text-2xl font-bold text-white tracking-tight">四、研究限制與未來擴充</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Left: Limitations -->
        <div class="bg-rose-950/20 p-5 rounded-xl border border-rose-900/40 space-y-3">
          <div class="flex items-center gap-2 text-sm font-bold text-rose-300 uppercase tracking-wider">
            <span>⚠️</span> 目前研究限制 (Research Limitations)
          </div>
          <ul class="list-disc list-inside space-y-2 text-xs md:text-sm text-slate-300 leading-relaxed">
            <li>
              <strong>申報日期非公布時間戳</strong>：SEC <code>filingDate</code> 為官方收件日期，部分公司於盤後發布新聞稿而於隔日申報，存在微小時間差。
            </li>
            <li>
              <strong>未區分盤前 / 盤後公告</strong>：第一版模型未細分盤前、盤中或盤後發布，均統一對齊當日或次一交易日。
            </li>
            <li>
              <strong>樣本數有限</strong>：每家公司近兩年約僅有 8 次申報事件（合計 40 筆），統計結果屬於探索性歷史觀察，不具長期統計顯著性定論。
            </li>
            <li>
              <strong>資料來源限制</strong>：Yahoo Finance 價格資料為公開調整後價格，並非官方交易所逐筆直連數據源。
            </li>
            <li>
              <strong>歷史比例 ≠ 未來機率</strong>：歷史上漲比例僅反映過去兩年統計現象，嚴禁直接推論為未來交易勝率或投資建議。
            </li>
          </ul>
        </div>

        <!-- Right: Future Extensions -->
        <div class="bg-cyan-950/20 p-5 rounded-xl border border-cyan-900/40 space-y-3">
          <div class="flex items-center gap-2 text-sm font-bold text-cyan-300 uppercase tracking-wider">
            <span>🚀</span> 未來擴充方向 (Future Extensions)
          </div>
          <ul class="list-disc list-inside space-y-2 text-xs md:text-sm text-slate-300 leading-relaxed">
            <li>
              <strong>引入精準公告時間戳 (Timestamp)</strong>：串接財經新聞或專業數據源，精準定位到「分/秒」之發布時刻。
            </li>
            <li>
              <strong>區分盤前 / 盤後並動態調整基準日</strong>：盤後公告以當日收盤為 T-1 基準，盤前公告以前一交易日收盤為基準。
            </li>
            <li>
              <strong>延長回測期間至 5~10 年</strong>：擴大歷史樣本量至數十場事件，提升樣本統計穩健度。
            </li>
            <li>
              <strong>納入 EPS / Revenue Surprise 分析</strong>：結合市場預期差值（Consensus Estimate），分析超越預期幅度與波動的相關性。
            </li>
            <li>
              <strong>擴充產業鏈指標股</strong>：納入晶圓代工龍頭 (TSM)、設備龍頭 (ASML)、網通晶片 (AVGO) 等更多半導體權值標的。
            </li>
          </ul>
        </div>

      </div>
    </section>

    <!-- FOOTER -->
    <footer class="pt-6 pb-8 border-t border-slate-800 text-center text-xs text-slate-500 space-y-1">
      <div>美股半導體財報事件波動分析專題 ｜ 課堂簡報儀表板</div>
      <div>本專案僅供學術與量化研究參考，不構成任何投資建議。</div>
    </footer>

  </div>

  <!-- SCRIPT LOGIC -->
  <script>
    const eventsData = {events_json};
    const summaryData = {summary_json};

    // Color definitions
    const colors = {{
      NVDA: '#10b981',
      AMD: '#f59e0b',
      INTC: '#3b82f6',
      QCOM: '#8b5cf6',
      MU: '#ec4899',
    }};

    // Helper: format badge
    function formatBadge(val) {{
      if (val === null || isNaN(val)) return '<span class="px-2 py-0.5 rounded badge-neutral">N/A</span>';
      const num = Number(val);
      const sign = num > 0 ? '+' : '';
      const cls = num > 0 ? 'badge-pos' : (num < 0 ? 'badge-neg' : 'badge-neutral');
      return `<span class="px-2 py-0.5 rounded font-semibold ${{cls}}">${{sign}}${{num.toFixed(2)}}%</span>`;
    }}

    // Render Summary Table
    function renderSummaryTable() {{
      const tbody = document.getElementById('summaryTableBody');
      tbody.innerHTML = '';
      summaryData.forEach(row => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        const color = colors[row.symbol] || '#ffffff';
        tr.innerHTML = `
          <td class="px-4 py-3 font-bold" style="color: ${{color}}">${{row.symbol}}</td>
          <td class="px-4 py-3"><span class="px-2 py-0.5 bg-slate-800 rounded text-slate-300 text-xs font-mono">${{row.horizon}}</span></td>
          <td class="px-4 py-3 text-right font-semibold text-white">${{row.median_abs_volatility_pct.toFixed(2)}}%</td>
          <td class="px-4 py-3 text-right font-mono">${{formatBadge(row.mean_return_pct)}}</td>
          <td class="px-4 py-3 text-right font-mono">${{formatBadge(row.median_return_pct)}}</td>
          <td class="px-4 py-3 text-center text-xs font-mono"><span class="text-emerald-400 font-bold">${{row.up_count}}</span> / <span class="text-rose-400 font-bold">${{row.down_count}}</span></td>
          <td class="px-4 py-3 text-right font-semibold ${{row.win_rate_pct >= 50 ? 'text-emerald-400' : 'text-rose-400'}}">${{row.win_rate_pct.toFixed(1)}}%</td>
          <td class="px-4 py-3 text-right text-emerald-400 font-mono">+${{row.max_gain_pct.toFixed(2)}}%</td>
          <td class="px-4 py-3 text-right text-rose-400 font-mono">${{row.max_loss_pct.toFixed(2)}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Render Events Table with Filters
    function renderEventsTable() {{
      const tbody = document.getElementById('eventsTableBody');
      const filterSymbol = document.getElementById('filterSymbol').value;
      const filterForm = document.getElementById('filterForm').value;
      const filterSearch = document.getElementById('filterSearch').value.toLowerCase().trim();
      const noEventsMsg = document.getElementById('noEventsMessage');

      tbody.innerHTML = '';

      const filtered = eventsData.filter(item => {{
        if (filterSymbol && item.symbol !== filterSymbol) return false;
        if (filterForm && item.form !== filterForm) return false;
        if (filterSearch) {{
          const str = (item.symbol + ' ' + item.form + ' ' + item.filing_date + ' ' + item.company_name).toLowerCase();
          if (!str.includes(filterSearch)) return false;
        }}
        return true;
      }});

      if (filtered.length === 0) {{
        noEventsMsg.classList.remove('hidden');
      }} else {{
        noEventsMsg.classList.add('hidden');
      }}

      filtered.forEach(ev => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        const color = colors[ev.symbol] || '#ffffff';
        tr.innerHTML = `
          <td class="px-4 py-2.5 font-bold" style="color: ${{color}}">${{ev.symbol}}</td>
          <td class="px-4 py-2.5"><span class="px-2 py-0.5 text-xs font-semibold rounded ${{ev.form === '10-K' ? 'bg-purple-950 text-purple-300 border border-purple-800' : 'bg-blue-950 text-blue-300 border border-blue-800'}}">${{ev.form}}</span></td>
          <td class="px-4 py-2.5 text-slate-300">${{ev.filing_date}}</td>
          <td class="px-4 py-2.5 text-slate-400">${{ev.effective_event_date}}</td>
          <td class="px-4 py-2.5 text-right text-slate-300">$${{ev.base_price.toFixed(2)}}</td>
          <td class="px-4 py-2.5 text-right">${{formatBadge(ev.return_1d_pct)}}</td>
          <td class="px-4 py-2.5 text-right">${{formatBadge(ev.return_3d_pct)}}</td>
          <td class="px-4 py-2.5 text-right">${{formatBadge(ev.return_5d_pct)}}</td>
          <td class="px-4 py-2.5 text-right text-white font-semibold">${{ev.abs_volatility_5d_pct.toFixed(2)}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Setup Charts
    function initCharts() {{
      const symbols = ['AMD', 'INTC', 'MU', 'NVDA', 'QCOM'];

      // Chart 1: Volatility
      const vol1D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+1D').median_abs_volatility_pct);
      const vol3D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+3D').median_abs_volatility_pct);
      const vol5D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+5D').median_abs_volatility_pct);

      new Chart(document.getElementById('chartVolatility'), {{
        type: 'bar',
        data: {{
          labels: symbols,
          datasets: [
            {{ label: '+1D 中位數絕對波動', data: vol1D, backgroundColor: '#38bdf8' }},
            {{ label: '+3D 中位數絕對波動', data: vol3D, backgroundColor: '#fb923c' }},
            {{ label: '+5D 中位數絕對波動', data: vol5D, backgroundColor: '#4ade80' }},
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }}
          }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold' }} }} }}
          }}
        }}
      }});

      // Chart 2: Positive Return Ratio (Win Rate)
      const win1D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+1D').win_rate_pct);
      const win3D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+3D').win_rate_pct);
      const win5D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+5D').win_rate_pct);

      new Chart(document.getElementById('chartWinRate'), {{
        type: 'bar',
        data: {{
          labels: symbols,
          datasets: [
            {{ label: '+1D 歷史正報酬比例', data: win1D, backgroundColor: '#2dd4bf' }},
            {{ label: '+3D 歷史正報酬比例', data: win3D, backgroundColor: '#f43f5e' }},
            {{ label: '+5D 歷史正報酬比例', data: win5D, backgroundColor: '#a855f7' }},
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }}
          }},
          scales: {{
            y: {{ min: 0, max: 100, grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold' }} }} }}
          }}
        }}
      }});

      // Chart 3: Mean Return
      const mean1D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+1D').mean_return_pct);
      const mean3D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+3D').mean_return_pct);
      const mean5D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+5D').mean_return_pct);

      new Chart(document.getElementById('chartMeanReturn'), {{
        type: 'bar',
        data: {{
          labels: symbols,
          datasets: [
            {{ label: '+1D 平均報酬率', data: mean1D, backgroundColor: '#0ea5e9' }},
            {{ label: '+3D 平均報酬率', data: mean3D, backgroundColor: '#eab308' }},
            {{ label: '+5D 平均報酬率', data: mean5D, backgroundColor: '#ec4899' }},
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }}
          }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold' }} }} }}
          }}
        }}
      }});

      // Chart 4: Trajectories
      let trajectoryChart = null;
      function updateTrajectoryChart(selectedSym) {{
        const filteredEvents = selectedSym === 'ALL' ? eventsData : eventsData.filter(e => e.symbol === selectedSym);
        const datasets = filteredEvents.map((ev, idx) => {{
          const isUp = ev.return_1d_pct >= 0;
          return {{
            label: `${{ev.symbol}} (${{ev.filing_date}} ${{ev.form}})`,
            data: [
              {{ x: '+1D', y: ev.return_1d_pct }},
              {{ x: '+3D', y: ev.return_3d_pct }},
              {{ x: '+5D', y: ev.return_5d_pct }}
            ],
            borderColor: selectedSym === 'ALL' ? (colors[ev.symbol] || '#94a3b8') : (isUp ? '#34d399' : '#f87171'),
            backgroundColor: 'transparent',
            borderWidth: 1.5,
            tension: 0.2,
            pointRadius: 3,
          }};
        }});

        if (trajectoryChart) trajectoryChart.destroy();

        trajectoryChart = new Chart(document.getElementById('chartTrajectory'), {{
          type: 'line',
          data: {{
            labels: ['+1D', '+3D', '+5D'],
            datasets: datasets
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: selectedSym !== 'ALL', labels: {{ color: '#94a3b8', font: {{ size: 10 }} }} }}
            }},
            scales: {{
              y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
              x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold' }} }} }}
            }}
          }}
        }});
      }}

      updateTrajectoryChart('ALL');
      document.getElementById('trajectorySymbolSelect').addEventListener('change', e => {{
        updateTrajectoryChart(e.target.value);
      }});
    }}

    // Initialize on page load
    document.addEventListener('DOMContentLoaded', () => {{
      renderSummaryTable();
      renderEventsTable();
      initCharts();

      // Attach filter listeners
      document.getElementById('filterSymbol').addEventListener('change', renderEventsTable);
      document.getElementById('filterForm').addEventListener('change', renderEventsTable);
      document.getElementById('filterSearch').addEventListener('input', renderEventsTable);
    }});
  </script>
</body>
</html>
"""
    return html_content


def export_dashboard():
    html = build_dashboard_html()
    os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)

    # Save to outputs/dashboard.html
    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Saved interactive HTML dashboard to: {OUTPUT_HTML_PATH}")

    # Also save to root dashboard.html for easy one-click access
    with open(ROOT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Saved root interactive dashboard to: {ROOT_HTML_PATH}")


if __name__ == "__main__":
    export_dashboard()
