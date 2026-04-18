# Trump War Statements vs Market Impact

> 트럼프 전쟁 관련 발언이 유가(WTI) 및 미국 화학기업 주가에 미치는 영향을 분석한 데이터 분석 포트폴리오 프로젝트

## 프로젝트 개요

트럼프 2기 집권(2025.01~) 이후 이란, 가자, 우크라이나 관련 발언을 수집하고, 발언 익일 WTI 원유 및 화학기업 주가 변동률을 분석했습니다.
화공공정 전공 배경을 바탕으로 **"트럼프 발언 → 유가 → 화학 원자재 원가"** 연쇄 영향을 데이터로 검증했습니다.

---

## 주요 분석 결과

### 이벤트 단계별 WTI 평균 변동률

| 단계 | 기간 | WTI 평균 변동률 |
|---|---|---|
| ① 경고단계 | ~2026-02-27 | +0.84% |
| ② 전쟁발발 | 2026-02-28 ~ 03-31 | -4.18% |
| ③ 호르무즈위기 | 2026-04~ | -16.41% |

### 전쟁 유형별 WTI 반응

| 케이스 | 발언수 | 평균 변동률 | 최대 하락 |
|---|---|---|---|
| Iran | 69 | -0.44% | -16.41% |
| Gaza/Israel | 37 | -0.27% | -6.04% |
| Ukraine/Russia | 16 | +0.24% | -8.57% |

### WTI vs 화학주 상관관계 (2026년)

| 종목 | 상관계수 |
|---|---|
| WTI vs LYB (LyondellBasell) | 0.966 |
| WTI vs DOW (Dow Chemical) | 0.934 |
| WTI vs XOM (ExxonMobil) | 0.793 |

---

## 핵심 인사이트

- 경고 발언은 유가를 소폭 끌어올리는 반면, 실제 공습 이후 전쟁이 길어지면 오히려 유가가 하락하는 역설적 패턴 발견
- 이란 발언은 평균적으로 하락이지만 변동성이 극단적 (호르무즈 해협 봉쇄 리스크)
- 우크라이나 발언만 유일하게 평균 플러스 (유럽 에너지 공급 불안 반영)
- LYB 상관계수 0.966 : 나프타/에틸렌 직결 종목이라 WTI와 거의 완벽하게 동조화

---

## 데이터 소스

| 데이터 | 출처 | 기간 |
|---|---|---|
| 트럼프 발언 | Kaggle - Trump Tweets 2009-2025 | 2025.01 ~ 2025.12 |
| 트럼프 발언 (2026) | 뉴스 기반 수동 수집 | 2026.01 ~ 2026.04 |
| WTI / DOW / XOM / LYB | Yahoo Finance (yfinance) | 2025.01 ~ 2026.04 |

---

```
## 파일 구조

trump_market_impact/
├── app.py                      # Streamlit 대시보드 메인
├── get_market_data.py          # 주가/유가 데이터 수집
├── filter4.py                  # 전쟁 관련 발언 필터링
├── add_2026.py                 # 2026년 발언 수동 추가
├── classify.py                 # 발언 케이스 분류 (Iran/Gaza/Ukraine)
├── analyze.py                  # 이벤트 전후 변동률 분석
├── compare_cases.py            # 전쟁 유형별 비교 분석
├── stats.py                    # 통계 분석
├── visualize.py                # matplotlib 시각화
└── data/
    ├── djt_posts_dec2025.csv       # 트럼프 발언 원본
    ├── war_tweets_filtered.csv     # 필터링된 전쟁 발언
    ├── market_data.csv             # 주가/유가 데이터
    ├── analysis_result.csv         # 이벤트 분석 결과
    └── case_analysis.csv           # 케이스별 분석 결과
```
---

## 주요 파일 역할

**filter4.py**
전체 6,349개 발언에서 전쟁 관련 키워드 필터링 → 159개 추출

**add_2026.py**
Kaggle 데이터셋이 2025년 12월까지만 있어 2026년 이란 전쟁 관련 발언 16개를 뉴스 기반으로 수동 추가

**classify.py**
키워드 스코어링 방식으로 발언을 Iran / Gaza/Israel / Ukraine/Russia 3개 케이스로 자동 분류

**analyze.py**
발언 날짜 기준 당일 종가 → 익일 종가 변동률 계산, 이벤트별 시장 반응 수치화

**app.py**
Streamlit 4탭 대시보드
- 📈 시장 반응 차트 (Plotly 인터랙티브)
- 📊 통계 분석 (단계별 변동률, 상관관계, TOP5)
- ⚔️ 전쟁유형 비교 (박스플롯)
- 📋 발언 데이터 (케이스 필터 + 키워드 검색)

---

## 실행 방법

```bash
python3 -m venv venv
source venv/bin/activate
pip install streamlit pandas plotly yfinance matplotlib
streamlit run app.py
```

---

## 기술 스택

Python / Pandas / yfinance / Plotly / Streamlit / Matplotlib

---

## 트러블슈팅

### 1. python 명령어 인식 안 됨 (WSL)
```bash
# 틀림
python -m venv venv
# 맞음
python3 -m venv venv
```

### 2. VS Code 터미널이 홈 디렉토리에서 열림
```bash
cd trump_market_impact
source venv/bin/activate
```

### 3. cat EOF 실패 시 파일 생성 안 됨
오류 발생 시 파일이 빈 채로 생성되거나 아예 생성되지 않음.
실행 전 반드시 `cat 파일명.py` 로 내용 확인 필요.

Claude 한계 : Claude는 터미널 실행 환경의 상태를 실시간으로 알 수 없음.
파일 생성 실패 후 python 실행해도 결과 없음의 인과관계를 파악하지 못함.
Claude 말대로 했는데 안 되면 Claude에게 묻기 전에 환경 상태를 직접 확인할 것.

### 4. venv가 git에 포함됨
```bash
echo "venv/" > .gitignore
git rm -r --cached venv/
git add .
git commit -m "remove venv"
```

### 5. yfinance 버전 변경으로 Close 컬럼 추출 방식 변경
```python
if isinstance(df.columns, pd.MultiIndex):
    all_data[name] = df['Close'][ticker]
else:
    all_data[name] = df['Close']
```

---

## 개발 환경

- OS : WSL Ubuntu 24 (Windows)
- Editor : VS Code
- Python : 3.12
- 가상환경 : venv

---

*화공공정 전공 + SK네트웍스 AI 부트캠프 데이터 관리 역량 강화 과정 개인 포트폴리오 프로젝트*
