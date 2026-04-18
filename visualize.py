import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates

plt.rcParams['font.family'] = 'DejaVu Sans'

market = pd.read_csv('data/market_data.csv', index_col=0, parse_dates=True)
market.index = pd.to_datetime(market.index).tz_localize(None)

# 2025년 7월부터만
market = market[market.index >= '2025-07-01']

events = [
    ('2026-01-08', 'Locked &\nLoaded', 'orange'),
    ('2026-02-24', 'Nuclear\nWarning', 'orange'),
    ('2026-02-28', 'Operation\nEpic Fury', 'red'),
    ('2026-03-09', 'Navy\nSunk', 'blue'),
    ('2026-03-13', 'Hormuz\nMines', 'orange'),
    ('2026-04-07', 'Civilisation\nWill Die', 'red'),
]

fig, axes = plt.subplots(4, 1, figsize=(16, 20), sharex=True)
fig.suptitle("Trump War Statements vs Market Impact (2025H2 - 2026)", 
             fontsize=16, fontweight='bold', y=0.98)

tickers = ['WTI', 'DOW', 'XOM', 'LYB']
colors = ['black', 'steelblue', 'darkorange', 'green']
labels = ['WTI Crude Oil', 'Dow Chemical', 'ExxonMobil', 'LyondellBasell']

for i, (ticker, color, label) in enumerate(zip(tickers, colors, labels)):
    ax = axes[i]
    ax.plot(market.index, market[ticker].values, color=color, linewidth=2)

    for j, (date_str, label_text, evt_color) in enumerate(events):
        date = pd.to_datetime(date_str)
        ax.axvline(x=date, color=evt_color, linestyle='--', alpha=0.8, linewidth=1.5)
        
        if i == 0:
            y_min = market[ticker].min()
            y_max = market[ticker].max()
            y_range = y_max - y_min
            # 레이블 높이 엇갈리게
            y_pos = y_max - (j % 3) * y_range * 0.12
            ax.text(date, y_pos, label_text, fontsize=7.5, color=evt_color,
                   ha='center', va='top',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    ax.set_ylabel(f'{label}\n(USD)', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f8f8')

axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45)

orange_patch = mpatches.Patch(color='orange', label='Warning/Threat')
red_patch = mpatches.Patch(color='red', label='Military Action')
blue_patch = mpatches.Patch(color='blue', label='War Progress')
fig.legend(handles=[orange_patch, red_patch, blue_patch], 
          loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('data/market_impact.png', dpi=150, bbox_inches='tight')
print("저장 완료!")
