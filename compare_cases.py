import pandas as pd
import numpy as np

tweets = pd.read_csv('data/war_tweets_filtered.csv')
tweets['date_only'] = pd.to_datetime(tweets['date_only'])
market = pd.read_csv('data/market_data.csv', index_col=0, parse_dates=True)
market.index = pd.to_datetime(market.index).tz_localize(None)

results = []
for _, row in tweets.iterrows():
    date = row['date_only']
    case = row['case']
    for ticker in ['WTI', 'DOW', 'XOM', 'LYB']:
        try:
            if date in market.index:
                price_day0 = market.loc[date, ticker]
            else:
                continue
            future = market.index[market.index > date]
            if len(future) == 0:
                continue
            price_day1 = market.loc[future[0], ticker]
            change = (price_day1 - price_day0) / price_day0 * 100
            results.append({
                'date': date,
                'case': case,
                'ticker': ticker,
                'change_pct': round(change, 2)
            })
        except:
            continue

df = pd.DataFrame(results)

print("=" * 60)
print("케이스별 익일 평균 변동률")
print("=" * 60)
pivot = df.groupby(['case', 'ticker'])['change_pct'].mean().unstack()
print(pivot.round(2).to_string())

print("\n" + "=" * 60)
print("WTI 기준 케이스별 상세")
print("=" * 60)
wti = df[df['ticker'] == 'WTI']
for case in ['Iran', 'Gaza/Israel', 'Ukraine/Russia']:
    sub = wti[wti['case'] == case]
    print(f"\n[{case}] n={len(sub)}")
    print(f"  평균: {sub['change_pct'].mean():+.2f}%")
    print(f"  최대 상승: {sub['change_pct'].max():+.2f}%")
    print(f"  최대 하락: {sub['change_pct'].min():+.2f}%")
    print(f"  상승 비율: {(sub['change_pct'] > 0).mean()*100:.1f}%")

df.to_csv('data/case_analysis.csv', index=False)
print("\n저장 완료!")
