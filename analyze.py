import pandas as pd
import numpy as np

# 데이터 로드
tweets = pd.read_csv('data/war_tweets_filtered.csv')
market = pd.read_csv('data/market_data.csv', index_col=0, parse_dates=True)
market.index = pd.to_datetime(market.index).tz_localize(None)

# 발언 날짜 중복 제거 (같은 날 여러 발언은 하나로)
tweets['date_only'] = pd.to_datetime(tweets['date_only'])
event_dates = tweets['date_only'].drop_duplicates().sort_values()

print(f"분석할 이벤트 날짜: {len(event_dates)}개")

results = []
for date in event_dates:
    for col in ['WTI', 'DOW', 'XOM', 'LYB']:
        try:
            # 발언 당일 종가
            if date in market.index:
                price_day0 = market.loc[date, col]
            else:
                continue

            # 익일 종가
            future_dates = market.index[market.index > date]
            if len(future_dates) == 0:
                continue
            price_day1 = market.loc[future_dates[0], col]

            # 변동률
            change = (price_day1 - price_day0) / price_day0 * 100

            results.append({
                'date': date,
                'ticker': col,
                'price_day0': round(price_day0, 2),
                'price_day1': round(price_day1, 2),
                'change_pct': round(change, 2)
            })
        except:
            continue

result_df = pd.DataFrame(results)
print(result_df.head(20).to_string())

result_df.to_csv('data/analysis_result.csv', index=False)
print("\n저장 완료!")
