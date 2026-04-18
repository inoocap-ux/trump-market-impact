import pandas as pd

data_2026 = [
    # 1월 - 위협/경고 단계
    {'date_only': '2026-01-08', 'text': 'The United States of America will come to their rescue. We are locked and loaded and ready to go. Iran must stop killing peaceful protesters NOW!', 'word_count': 30},
    {'date_only': '2026-01-15', 'text': 'TAKE OVER YOUR INSTITUTIONS. The United States is watching. HELP IS ON ITS WAY. The Iranian regime cannot survive.', 'word_count': 22},
    {'date_only': '2026-01-20', 'text': 'Iran cannot have a Nuclear Weapon. Maximum pressure campaign will continue. Iran must come to the table or face severe consequences.', 'word_count': 25},
    {'date_only': '2026-01-29', 'text': 'Signed Executive Order reaffirming national emergency with respect to Iran. Countries that purchase goods from Iran will face additional tariffs. Maximum pressure!', 'word_count': 28},

    # 2월 - 군사 집결/협상 결렬
    {'date_only': '2026-02-06', 'text': 'I want Iran to be a great Country, but one that cannot have a Nuclear Weapon. Deployed massive armada to the region. Come to the table or face stronger consequences.', 'word_count': 33},
    {'date_only': '2026-02-12', 'text': 'Regime change in Iran would be the best thing that could happen. The Iranian people deserve freedom. The regime is weak and getting weaker every day.', 'word_count': 30},
    {'date_only': '2026-02-24', 'text': 'Iran has restarted its nuclear program and is developing missiles capable of striking the United States of America. This will NEVER be allowed to happen!', 'word_count': 29},
    {'date_only': '2026-02-26', 'text': 'Negotiations with Iran have failed. They refuse to give up nuclear weapons. The United States has been more than patient. Iran is the worlds leading state sponsor of terrorism.', 'word_count': 32},

    # 2월 28일 - 공습 시작 (핵심 이벤트)
    {'date_only': '2026-02-28', 'text': 'A short time ago the United States military began major combat operations in Iran. Our objective is to defend the American people by eliminating imminent threats from the Iranian regime. For 47 years Iran has chanted Death to America.', 'word_count': 42},

    # 3월 - 전쟁 진행
    {'date_only': '2026-03-02', 'text': 'Operation Epic Fury is proceeding exactly as planned. Irans nuclear facilities have been destroyed. Supreme Leader eliminated. The world is safer today than it was yesterday.', 'word_count': 31},
    {'date_only': '2026-03-09', 'text': 'We are achieving major strides toward completing our military objective. Most of Irans naval power has been sunk. We continue to target Irans drone and missile capabilities.', 'word_count': 31},
    {'date_only': '2026-03-13', 'text': 'Iran must remove all mines from the Strait of Hormuz IMMEDIATELY. If mines are not removed forthwith the Military consequences to Iran will be at a level never seen before.', 'word_count': 33},
    {'date_only': '2026-03-22', 'text': 'We are very close to meeting our objectives as we consider winding down our great Military efforts in the Middle East. Irans military capabilities have been completely destroyed.', 'word_count': 32},

    # 4월 - 호르무즈 해협 위기
    {'date_only': '2026-04-05', 'text': 'Iran will pay a price like no country has ever paid before if they do not open the Strait of Hormuz. Our military is ready. Do not test the United States!', 'word_count': 34},
    {'date_only': '2026-04-07', 'text': 'If Iran doesnt FULLY OPEN the Strait of Hormuz within 48 HOURS the United States will hit and obliterate their various POWER PLANTS STARTING WITH THE BIGGEST ONE FIRST!', 'word_count': 33},
    {'date_only': '2026-04-07', 'text': 'A whole civilisation will die tonight never to be brought back again. I dont want that to happen but it probably will. Open the Strait NOW or face total destruction.', 'word_count': 34},
]

df_existing = pd.read_csv('data/war_tweets_filtered.csv')
df_2026 = pd.DataFrame(data_2026)
df_combined = pd.concat([df_existing, df_2026], ignore_index=True)
df_combined = df_combined.sort_values('date_only').reset_index(drop=True)

print(f"기존 데이터: {len(df_existing)}개")
print(f"추가 데이터: {len(df_2026)}개")
print(f"최종 합계: {len(df_combined)}개")
print(f"\n날짜 범위: {df_combined['date_only'].min()} ~ {df_combined['date_only'].max()}")

df_combined.to_csv('data/war_tweets_filtered.csv', index=False)
print("저장 완료!")
