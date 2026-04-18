import pandas as pd
import numpy as np

# 데이터 로드
results = pd.read_csv('data/analysis_result.csv')
results['date'] = pd.to_datetime(results['date'])

# 2026년 이벤트만
results_2026 = results[results['date'] >= '2026-01-01']

print("=" * 60)
print("1. 전체 기간 평균 익일 변동률")
print("=" * 60)
for ticker in ['WTI', 'DOW', 'XOM', 'LYB']:
    df = results_2026[results_2026['ticker'] == ticker]
    print(f"{ticker}: 평균 {df['change_pct'].mean():.2f}% | "
          f"최대 상승 {df['change_pct'].max():.2f}% | "
          f"최대 하락 {df['change_pct'].min():.2f}%")

print("\n" + "=" * 60)
print("2. 이벤트 단계별 평균 변동률")
print("=" * 60)

# 단계 분류
def get_phase(date):
    if date < pd.Timestamp('2026-02-28'):
        return '1_경고단계'
    elif date <= pd.Timestamp('2026-03-01'):
        return '2_공습시작'
    elif date <= pd.Timestamp('2026-03-31'):
        return '3_전쟁진행'
    else:
        return '4_호르무즈위기'

results_2026 = results_2026.copy()
results_2026['phase'] = results_2026['date'].apply(get_phase)

for phase in sorted(results_2026['phase'].unique()):
    df = results_2026[results_2026['phase'] == phase]
    wti = df[df['ticker']=='WTI']['change_pct'].mean()
    xom = df[df['ticker']=='XOM']['change_pct'].mean()
    print(f"\n[{phase}]")
    print(f"  WTI: {wti:+.2f}%  XOM: {xom:+.2f}%")

print("\n" + "=" * 60)
print("3. 발언 후 가장 큰 충격을 준 TOP5 이벤트 (WTI 기준)")
print("=" * 60)
wti_results = results_2026[results_2026['ticker'] == 'WTI'].copy()
wti_results['abs_change'] = wti_results['change_pct'].abs()
top5 = wti_results.nlargest(5, 'abs_change')[['date', 'change_pct', 'price_day0', 'price_day1']]
print(top5.to_string(index=False))

print("\n" + "=" * 60)
print("4. WTI vs 화학주 상관관계 (2026년)")
print("=" * 60)
market = pd.read_csv('data/market_data.csv', index_col=0, parse_dates=True)
market.index = pd.to_datetime(market.index).tz_localize(None)
market_2026 = market[market.index >= '2026-01-01']
for ticker in ['DOW', 'XOM', 'LYB']:
    corr = market_2026['WTI'].corr(market_2026[ticker])
    print(f"WTI vs {ticker}: {corr:.3f}")

