import pandas as pd

df = pd.read_csv('data/djt_posts_dec2025.csv')
df['date'] = pd.to_datetime(df['date'], utc=True)
df['date_only'] = df['date'].dt.date
df = df[df['date'] >= '2025-01-20']

# 더 좁힌 키워드
keywords = ['Iran', 'Russia', 'Ukraine', 'Gaza', 
            'Israel', 'Hamas', 'ceasefire', 'missile',
            'nuclear', 'airstrike', 'Houthi', 'NATO']

pattern = '|'.join(keywords)
war_df = df[df['text'].str.contains(pattern, case=False, na=False)]
war_df = war_df[['date_only', 'text']].sort_values('date_only')

print(f"전쟁 관련 발언 수: {len(war_df)}")
print(war_df[['date_only', 'text']].to_string())

war_df.to_csv('data/war_tweets_filtered.csv', index=False)
print("\n저장 완료!")
