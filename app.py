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
    df_all = pd.read_csv('data/analysis_result.csv')
    df_all['date'] = pd.to_datetime(df_all['date'])
    case_df = pd.read_csv('data/case_analysis.csv')
    case_df['date'] = pd.to_datetime(case_df['date'])
    window_df = pd.read_csv('data/window_analysis.csv')
    intent_df = pd.read_csv('data/intent_analysis.csv')
    return market, tweets, df_all, case_df, window_df, intent_df

market, tweets, df_all, case_df, window_df, intent_df = load_data()

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
    st.subheader("📊 발언일 vs 비발언일 익일 변동률 비교")
    st.caption("※ 본 분석은 트럼프 전쟁 관련 발언이 있던 날과 없던 날의 익일 변동률을 비교한 것입니다.")

    compare_data = []
    for ticker in ['WTI', 'DOW', 'XOM', 'LYB']:
        sub = df_all[df_all['ticker'] == ticker]
        event = sub[sub['is_event'] == True]['change_pct']
        non_event = sub[sub['is_event'] == False]['change_pct']
        compare_data.append({
            '종목': ticker,
            '발언일 평균': f"{event.mean():+.2f}%",
            '발언일 상승비율': f"{(event>0).mean()*100:.1f}%",
            '비발언일 평균': f"{non_event.mean():+.2f}%",
            '비발언일 상승비율': f"{(non_event>0).mean()*100:.1f}%",
            '차이': f"{event.mean() - non_event.mean():+.2f}%"
        })
    compare_df = pd.DataFrame(compare_data)
    st.dataframe(compare_df, hide_index=True)
    st.warning("⚠️ 모든 종목에서 발언일 익일 변동률이 비발언일보다 낮게 나타납니다.")

    st.markdown("---")
    st.subheader("📅 주요 발언 전후 5일 WTI 누적 변동률")
    st.caption("※ 발언 5일 전 → 발언일, 발언일 → 발언 5일 후 WTI 누적 변동률")

    fig_window = go.Figure()
    fig_window.add_trace(go.Bar(
        x=window_df['event'],
        y=window_df['before_5d'],
        name='발언 5일 전→발언일',
        marker_color='steelblue'
    ))
    fig_window.add_trace(go.Bar(
        x=window_df['event'],
        y=window_df['after_5d'],
        name='발언일→발언 5일 후',
        marker_color='tomato'
    ))
    fig_window.update_layout(
        barmode='group',
        title='주요 발언 전후 5일 WTI 누적 변동률',
        yaxis_title='변동률 (%)',
        height=450
    )
    st.plotly_chart(fig_window, width='stretch')
    st.info("💡 전쟁 초반(1월-2월) 발언 후 상승 → 전쟁 후반(3월-4월) 발언 후 하락. 발언 영향력이 시간이 지날수록 약해지는 패턴.")
    st.markdown("---")
    st.subheader("🔍 스페셜 케이스 - 트럼프 유가 조절자 가설")
    st.caption("※ 샘플 수가 적어 통계적 유의성은 낮으나 흥미로운 패턴이 관찰됨")

    zone_stats = intent_df.groupby('wti_zone')['wti_next_change'].agg(['mean', 'count']).reset_index()
    zone_stats.columns = ['WTI 구간', '익일 평균 변동률(%)', '발언 수']
    zone_stats['익일 평균 변동률(%)'] = zone_stats['익일 평균 변동률(%)'].round(2)
    zone_order = ['저유가(~65)', '중유가(65~80)', '고유가(80~95)', '초고유가(95~)']
    zone_stats['WTI 구간'] = pd.Categorical(zone_stats['WTI 구간'], categories=zone_order, ordered=True)
    zone_stats = zone_stats.sort_values('WTI 구간')
    st.dataframe(zone_stats, hide_index=True)
    st.warning("⚠️ 샘플 수가 적어 통계적 유의성은 낮으나 흥미로운 두 단계 패턴이 관찰됨.")
    st.markdown("""
**1단계 (전쟁 초반):** 강경 발언 → 유가 상승  
→ 전쟁 명분 쌓기, 시장에 긴장감 주입

**2단계 (전쟁 후반):** 유화/종전 발언 → 유가 하락  
→ 유가 급등으로 인한 민심 불안 완화 목적  
→ 실제로 트럼프는 4월 발언에서 "기름값 좀 더 내도 된다"고 직접 언급

**결론:** 트럼프가 전쟁 국면에 따라 발언 강도를 조절하며 유가에 영향을 미쳤을 가능성이 있음.  
단, 인과관계 단정은 어려우며 유가 불안 시 발언이 많아지는 역인과 가능성도 존재.
    """)
    
    st.markdown("---")
    st.subheader("🔗 WTI vs 화학주 상관관계 (2026년)")
    market_2026 = market[market.index >= '2026-01-01']
    col1, col2, col3 = st.columns(3)
    col1.metric("WTI vs DOW", f"{market_2026['WTI'].corr(market_2026['DOW']):.3f}")
    col2.metric("WTI vs XOM", f"{market_2026['WTI'].corr(market_2026['XOM']):.3f}")
    col3.metric("WTI vs LYB", f"{market_2026['WTI'].corr(market_2026['LYB']):.3f}")

    st.markdown("---")
    st.subheader("💥 최대 충격 이벤트 TOP5 (WTI 기준 발언일 익일 변동률)")
    wti_results = df_all[(df_all['ticker'] == 'WTI') & (df_all['is_event'] == True)].copy()
    wti_results['abs_change'] = wti_results['change_pct'].abs()
    top5 = wti_results.nlargest(5, 'abs_change')[['date', 'change_pct']].copy()
    
    # 발언일/익일 종가 다시 계산
    prices = []
    for _, row in top5.iterrows():
        date = pd.Timestamp(row['date'])
        if date in market.index:
            future = market.index[market.index > date]
            price_day0 = market.loc[date, 'WTI']
            price_day1 = market.loc[future[0], 'WTI'] if len(future) > 0 else None
        else:
            price_day0, price_day1 = None, None
        prices.append({'발언일 종가': price_day0, '익일 종가': price_day1})
    
    prices_df = pd.DataFrame(prices)
    top5 = top5.reset_index(drop=True)
    top5 = pd.concat([top5, prices_df], axis=1)
    top5.columns = ['날짜', '익일 변동률(%)', '발언일 종가', '익일 종가']
    st.dataframe(top5.style.format({
        '익일 변동률(%)': '{:.2f}%',
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