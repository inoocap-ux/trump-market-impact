import pandas as pd
import numpy as np

market = pd.read_csv('data/market_data.csv', index_col=0, parse_dates=True)
market.index = pd.to_datetime(market.index).tz_localize(None)

tweets = pd.read_csv('data/war_tweets_filtered.csv')
tweets['date_only'] = pd.to_datetime(tweets['date_only'])
event_dates = set(tweets['date_only'].dt.date)

# ============================================================
# 1번 - 발언일 vs 비발언일
# ============================================================
results = []
for i in range(len(market) - 1):
    date = market.index[i]
    is_event = date.date() in event_dates
    for ticker in ['WTI', 'DOW', 'XOM', 'LYB']:
        price_day0 = market.iloc[i][ticker]
        price_day1 = market.iloc[i + 1][ticker]
        change = (price_day1 - price_day0) / price_day0 * 100
        results.append({
            'date': date,
            'ticker': ticker,
            'change_pct': round(change, 2),
            'is_event': is_event
        })

df = pd.DataFrame(results)
df.to_csv('data/analysis_result.csv', index=False)

# ============================================================
# 2번 - 발언 전후 5일 누적 변동률 (주요 이벤트만)
# ============================================================
key_events = [
    ('2026-01-08', 'Locked & Loaded'),
    ('2026-02-24', 'Nuclear Warning'),
    ('2026-02-28', 'Operation Epic Fury'),
    ('2026-03-09', 'Navy Sunk'),
    ('2026-04-07', 'Civilisation Will Die'),
]

print("=" * 60)
print("2번 - 주요 발언 전후 5일 WTI 누적 변동률")
print("=" * 60)

window_results = []
for date_str, label in key_events:
    base_date = pd.Timestamp(date_str)
    future_dates = market.index[market.index >= base_date]
    past_dates = market.index[market.index < base_date]

    if len(future_dates) < 6 or len(past_dates) < 5:
        continue

    price_base = market.loc[future_dates[0], 'WTI']
    price_minus5 = market.loc[past_dates[-5], 'WTI']
    price_plus5 = market.loc[future_dates[5], 'WTI']

    before = (price_base - price_minus5) / price_minus5 * 100
    after = (price_plus5 - price_base) / price_base * 100

    print(f"\n[{label}] {date_str}")
    print(f"  발언 5일 전 → 발언일: {before:+.2f}%")
    print(f"  발언일 → 발언 5일 후: {after:+.2f}%")

    window_results.append({
        'event': label,
        'date': date_str,
        'before_5d': round(before, 2),
        'after_5d': round(after, 2)
    })

window_df = pd.DataFrame(window_results)
window_df.to_csv('data/window_analysis.csv', index=False)

# ============================================================
# 3번 - 발언 의도 분석 (발언 직전 WTI 수준 vs 익일 변동률)
# ============================================================
print("\n" + "=" * 60)
print("3번 - 발언 직전 WTI 수준 vs 익일 변동률 (의도 분석)")
print("=" * 60)

tweets_sorted = tweets.copy()
tweets_sorted['date_only'] = pd.to_datetime(tweets_sorted['date_only'])
tweets_sorted = tweets_sorted.drop_duplicates('date_only').sort_values('date_only')

intent_results = []
for _, row in tweets_sorted.iterrows():
    date = row['date_only']
    if date not in market.index:
        continue
    future = market.index[market.index > date]
    if len(future) == 0:
        continue

    wti_level = market.loc[date, 'WTI']
    wti_change = (market.loc[future[0], 'WTI'] - wti_level) / wti_level * 100

    intent_results.append({
        'date': date,
        'wti_level': round(wti_level, 2),
        'wti_next_change': round(wti_change, 2)
    })

intent_df = pd.DataFrame(intent_results)

# WTI 수준 구간 나누기
intent_df['wti_zone'] = pd.cut(
    intent_df['wti_level'],
    bins=[0, 65, 80, 95, 999],
    labels=['저유가(~65)', '중유가(65~80)', '고유가(80~95)', '초고유가(95~)']
)

print(intent_df.groupby('wti_zone')['wti_next_change'].agg(['mean', 'count']).round(2))
intent_df.to_csv('data/intent_analysis.csv', index=False)

print("\n저장 완료!")