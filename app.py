import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Trump War Statements vs Market Impact",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_data():
    market = pd.read_csv('data/market_data.csv', index_col=0, parse_dates=True)
    market.index = pd.to_datetime(market.index).tz_localize(None)
    tweets = pd.read_csv('data/war_tweets_filtered.csv')
    tweets['date_only'] = pd.to_datetime(tweets['date_only'])
    results = pd.read_csv('data/analysis_result.csv')
    results['date'] = pd.to_datetime(results['date'])
    case_df = pd.read_csv('data/case_analysis.csv')
    case_df['date'] = pd.to_datetime(case_df['date'])
    return market, tweets, results, case_df

market, tweets, results, case_df = load_data()

events = [
    ('2026-01-08', 'Locked & Loaded', 'orange'),
    ('2026-02-24', 'Nuclear Warning', 'orange'),
    ('2026-02-28', 'Operation Epic Fury', 'red'),
    ('2026-03-09', 'Navy Sunk', 'blue'),
    ('2026-03-13', 'Hormuz Mines', 'orange'),
    ('2026-04-07', 'Civilisation Will Die', 'red'),
]

st.title("🛢️ Trump War Statements vs Market Impact")
st.markdown("**이란 전쟁 관련 트럼프 발언이 유가 및 화학기업 주가에 미친 영향 분석**")
st.markdown("---")

st.sidebar.title("⚙️ 설정")
start_date = st.sidebar.date_input("시작일", value=pd.Timestamp('2025-02-01'))
end_date = st.sidebar.date_input("종료일", value=pd.Timestamp('2026-04-17'))
selected_tickers = st.sidebar.multiselect(
    "종목 선택",
    ['WTI', 'DOW', 'XOM', 'LYB'],
    default=['WTI', 'XOM', 'LYB']
)
show_events = st.sidebar.checkbox("이벤트 표시", value=True)

market_filtered = market[
    (market.index >= pd.Timestamp(start_date)) &
    (market.index <= pd.Timestamp(end_date))
]

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 시장 반응 차트",
    "📊 통계 분석",
    "⚔️ 전쟁유형 비교",
    "📋 발언 데이터"
])

with tab1:
    fig = make_subplots(
        rows=len(selected_tickers), cols=1,
        shared_xaxes=True,
        subplot_titles=selected_tickers,
        vertical_spacing=0.05
    )
    colors = {'WTI': 'black', 'DOW': 'steelblue', 'XOM': 'darkorange', 'LYB': 'green'}

    for i, ticker in enumerate(selected_tickers):
        fig.add_trace(
            go.Scatter(
                x=market_filtered.index,
                y=market_filtered[ticker],
                name=ticker,
                line=dict(color=colors[ticker], width=2),
                showlegend=True
            ),
            row=i+1, col=1
        )

    if show_events:
        for date_str, label, color in events:
            date = pd.Timestamp(date_str)
            if pd.Timestamp(start_date) <= date <= pd.Timestamp(end_date):
                for i in range(len(selected_tickers)):
                    fig.add_vline(
                        x=date, line_dash="dash",
                        line_color=color, opacity=0.7,
                        row=i+1, col=1
                    )
        # 범례용 더미 trace
        for date_str, label, color in events:
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='lines',
                line=dict(color=color, dash='dash', width=2),
                name=label,
                showlegend=True
            ))

    fig.update_layout(
        height=300 * len(selected_tickers),
        title_text="Trump 발언 전후 시장 반응",
        showlegend=True,
        hovermode='x unified',
        legend=dict(
            orientation='v',
            x=1.02,
            y=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray',
            borderwidth=1
        )
    )
    st.plotly_chart(fig, width='stretch')

with tab2:
    st.subheader("📊 이벤트 단계별 평균 변동률")
    results_2026 = results[results['date'] >= '2026-01-01'].copy()

    def get_phase(date):
        if date < pd.Timestamp('2026-02-28'):
            return '① 경고단계'
        elif date <= pd.Timestamp('2026-03-31'):
            return '② 전쟁발발'
        else:
            return '③ 호르무즈위기'

    results_2026['phase'] = results_2026['date'].apply(get_phase)
    phase_stats = results_2026.groupby(['phase', 'ticker'])['change_pct'].mean().unstack()
    st.dataframe(phase_stats.style.format("{:.2f}%").background_gradient(cmap='RdYlGn', axis=None))

    st.subheader("🔗 WTI vs 화학주 상관관계 (2026년)")
    market_2026 = market[market.index >= '2026-01-01']
    col1, col2, col3 = st.columns(3)
    col1.metric("WTI vs DOW", f"{market_2026['WTI'].corr(market_2026['DOW']):.3f}")
    col2.metric("WTI vs XOM", f"{market_2026['WTI'].corr(market_2026['XOM']):.3f}")
    col3.metric("WTI vs LYB", f"{market_2026['WTI'].corr(market_2026['LYB']):.3f}")

    st.subheader("💥 최대 충격 이벤트 TOP5 (WTI 기준)")
    wti_results = results_2026[results_2026['ticker'] == 'WTI'].copy()
    wti_results['abs_change'] = wti_results['change_pct'].abs()
    top5 = wti_results.nlargest(5, 'abs_change')[['date', 'change_pct', 'price_day0', 'price_day1']]
    top5.columns = ['날짜', '변동률(%)', '발언일 종가', '익일 종가']
    st.dataframe(top5.style.format({
        '변동률(%)': '{:.2f}%',
        '발언일 종가': '${:.2f}',
        '익일 종가': '${:.2f}'
    }))

with tab3:
    st.subheader("⚔️ 전쟁 유형별 시장 반응 비교")
    wti_case = case_df[case_df['ticker'] == 'WTI']
    stats = wti_case.groupby('case')['change_pct'].agg(['mean', 'max', 'min', 'count']).round(2)
    stats.columns = ['평균변동률(%)', '최대상승(%)', '최대하락(%)', '발언수']
    stats = stats[stats.index.isin(['Iran', 'Gaza/Israel', 'Ukraine/Russia'])]
    st.dataframe(stats.style.format({
        '평균변동률(%)': '{:+.2f}%',
        '최대상승(%)': '{:+.2f}%',
        '최대하락(%)': '{:+.2f}%',
    }).background_gradient(cmap='RdYlGn', subset=['평균변동률(%)']))

    fig2 = go.Figure()
    colors2 = {'Iran': 'red', 'Gaza/Israel': 'orange', 'Ukraine/Russia': 'blue'}
    for case in ['Iran', 'Gaza/Israel', 'Ukraine/Russia']:
        data = wti_case[wti_case['case'] == case]['change_pct']
        fig2.add_trace(go.Box(
            y=data,
            name=case,
            marker_color=colors2[case],
            boxpoints='all',
            jitter=0.3
        ))
    fig2.update_layout(
        title='WTI 익일 변동률 분포 (전쟁 유형별)',
        yaxis_title='익일 변동률 (%)',
        height=500
    )
    st.plotly_chart(fig2, width='stretch')

    st.subheader("💡 인사이트")
    st.info("🇷🇺 Ukraine/Russia 발언: 유일하게 평균 플러스. 유럽 에너지 공급 불안 반영.")
    st.warning("🇮🇱 Gaza/Israel 발언: 소폭 하락. 직접적 산유국 리스크 아니라 영향 제한적.")
    st.error("🇮🇷 Iran 발언: 평균 하락 + 최대 -16.41% 극단 변동. 호르무즈 봉쇄 리스크 반영.")

with tab4:
    st.subheader("📋 전쟁 관련 발언 데이터")
    case_filter = st.selectbox("케이스 필터", ['전체', 'Iran', 'Gaza/Israel', 'Ukraine/Russia'])
    search = st.text_input("키워드 검색", placeholder="Iran, nuclear, Hormuz ...")
    tweets_filtered = tweets.copy()
    if case_filter != '전체':
        tweets_filtered = tweets_filtered[tweets_filtered['case'] == case_filter]
    if search:
        tweets_filtered = tweets_filtered[tweets_filtered['text'].str.contains(search, case=False, na=False)]
    tweets_filtered = tweets_filtered.sort_values('date_only', ascending=False)
    st.write(f"총 {len(tweets_filtered)}개 발언")
    for _, row in tweets_filtered.iterrows():
        with st.expander(f"📅 {row['date_only']} [{row.get('case', '')}] — {str(row['text'])[:80]}..."):
            st.write(row['text'])

st.markdown("---")
st.markdown("**데이터 출처:** Kaggle Trump Tweets Dataset, Yahoo Finance | **분석:** 화학 원자재 가격 변동 조기경보 프로젝트")