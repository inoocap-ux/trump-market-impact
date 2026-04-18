import pandas as pd

df = pd.read_csv('data/war_tweets_filtered.csv')

def classify_case(text):
    text_lower = text.lower()
    
    iran = ['iran', 'nuclear', 'hormuz', 'tehran', 'persian', 'irgc', 'khamenei', 'epic fury', 'midnight hammer']
    gaza = ['gaza', 'hamas', 'hostage', 'israel', 'ceasefire', 'palestin', 'netanyahu', 'houthi']
    ukraine = ['ukraine', 'russia', 'putin', 'zelensky', 'nato', 'moscow', 'kyiv']
    
    iran_score = sum(1 for k in iran if k in text_lower)
    gaza_score = sum(1 for k in gaza if k in text_lower)
    ukraine_score = sum(1 for k in ukraine if k in text_lower)
    
    if iran_score == 0 and gaza_score == 0 and ukraine_score == 0:
        return 'other'
    
    scores = {'Iran': iran_score, 'Gaza/Israel': gaza_score, 'Ukraine/Russia': ukraine_score}
    return max(scores, key=scores.get)

df['case'] = df['text'].apply(classify_case)

print(df['case'].value_counts())
print("\n샘플 확인:")
for case in ['Iran', 'Gaza/Israel', 'Ukraine/Russia']:
    sample = df[df['case'] == case].head(2)
    for _, row in sample.iterrows():
        print(f"\n[{case}] {row['date_only']}")
        print(f"{str(row['text'])[:100]}...")

df.to_csv('data/war_tweets_filtered.csv', index=False)
print("\n저장 완료!")
