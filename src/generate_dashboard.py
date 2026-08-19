"""Interactive HTML Dashboard & Presentation Generator for Group 2

Generates a standalone, feature-rich, interactive HTML dashboard & 10-min presentation:
PART 1: Team & Project Hero/Header
PART 2: Core Result Dashboard (KPIs, Charts, Summary Matrix, Event Explorer, CSV export)
PART 3: Corrected Financial Terminology (Historical Positive Return Rate, strictly non-causal)
PART 4: 01｜Project Motivation & Research Question
PART 5: 02｜Data Pipeline & Methodology
PART 6: 03｜AI/Antigravity Development Workflow
PART 7: 04｜Challenges & Problem-Solving
PART 8: 05｜Core Findings & Real Data Insights (3 Cards)
PART 9: 06｜Data Limitations & Disclaimer
PART 10: Footer & GitHub Repository Link

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
    events_path = os.path.join(OUTPUT_TABLES_DIR, "event_details.csv")
    summary_path = os.path.join(OUTPUT_TABLES_DIR, "company_summary.csv")

    if not os.path.exists(events_path) or not os.path.exists(summary_path):
        raise FileNotFoundError("Required output tables not found. Please run analyze_events.py first.")

    events_df = pd.read_csv(events_path)
    summary_df = pd.read_csv(summary_path)

    events_json = events_df.to_json(orient="records")
    summary_json = summary_df.to_json(orient="records")

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>美股半導體財報事件波動分析工具 ｜ 第二組成果報告</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    body {{
      font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #090d16;
      color: #f1f5f9;
    }}
    .font-mono-code {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .glass-card {{
      background: rgba(15, 23, 42, 0.78);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 1rem;
    }}
    .glass-card-accent {{
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
      border: 1px solid rgba(56, 189, 248, 0.2);
    }}
    .glass-card-hover:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
      transition: all 0.2s ease-in-out;
    }}
    .badge-pos {{
      background-color: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
    }}
    .badge-neg {{
      background-color: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.35);
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
      background: #090d16;
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
<body class="min-h-screen p-4 md:p-8 space-y-12">
  <div class="max-w-7xl mx-auto space-y-12">
    
    <!-- ================================================== -->
    <!-- PART 1 ｜ 頁面最上方：專案與組別基本資料 Hero Header -->
    <!-- ================================================== -->
    <header class="glass-card p-6 md:p-8 border-slate-800 relative overflow-hidden">
      <div class="absolute -right-20 -top-20 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-20 -bottom-20 w-80 h-80 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative z-10 space-y-6">
        <!-- Top Meta Tags -->
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex flex-wrap items-center gap-2">
            <span class="px-3.5 py-1 text-xs font-black tracking-widest text-cyan-300 uppercase bg-cyan-950/80 border border-cyan-700/60 rounded-md">
              第二組
            </span>
            <span class="px-3 py-1 text-xs font-semibold text-slate-300 bg-slate-800/90 rounded-md border border-slate-700">
              美股半導體＋財報日 ｜ SEC EDGAR
            </span>
            <span class="text-xs text-slate-400 font-medium">10 分鐘課堂成果報告</span>
          </div>
          
          <div class="flex items-center gap-3">
            <button onclick="window.print()" class="px-3.5 py-1.5 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 transition flex items-center gap-1.5">
              <span>🖨️</span> 列印 / PDF
            </button>
            <a href="tables/event_details.csv" download class="px-3.5 py-1.5 text-xs font-semibold bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition shadow-lg shadow-cyan-900/30 flex items-center gap-1.5">
              <span>📥</span> 下載 CSV 數據
            </a>
          </div>
        </div>

        <!-- Title and Team -->
        <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <div class="space-y-1.5">
            <h1 class="text-3xl md:text-5xl font-black tracking-tight text-white">
              美股半導體財報事件波動分析工具
            </h1>
            <p class="text-slate-400 text-sm md:text-base font-medium tracking-wide">
              Semiconductor Earnings Event Volatility Dashboard
            </p>
          </div>

          <!-- Team Members -->
          <div class="bg-slate-900/80 px-5 py-3 rounded-xl border border-slate-800 flex flex-wrap items-center gap-4 text-xs">
            <span class="text-slate-400 font-bold uppercase tracking-wider">組員</span>
            <div class="flex items-center gap-4 font-mono-code">
              <span class="text-slate-200 font-semibold">B54144035 <strong class="text-cyan-300 font-sans">張丞伶</strong></span>
              <span class="text-slate-200 font-semibold">D44126176 <strong class="text-cyan-300 font-sans">賴則維</strong></span>
              <span class="text-slate-200 font-semibold">E34141133 <strong class="text-cyan-300 font-sans">劉宇博</strong></span>
            </div>
          </div>
        </div>

        <!-- Info Badges Bar -->
        <div class="pt-4 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div class="bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/60">
            <span class="text-slate-500 font-medium block">分析標的</span>
            <span class="text-slate-200 font-bold">NVDA · AMD · INTC · QCOM · MU</span>
          </div>
          <div class="bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/60">
            <span class="text-slate-500 font-medium block">資料來源</span>
            <span class="text-slate-200 font-bold">SEC EDGAR × Yahoo Finance</span>
          </div>
          <div class="bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/60">
            <span class="text-slate-500 font-medium block">分析期間</span>
            <span class="text-slate-200 font-bold">近兩年滾動歷史區間</span>
          </div>
          <div class="bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/60">
            <span class="text-slate-500 font-medium block">事件類型</span>
            <span class="text-slate-200 font-bold">10-Q (季報) / 10-K (年報)</span>
          </div>
        </div>

      </div>
    </header>


    <!-- ================================================== -->
    <!-- PART 2 ｜ 成果 DASHBOARD (整份頁面的視覺核心) -->
    <!-- ================================================== -->
    <section class="space-y-6">
      
      <!-- Section Title Badge -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-2.5 h-7 bg-cyan-400 rounded-full shadow-lg shadow-cyan-400/50"></div>
          <h2 class="text-2xl md:text-3xl font-black text-white tracking-tight">成果 Dashboard</h2>
          <span class="text-xs px-2.5 py-1 bg-cyan-950/60 border border-cyan-800 text-cyan-300 rounded-md font-semibold">
            即時動態成果展示
          </span>
        </div>
        <div class="text-xs text-slate-400 hidden sm:block">
          * 數據基於真實近兩年 40 場 SEC 財報申報事件
        </div>
      </div>

      <!-- 1. KPI 摘要卡片 -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider">總分析財報事件</div>
          <div class="text-3xl md:text-4xl font-extrabold text-white mt-2">40 <span class="text-sm font-normal text-slate-400">場</span></div>
          <div class="text-xs text-slate-400 mt-1">5 檔標的 × 各 8 次 (6 次 10-Q + 2 次 10-K)</div>
        </div>

        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider">+1D 絕對波動最高</div>
          <div class="text-3xl md:text-4xl font-extrabold text-amber-400 mt-2">INTC <span class="text-xl">7.26%</span></div>
          <div class="text-xs text-slate-400 mt-1">中位數絕對波動 (+5D 達 9.75%)</div>
        </div>

        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider">+1D 歷史正報酬比例最高</div>
          <div class="text-3xl md:text-4xl font-extrabold text-emerald-400 mt-2">QCOM <span class="text-xl">75.0%</span></div>
          <div class="text-xs text-slate-400 mt-1">近兩年 8 次事件中 6 次 +1D 為正報酬</div>
        </div>

        <div class="glass-card p-5 glass-card-hover">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider">NVDA +3D 歷史現象</div>
          <div class="text-3xl md:text-4xl font-extrabold text-rose-400 mt-2">0.0% <span class="text-sm font-normal text-slate-400">正報酬</span></div>
          <div class="text-xs text-slate-400 mt-1">8 次事件在 +3D 均為負 (不代表未來必然下跌)</div>
        </div>

      </div>

      <!-- 2. 四大互動圖表 (Chart.js) -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Chart 1: Median Volatility -->
        <div class="glass-card p-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-bold text-white">五家公司中位數絕對波動比較 (+1D / +3D / +5D)</h3>
              <p class="text-xs text-slate-400">衡量財報公布後市場的絕對重定價幅度（不分漲跌）</p>
            </div>
            <span class="text-xs px-2.5 py-1 bg-slate-800 rounded font-semibold text-slate-300 font-mono-code">%</span>
          </div>
          <div class="h-72">
            <canvas id="chartVolatility"></canvas>
          </div>
        </div>

        <!-- Chart 2: Positive Return Ratio -->
        <div class="glass-card p-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-bold text-white">歷史正報酬比例比較 (Historical Positive Return Rate)</h3>
              <p class="text-xs text-slate-400">近兩年各天期正報酬事件次數比例（紅虛線為 50% 基準線，非未來機率）</p>
            </div>
            <span class="text-xs px-2.5 py-1 bg-slate-800 rounded font-semibold text-slate-300 font-mono-code">基準: 50%</span>
          </div>
          <div class="h-72">
            <canvas id="chartWinRate"></canvas>
          </div>
        </div>

        <!-- Chart 3: Mean Return -->
        <div class="glass-card p-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-bold text-white">平均報酬率比較 (+1D / +3D / +5D)</h3>
              <p class="text-xs text-slate-400">反映歷史樣本在各天期之方向性平均幅度</p>
            </div>
            <span class="text-xs px-2.5 py-1 bg-slate-800 rounded font-semibold text-slate-300 font-mono-code">%</span>
          </div>
          <div class="h-72">
            <canvas id="chartMeanReturn"></canvas>
          </div>
        </div>

        <!-- Chart 4: Interactive Trajectory Simulator -->
        <div class="glass-card p-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
            <div>
              <h3 class="text-lg font-bold text-white">個別財報事件軌跡 (+1D → +3D → +5D)</h3>
              <p class="text-xs text-slate-400">點選切換檢視個別公司每場財報公布後的走勢演變</p>
            </div>
            <select id="trajectorySymbolSelect" class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-cyan-500 font-semibold">
              <option value="ALL">全部標的走勢彙總</option>
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

      </div>

      <!-- 3. 五家公司統計矩陣 (Summary Matrix Table) -->
      <div class="glass-card p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-bold text-white">五家公司完整統計矩陣</h3>
            <p class="text-xs text-slate-400">各標的在 +1D、+3D、+5D 之波動、報酬與正負次數統計</p>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm text-slate-300">
            <thead class="text-xs uppercase bg-slate-800/90 text-slate-400 border-b border-slate-700">
              <tr>
                <th class="px-4 py-3 font-semibold">股票代碼</th>
                <th class="px-4 py-3 font-semibold">天期</th>
                <th class="px-4 py-3 font-semibold text-right">中位數絕對波動</th>
                <th class="px-4 py-3 font-semibold text-right">平均報酬率</th>
                <th class="px-4 py-3 font-semibold text-right">中位數報酬率</th>
                <th class="px-4 py-3 font-semibold text-center">正 / 負次數</th>
                <th class="px-4 py-3 font-semibold text-right">歷史正報酬比例</th>
                <th class="px-4 py-3 font-semibold text-right">歷史最大漲幅</th>
                <th class="px-4 py-3 font-semibold text-right">歷史最大跌幅</th>
              </tr>
            </thead>
            <tbody id="summaryTableBody" class="divide-y divide-slate-800 text-xs md:text-sm">
              <!-- Rendered by JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- 4. Event Explorer (逐事件明細篩選器) -->
      <div class="glass-card p-6">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h3 class="text-xl font-bold text-white">Event Explorer ｜ 逐事件明細搜尋器</h3>
            <p class="text-xs text-slate-400 mt-0.5">點擊表頭可排序，支援公司、申報表 (10-Q/10-K) 與關鍵字即時篩選</p>
          </div>
          <div class="flex flex-wrap items-center gap-3">
            <!-- Filter Symbol -->
            <select id="filterSymbol" class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500 font-semibold">
              <option value="">所有股票 (All Symbols)</option>
              <option value="NVDA">NVDA</option>
              <option value="AMD">AMD</option>
              <option value="INTC">INTC</option>
              <option value="QCOM">QCOM</option>
              <option value="MU">MU</option>
            </select>
            <!-- Filter Form -->
            <select id="filterForm" class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500 font-semibold">
              <option value="">所有申報類型 (All Forms)</option>
              <option value="10-Q">10-Q (季報)</option>
              <option value="10-K">10-K (年報)</option>
            </select>
            <!-- Search Input -->
            <input type="text" id="filterSearch" placeholder="搜尋日期、公司代碼..." class="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 w-48 focus:outline-none focus:border-cyan-500" />
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm text-slate-300">
            <thead class="text-xs uppercase bg-slate-800/90 text-slate-400 border-b border-slate-700">
              <tr>
                <th class="px-4 py-3 font-semibold">標的</th>
                <th class="px-4 py-3 font-semibold">申報表</th>
                <th class="px-4 py-3 font-semibold">SEC 申報日</th>
                <th class="px-4 py-3 font-semibold">有效交易日</th>
                <th class="px-4 py-3 font-semibold text-right">基準價 (T-1)</th>
                <th class="px-4 py-3 font-semibold text-right">+1D 報酬</th>
                <th class="px-4 py-3 font-semibold text-right">+3D 報酬</th>
                <th class="px-4 py-3 font-semibold text-right">+5D 報酬</th>
                <th class="px-4 py-3 font-semibold text-right">+5D 絕對波動</th>
              </tr>
            </thead>
            <tbody id="eventsTableBody" class="divide-y divide-slate-800 font-mono-code text-xs">
              <!-- Rendered by JS -->
            </tbody>
          </table>
        </div>
        <div id="noEventsMessage" class="hidden text-center py-8 text-slate-500 text-sm">
          查無符合條件的財報事件。
        </div>
      </div>

    </section>


    <!-- ================================================== -->
    <!-- PART 4 ｜ 01｜專案想法：我們為什麼做這個工具？ -->
    <!-- ================================================== -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-7 bg-blue-500 rounded-full shadow-lg shadow-blue-500/50"></div>
        <h2 class="text-2xl font-black text-white tracking-tight">01 ｜ 專案想法：我們為什麼做這個工具？</h2>
      </div>

      <div class="space-y-4 text-slate-300 text-sm md:text-base leading-relaxed">
        <p>
          財報公布是股票市場的重要事件，不同半導體公司的股價反應可能存在明顯差異。
        </p>
        <p>
          因此我們希望建立一個可以自動抓取資料並分析的工具，結合 SEC 官方財報申報資料與歷史股價，觀察五家美國半導體公司在財報事件後的短期市場反應。
        </p>
      </div>

      <!-- Core Question Highlight Box -->
      <div class="glass-card-accent p-6 rounded-xl border border-cyan-500/30 text-center space-y-2">
        <div class="text-xs font-bold uppercase tracking-widest text-cyan-400">核心問題 (Core Research Question)</div>
        <div class="text-lg md:text-2xl font-black text-white leading-snug">
          「NVDA、AMD、INTC、QCOM、MU 發布財報後，<br />
          <span class="text-amber-400">未來 1、3、5 個交易日通常會移動多大？</span>
          是否存在值得觀察的歷史特徵？」
        </div>
      </div>
    </section>


    <!-- ================================================== -->
    <!-- PART 5 ｜ 02｜資料與方法 -->
    <!-- ================================================== -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-7 bg-cyan-500 rounded-full shadow-lg shadow-cyan-500/50"></div>
        <h2 class="text-2xl font-black text-white tracking-tight">02 ｜ 資料與方法</h2>
      </div>

      <!-- Visual Pipeline Flow -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-center">
        
        <div class="bg-slate-800/80 p-4 rounded-xl border border-slate-700 flex flex-col justify-between">
          <div class="text-xs text-cyan-400 font-bold">資料源 ①</div>
          <div class="text-sm font-black text-white mt-1">SEC EDGAR</div>
          <div class="text-xs text-slate-400 mt-1 font-mono-code">10-Q / 10-K</div>
          <div class="text-slate-500 font-bold text-xs mt-2">➔</div>
        </div>

        <div class="bg-slate-800/80 p-4 rounded-xl border border-slate-700 flex flex-col justify-between">
          <div class="text-xs text-cyan-400 font-bold">定位事件</div>
          <div class="text-sm font-black text-white mt-1">取得 filingDate</div>
          <div class="text-xs text-slate-400 mt-1">官方申報日</div>
          <div class="text-slate-500 font-bold text-xs mt-2">➔</div>
        </div>

        <div class="bg-slate-800/80 p-4 rounded-xl border border-slate-700 flex flex-col justify-between">
          <div class="text-xs text-cyan-400 font-bold">資料源 ②</div>
          <div class="text-sm font-black text-white mt-1">Yahoo Finance</div>
          <div class="text-xs text-slate-400 mt-1">歷史日線股價</div>
          <div class="text-slate-500 font-bold text-xs mt-2">➔</div>
        </div>

        <div class="bg-slate-800/80 p-4 rounded-xl border border-slate-700 flex flex-col justify-between">
          <div class="text-xs text-cyan-400 font-bold">對齊規則</div>
          <div class="text-sm font-black text-white mt-1">交易日對齊</div>
          <div class="text-xs text-slate-400 mt-1">T-1 基準收盤價</div>
          <div class="text-slate-500 font-bold text-xs mt-2">➔</div>
        </div>

        <div class="bg-slate-800/80 p-4 rounded-xl border border-slate-700 flex flex-col justify-between">
          <div class="text-xs text-cyan-400 font-bold">波動計算</div>
          <div class="text-sm font-black text-white mt-1">+1D / +3D / +5D</div>
          <div class="text-xs text-slate-400 mt-1">報酬與絕對波動</div>
          <div class="text-slate-500 font-bold text-xs mt-2">➔</div>
        </div>

        <div class="bg-cyan-950/40 p-4 rounded-xl border border-cyan-700/60 flex flex-col justify-between">
          <div class="text-xs text-cyan-300 font-bold">分析產出</div>
          <div class="text-sm font-black text-white mt-1">五家公司比較</div>
          <div class="text-xs text-cyan-400 mt-1">統計矩陣 & 圖表</div>
          <div class="text-cyan-400 font-bold text-xs mt-2">✓ 完成</div>
        </div>

      </div>

      <!-- Overview Info -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
        <div class="bg-slate-900/60 p-4 rounded-lg border border-slate-800">
          <span class="text-xs font-bold uppercase tracking-wider text-cyan-400 block mb-1">分析標的</span>
          <span class="text-sm font-semibold text-slate-200">NVDA (NVIDIA)、AMD、INTC (Intel)、QCOM (Qualcomm)、MU (Micron)</span>
        </div>
        <div class="bg-slate-900/60 p-4 rounded-lg border border-slate-800">
          <span class="text-xs font-bold uppercase tracking-wider text-cyan-400 block mb-1">主要分析指標</span>
          <span class="text-sm font-semibold text-slate-200">報酬率 (%) · 絕對波動 (%) · 中位數 · 平均數 · 歷史正報酬比例</span>
        </div>
      </div>
    </section>


    <!-- ================================================== -->
    <!-- PART 6 ｜ 03｜我們怎麼把工具做出來？ -->
    <!-- ================================================== -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-7 bg-purple-500 rounded-full shadow-lg shadow-purple-500/50"></div>
        <h2 class="text-2xl font-black text-white tracking-tight">03 ｜ 我們怎麼把工具做出來？</h2>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div class="bg-slate-800/60 p-5 rounded-xl border border-slate-700 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-purple-400 uppercase">步驟 1</span>
            <span class="w-6 h-6 rounded-full bg-purple-900/60 text-purple-300 flex items-center justify-center font-bold text-xs">1</span>
          </div>
          <h3 class="text-base font-bold text-white">① 需求拷問與 PLAN</h3>
          <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
            先確定股票、資料來源、事件定義、分析期間、輸出方式與驗收條件。
          </p>
        </div>

        <div class="bg-slate-800/60 p-5 rounded-xl border border-slate-700 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-blue-400 uppercase">步驟 2</span>
            <span class="w-6 h-6 rounded-full bg-blue-900/60 text-blue-300 flex items-center justify-center font-bold text-xs">2</span>
          </div>
          <h3 class="text-base font-bold text-white">② Python / 資料抓取</h3>
          <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
            利用 Python 從 SEC EDGAR 取得 10-Q / 10-K filing，並取得 Yahoo Finance 歷史股價。
          </p>
        </div>

        <div class="bg-slate-800/60 p-5 rounded-xl border border-slate-700 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-cyan-400 uppercase">步驟 3</span>
            <span class="w-6 h-6 rounded-full bg-cyan-900/60 text-cyan-300 flex items-center justify-center font-bold text-xs">3</span>
          </div>
          <h3 class="text-base font-bold text-white">③ Antigravity 實作</h3>
          <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
            使用 Antigravity 協助建立資料清理、事件分析、視覺化與測試流程。
          </p>
        </div>

        <div class="bg-slate-800/60 p-5 rounded-xl border border-slate-700 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-emerald-400 uppercase">步驟 4</span>
            <span class="w-6 h-6 rounded-full bg-emerald-900/60 text-emerald-300 flex items-center justify-center font-bold text-xs">4</span>
          </div>
          <h3 class="text-base font-bold text-white">④ 測試與驗收</h3>
          <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
            實際執行 pipeline，並透過測試、CSV 與視覺化結果確認資料與計算是否正常。
          </p>
        </div>

      </div>
    </section>


    <!-- ================================================== -->
    <!-- PART 7 ｜ 04｜遇到什麼問題？ -->
    <!-- ================================================== -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-7 bg-amber-500 rounded-full shadow-lg shadow-amber-500/50"></div>
        <h2 class="text-2xl font-black text-white tracking-tight">04 ｜ 遇到什麼問題？</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        
        <!-- Problem 1 -->
        <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-800 space-y-3">
          <div class="space-y-1">
            <span class="text-xs font-black text-rose-400 uppercase tracking-wider">Problem 1 ｜ 執行步驟偏差</span>
            <p class="text-sm font-semibold text-slate-200">
              原本規劃按照 TASK 一步一步開發，但第一次交給 Antigravity 實作後，AI 直接建立了完整 pipeline。
            </p>
          </div>
          <div class="pt-2 border-t border-slate-800 space-y-1">
            <span class="text-xs font-black text-emerald-400 uppercase tracking-wider">Solution ｜ 嚴格驗收</span>
            <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
              我們沒有直接把「AI 顯示完成」當作成功，而是重新透過實際執行、單元測試、CSV 與圖表結果進行驗收。
            </p>
          </div>
        </div>

        <!-- Problem 2 -->
        <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-800 space-y-3">
          <div class="space-y-1">
            <span class="text-xs font-black text-rose-400 uppercase tracking-wider">Problem 2 ｜ 非交易日對齊</span>
            <p class="text-sm font-semibold text-slate-200">
              SEC filingDate 與股票交易日不一定直接對應，例如週末或非交易日。
            </p>
          </div>
          <div class="pt-2 border-t border-slate-800 space-y-1">
            <span class="text-xs font-black text-emerald-400 uppercase tracking-wider">Solution ｜ 交易日序列對齊</span>
            <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
              將事件日期與實際交易日資料進行對齊，再計算事件後 +1D / +3D / +5D。
            </p>
          </div>
        </div>

        <!-- Problem 3 -->
        <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-800 space-y-3">
          <div class="space-y-1">
            <span class="text-xs font-black text-rose-400 uppercase tracking-wider">Problem 3 ｜ SEC 限制</span>
            <p class="text-sm font-semibold text-slate-200">
              SEC EDGAR API 初始請求時因 User-Agent Email 格式包含符號遭伺服器 HTTP 403 阻擋。
            </p>
          </div>
          <div class="pt-2 border-t border-slate-800 space-y-1">
            <span class="text-xs font-black text-emerald-400 uppercase tracking-wider">Solution ｜ 合規 Header</span>
            <p class="text-xs md:text-sm text-slate-400 leading-relaxed">
              依據 SEC 官方規範調整合規格式之 User-Agent Header，順利通過 API 驗證。
            </p>
          </div>
        </div>

      </div>
    </section>


    <!-- ================================================== -->
    <!-- PART 8 ｜ 05｜我們發現了什麼？ (3 個核心 Insight Cards) -->
    <!-- ================================================== -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-7 bg-emerald-500 rounded-full shadow-lg shadow-emerald-500/50"></div>
        <h2 class="text-2xl font-black text-white tracking-tight">05 ｜ 我們發現了什麼？</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <!-- Insight 1: INTC & AMD Volatility -->
        <div class="bg-slate-900/90 p-6 rounded-xl border border-slate-800 flex flex-col justify-between space-y-4">
          <div class="space-y-2">
            <div class="text-xs font-bold uppercase tracking-wider text-amber-400">發現 ① ｜ 典型短期波動最大</div>
            <h3 class="text-lg font-bold text-white">INTC 與 AMD 財報後震盪最劇烈</h3>
            <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
              在公布後首個交易日 (+1D)，<strong>INTC</strong> 中位數絕對波動達 <span class="text-amber-400 font-bold">7.26%</span>（+5D 達 9.75%），<strong>AMD</strong> 達 <span class="text-amber-400 font-bold">6.73%</span>（+5D 達 10.16%）。INTC 於 +5D 歷史最大單次震盪高達 +41.48% 與 -19.13%，市場重定價幅度在 5 家中最高。
            </p>
          </div>
          <div class="bg-slate-800/80 px-3.5 py-2 rounded-lg text-xs font-mono-code text-slate-300">
            INTC +1D: 7.26% ｜ AMD +1D: 6.73%
          </div>
        </div>

        <!-- Insight 2: QCOM Positive Ratio -->
        <div class="bg-slate-900/90 p-6 rounded-xl border border-slate-800 flex flex-col justify-between space-y-4">
          <div class="space-y-2">
            <div class="text-xs font-bold uppercase tracking-wider text-emerald-400">發現 ② ｜ 首日歷史正報酬比例</div>
            <h3 class="text-lg font-bold text-white">QCOM +1D 呈現較高正報酬比例</h3>
            <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
              近兩年 8 次財報事件中，<strong>QCOM</strong> 有 6 次在 +1D 報酬為正，歷史正報酬比例為 <span class="text-emerald-400 font-bold">75%</span>（+1D 平均報酬率為 +1.23%）。此為歷史樣本之客觀描述，不代表未來必然上漲。
            </p>
          </div>
          <div class="bg-slate-800/80 px-3.5 py-2 rounded-lg text-xs font-mono-code text-slate-300">
            QCOM +1D 歷史正報酬比例: 75% (6/8 次)
          </div>
        </div>

        <!-- Insight 3: NVDA +3D Phenomenon -->
        <div class="bg-slate-900/90 p-6 rounded-xl border border-slate-800 flex flex-col justify-between space-y-4">
          <div class="space-y-2">
            <div class="text-xs font-bold uppercase tracking-wider text-rose-400">發現 ③ ｜ 樣本歷史特殊現象</div>
            <h3 class="text-lg font-bold text-white">NVDA +3D 在樣本中皆為負報酬</h3>
            <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
              近兩年樣本中，<strong>NVDA</strong> 的 8 次財報事件在 +3D 均呈現負報酬，歷史正報酬比例為 <span class="text-rose-400 font-bold">0%</span>（中位數報酬率 -2.92%）。此結果為樣本期間內的歷史描述，樣本數有限，不代表未來必然下跌。
            </p>
          </div>
          <div class="bg-slate-800/80 px-3.5 py-2 rounded-lg text-xs font-mono-code text-slate-300">
            NVDA +3D 歷史正報酬比例: 0% (0/8 次)
          </div>
        </div>

      </div>
    </section>


    <!-- ================================================== -->
    <!-- PART 9 ｜ 06｜資料限制 -->
    <!-- ================================================== -->
    <section class="glass-card p-6 md:p-8 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-7 bg-rose-500 rounded-full shadow-lg shadow-rose-500/50"></div>
        <h2 class="text-2xl font-black text-white tracking-tight">06 ｜ 資料限制</h2>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        
        <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
          <span class="text-rose-400 font-bold text-base mt-0.5">1.</span>
          <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
            SEC <code>filingDate</code> 是 SEC 文件申報日期，不一定完全等同市場實際 earnings announcement time。
          </p>
        </div>

        <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
          <span class="text-rose-400 font-bold text-base mt-0.5">2.</span>
          <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
            目前沒有區分財報是在盤前或盤後發布。
          </p>
        </div>

        <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
          <span class="text-rose-400 font-bold text-base mt-0.5">3.</span>
          <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
            每家公司近兩年約只有 8 次事件，樣本數有限。
          </p>
        </div>

        <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
          <span class="text-rose-400 font-bold text-base mt-0.5">4.</span>
          <p class="text-xs md:text-sm text-slate-300 leading-relaxed">
            本工具分析的是歷史事件後的價格反應，不能將歷史正報酬比例直接解讀為未來上漲機率。
          </p>
        </div>

      </div>

      <!-- Prominent Positioning Statement Banner -->
      <div class="bg-gradient-to-r from-slate-900 via-cyan-950/40 to-slate-900 p-4 rounded-xl border border-cyan-700/40 text-center">
        <span class="text-xs md:text-sm font-bold text-cyan-300 tracking-wide">
          📌 本工具定位為歷史事件分析與資料探索工具，而非投資預測模型。
        </span>
      </div>
    </section>


    <!-- ================================================== -->
    <!-- PART 10 ｜ 頁面最底部：收尾與 Repository 資訊 -->
    <!-- ================================================== -->
    <footer class="glass-card p-6 md:p-8 border-slate-800 text-center space-y-3">
      <div class="text-base md:text-lg font-black text-white">
        第二組 ｜ 美股半導體＋財報日 ｜ SEC EDGAR
      </div>
      <div class="text-xs md:text-sm text-slate-400 font-medium font-mono-code">
        SEC EDGAR × Yahoo Finance × Python × Antigravity
      </div>
      <div class="pt-2">
        <a href="https://github.com/Ryoma1022/G2" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-400 text-xs font-mono-code rounded-lg border border-slate-700 transition">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
          </svg>
          https://github.com/Ryoma1022/G2
        </a>
      </div>
    </footer>

  </div>

  <!-- SCRIPT LOGIC (Interactive Dashboard Functionality) -->
  <script>
    const eventsData = {events_json};
    const summaryData = {summary_json};

    const colors = {{
      NVDA: '#10b981',
      AMD: '#f59e0b',
      INTC: '#3b82f6',
      QCOM: '#8b5cf6',
      MU: '#ec4899',
    }};

    function formatBadge(val) {{
      if (val === null || isNaN(val)) return '<span class="px-2 py-0.5 rounded badge-neutral">N/A</span>';
      const num = Number(val);
      const sign = num > 0 ? '+' : '';
      const cls = num > 0 ? 'badge-pos' : (num < 0 ? 'badge-neg' : 'badge-neutral');
      return `<span class="px-2 py-0.5 rounded font-semibold ${{cls}}">${{sign}}${{num.toFixed(2)}}%</span>`;
    }}

    function renderSummaryTable() {{
      const tbody = document.getElementById('summaryTableBody');
      tbody.innerHTML = '';
      summaryData.forEach(row => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        const color = colors[row.symbol] || '#ffffff';
        tr.innerHTML = `
          <td class="px-4 py-3 font-bold" style="color: ${{color}}">${{row.symbol}}</td>
          <td class="px-4 py-3"><span class="px-2 py-0.5 bg-slate-800 rounded text-slate-300 text-xs font-mono-code font-bold">${{row.horizon}}</span></td>
          <td class="px-4 py-3 text-right font-bold text-white font-mono-code">${{row.median_abs_volatility_pct.toFixed(2)}}%</td>
          <td class="px-4 py-3 text-right font-mono-code">${{formatBadge(row.mean_return_pct)}}</td>
          <td class="px-4 py-3 text-right font-mono-code">${{formatBadge(row.median_return_pct)}}</td>
          <td class="px-4 py-3 text-center text-xs font-mono-code"><span class="text-emerald-400 font-bold">${{row.up_count}}</span> / <span class="text-rose-400 font-bold">${{row.down_count}}</span></td>
          <td class="px-4 py-3 text-right font-bold font-mono-code ${{row.win_rate_pct >= 50 ? 'text-emerald-400' : 'text-rose-400'}}">${{row.win_rate_pct.toFixed(1)}}%</td>
          <td class="px-4 py-3 text-right text-emerald-400 font-mono-code font-bold">+${{row.max_gain_pct.toFixed(2)}}%</td>
          <td class="px-4 py-3 text-right text-rose-400 font-mono-code font-bold">${{row.max_loss_pct.toFixed(2)}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

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
        tr.className = 'hover:bg-slate-800/60 transition';
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
          <td class="px-4 py-2.5 text-right text-white font-bold">${{ev.abs_volatility_5d_pct.toFixed(2)}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

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
            legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 11, weight: 'bold' }} }} }}
          }},
          scales: {{
            y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold', size: 12 }} }} }}
          }}
        }}
      }});

      // Chart 2: Positive Return Ratio
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
            legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 11, weight: 'bold' }} }} }}
          }},
          scales: {{
            y: {{ min: 0, max: 100, grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold', size: 12 }} }} }}
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
            legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 11, weight: 'bold' }} }} }}
          }},
          scales: {{
            y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold', size: 12 }} }} }}
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
            borderWidth: 1.8,
            tension: 0.2,
            pointRadius: 3.5,
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
              y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
              x: {{ grid: {{ display: false }}, ticks: {{ color: '#f1f5f9', font: {{ weight: 'bold', size: 12 }} }} }}
            }}
          }}
        }});
      }}

      updateTrajectoryChart('ALL');
      document.getElementById('trajectorySymbolSelect').addEventListener('change', e => {{
        updateTrajectoryChart(e.target.value);
      }});
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      renderSummaryTable();
      renderEventsTable();
      initCharts();

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

    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Saved interactive HTML presentation dashboard to: {OUTPUT_HTML_PATH}")

    with open(ROOT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Saved root interactive presentation dashboard to: {ROOT_HTML_PATH}")


if __name__ == "__main__":
    export_dashboard()
