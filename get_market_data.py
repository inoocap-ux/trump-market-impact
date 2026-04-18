import pandas as pd
import yfinance as yf

start = '2025-01-20'
end = '2026-04-18'

tickers = {
    'WTI': 'CL=F',
    'DOW': 'DOW',
    'XOM': 'XOM',
    'LYB': 'LYB'
}

print("시장 데이터 수집 중...")
all_data = {}

for name, ticker in tickers.items():
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if len(df) > 0:
        # 멀티인덱스 대응
        if isinstance(df.columns, pd.MultiIndex):
            all_data[name] = df['Close'][ticker]
        else:
            all_data[name] = df['Close']
        print(f"{name}: {len(df)}개 수집 완료")
    else:
        print(f"{name}: 수집 실패")

market_df = pd.concat(all_data, axis=1)
market_df.columns = list(tickers.keys())
market_df.index = pd.to_datetime(market_df.index)
market_df = market_df.dropna(how='all')

print(f"\n날짜 범위: {market_df.index.min()} ~ {market_df.index.max()}")
print(f"총 {len(market_df)}일치 데이터")
print(market_df.tail(3))

market_df.to_csv('data/market_data.csv')
print("\n저장 완료!")
