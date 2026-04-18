import pandas as pd

df = pd.read_csv('data/djt_posts_dec2025.csv')
df['date'] = pd.to_datetime(df['date'], utc=True)
df['date_only'] = df['date'].dt.date
df = df[df['date'] >= '2025-01-20']

# 진짜 전쟁 직접 관련만
keywords = ['Iran', 'Gaza', 'Hamas', 'ceasefire', 
            'missile', 'nuclear', 'airstrike', 'Houthi',
            'Ukraine war', 'peace deal', 'troops to']

pattern = '|'.join(keywords)
war_df = df[df['text'].str.contains(pattern, case=False, na=False)]
war_df = war_df[['date_only', 'text']].sort_values('date_only')

print(f"전쟁 관련 발언 수: {len(war_df)}")

# 샘플 5개 출력
for _, row in war_df.head(5).iterrows():
    print(f"\n날짜: {row['date_only']}")
    print(f"내용: {row['text'][:150]}...")

war_df.to_csv('data/war_tweets_filtered.csv', index=False)
print("\n저장 완료!")
