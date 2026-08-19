"""Interactive HTML Dashboard Generator

Generates a standalone, feature-rich, interactive HTML dashboard
containing interactive Chart.js visualizations, KPI metric cards,
filterable event explorer tables, and analytical summaries.
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
  <title>美股半導體財報事件波動分析儀表板</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    body {{
      font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #0f172a;
      color: #f1f5f9;
    }}
    .glass-card {{
      background: rgba(30, 41, 59, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 1rem;
    }}
    .glass-card-hover:hover {{
      border-color: rgba(56, 189, 248, 0.3);
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
      background: #0f172a;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 4px;
    }}
  </style>
</head>
<body class="min-h-screen p-4 md:p-8">
  <div class="max-w-7xl mx-auto space-y-8">
    
    <!-- HEADER -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
      <div>
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 text-xs font-semibold tracking-wider text-cyan-400 uppercase bg-cyan-950/60 border border-cyan-800 rounded-full">
            SEC EDGAR + YAHOO FINANCE
          </span>
          <span class="text-xs text-slate-400">近兩年滾動分析 (2024~2026)</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight text-white mt-2">
          美股半導體財報事件波動分析儀表板
        </h1>
        <p class="text-slate-400 text-sm md:text-base mt-1">
          追蹤 <strong class="text-cyan-400">NVDA</strong>、<strong class="text-cyan-400">AMD</strong>、<strong class="text-cyan-400">INTC</strong>、<strong class="text-cyan-400">QCOM</strong>、<strong class="text-cyan-400">MU</strong> 在 10-Q / 10-K 申報後第 1、3、5 交易日之歷史波動與報酬
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

    <!-- KPI CARDS -->
    <section class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="glass-card p-5 glass-card-hover">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">總分析財報事件</div>
        <div class="text-3xl font-extrabold text-white mt-2">40 <span class="text-sm font-normal text-slate-400">場</span></div>
        <div class="text-xs text-slate-400 mt-1">5 檔標的 × 各 8 次 (6 次 10-Q + 2 次 10-K)</div>
      </div>

      <div class="glass-card p-5 glass-card-hover">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">+1D 波動冠軍</div>
        <div class="text-3xl font-extrabold text-amber-400 mt-2">INTC <span class="text-lg">7.26%</span></div>
        <div class="text-xs text-slate-400 mt-1">中位數絕對波動 (+5D 達 9.75%)</div>
      </div>

      <div class="glass-card p-5 glass-card-hover">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">+1D 上漲勝率王</div>
        <div class="text-3xl font-extrabold text-emerald-400 mt-2">QCOM <span class="text-lg">75.0%</span></div>
        <div class="text-xs text-slate-400 mt-1">8 次事件中 6 次首日收紅</div>
      </div>

      <div class="glass-card p-5 glass-card-hover">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">NVDA +3D 現象</div>
        <div class="text-3xl font-extrabold text-rose-400 mt-2">0.0% <span class="text-sm font-normal text-slate-400">勝率</span></div>
        <div class="text-xs text-slate-400 mt-1">8 次事件在第 3 日均呈現拉回調整</div>
      </div>
    </section>

    <!-- INTERACTIVE CHARTS SECTION -->
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

      <!-- Chart 2: Win Rate -->
      <div class="glass-card p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-lg font-bold text-white">財報後上漲機率對比 (Win Rate)</h2>
            <p class="text-xs text-slate-400">正報酬比例 (紅虛線為 50% 多空分界)</p>
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
            <p class="text-xs text-slate-400">反映整體方向性期望值</p>
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
            <p class="text-xs text-slate-400">點選標的切換單一公司的各場事件曲線</p>
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

    <!-- SUMMARY METRICS TABLE -->
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
              <th class="px-4 py-3 font-semibold text-right">上漲勝率</th>
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

    <!-- EVENT EXPLORER WITH FILTERS -->
    <section class="glass-card p-6">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h2 class="text-xl font-bold text-white">財報事件詳細明細搜尋器 (Event Explorer)</h2>
          <p class="text-xs text-slate-400 mt-0.5">點擊表頭可排序，支援公司、申報類別與日期篩選</p>
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

    <!-- KEY INSIGHTS & METHODOLOGY NOTES -->
    <footer class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-800 text-xs text-slate-400">
      <div class="space-y-2">
        <h3 class="text-sm font-bold text-slate-200">📌 核心統計發現與觀察</h3>
        <ul class="list-disc list-inside space-y-1 text-slate-400 leading-relaxed">
          <li><strong>重定價幅度</strong>：INTC (7.26%) 與 AMD (6.73%) 在 +1D 的波動度顯著高於其他三家。</li>
          <li><strong>利多出盡 / 拉回現象</strong>：NVDA 在 +1D 上漲機率為 50%，但在 +3D 上漲勝率為 0.0%，中位數報酬為 -2.92%，反映市場公布後短期容易出現資金獲利了結。</li>
          <li><strong>勝率表現</strong>：QCOM 在發布後 +1D 的勝率達 75.0%，為五家中最具正向偏向的標的。</li>
        </ul>
      </div>
      <div class="space-y-2">
        <h3 class="text-sm font-bold text-slate-200">⚠️ 資料與計算規則說明</h3>
        <ul class="list-disc list-inside space-y-1 text-slate-400 leading-relaxed">
          <li><strong>事件日對齊</strong>：採 SEC EDGAR <code>filingDate</code>，遇非交易日自動對應其後最近之有效交易日。</li>
          <li><strong>基準收盤價</strong>：取有效事件日前一個交易日的 Close 價格。</li>
          <li><strong>交易日序列</strong>：+1D 為事件當日、+3D 為 index+2、+5D 為 index+4，不採日曆日直接加減。</li>
          <li><strong>免責聲明</strong>：本儀表板僅提供歷史波動參考，不預測未來股價走勢，不構成投資建議。</li>
        </ul>
      </div>
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
            {{ label: '+1D 中位數波動', data: vol1D, backgroundColor: '#38bdf8' }},
            {{ label: '+3D 中位數波動', data: vol3D, backgroundColor: '#fb923c' }},
            {{ label: '+5D 中位數波動', data: vol5D, backgroundColor: '#4ade80' }},
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

      // Chart 2: Win Rate
      const win1D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+1D').win_rate_pct);
      const win3D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+3D').win_rate_pct);
      const win5D = symbols.map(s => summaryData.find(d => d.symbol === s && d.horizon === '+5D').win_rate_pct);

      new Chart(document.getElementById('chartWinRate'), {{
        type: 'bar',
        data: {{
          labels: symbols,
          datasets: [
            {{ label: '+1D 勝率', data: win1D, backgroundColor: '#2dd4bf' }},
            {{ label: '+3D 勝率', data: win3D, backgroundColor: '#f43f5e' }},
            {{ label: '+5D 勝率', data: win5D, backgroundColor: '#a855f7' }},
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
            {{ label: '+1D 平均報酬', data: mean1D, backgroundColor: '#0ea5e9' }},
            {{ label: '+3D 平均報酬', data: mean3D, backgroundColor: '#eab308' }},
            {{ label: '+5D 平均報酬', data: mean5D, backgroundColor: '#ec4899' }},
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
