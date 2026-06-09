import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="Global Top 10 Stocks Dashboard", layout="wide")

st.title("📈 글로벌 시가총액 Top 10 주식 대시보드")
st.markdown("Yahoo Finance 데이터를 활용하여 최근 1년간 글로벌 시가총액 상위 10개 종목의 주가 및 수익률 변화를 시각화합니다.")

# 글로벌 시가총액 Top 10 티커 (대표 종목)
TOP_10_TICKERS = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'NVDA': 'NVIDIA',
    'GOOGL': 'Alphabet',
    'AMZN': 'Amazon',
    'META': 'Meta',
    'TSM': 'TSMC',
    'BRK-B': 'Berkshire Hathaway',
    'LLY': 'Eli Lilly',
    'AVGO': 'Broadcom'
}

@st.cache_data(ttl=86400) # 하루(86400초) 동안 데이터 캐싱
def load_data():
    tickers = list(TOP_10_TICKERS.keys())
    # 최근 1년(1y) 데이터 다운로드
    df = yf.download(tickers, period="1y")
    return df['Close'] # 종가(Close) 데이터만 추출

try:
    with st.spinner('데이터를 불러오는 중입니다...'):
        close_data = load_data()
    
    st.success("데이터 로드 완료!")

    # 탭 구성으로 깔끔하게 배치
    tab1, tab2, tab3 = st.tabs(["📊 1년 누적 수익률 비교", "💵 주가(Price) 추이", "📋 원본 데이터(Raw Data)"])

    with tab1:
        st.subheader("Top 10 종목 최근 1년 누적 수익률 (%)")
        st.markdown("1년 전 첫 거래일의 주가를 0%로 기준 잡고 변화율을 보여줍니다.")
        
        # 수익률 계산: (현재가 / 1년 전 가격 - 1) * 100
        normalized_data = (close_data / close_data.iloc[0] - 1) * 100
        
        # [수정 사항] 
        # 1. hover_data 인자를 제거하여 Index 참조 에러를 해결했습니다.
        # 2. Wide-form 데이터 구조에 맞춰 범례 라벨 키를 'variable'로 수정했습니다.
        fig_norm = px.line(normalized_data, 
                           labels={'value': '수익률 (%)', 'Date': '날짜', 'variable': '종목'})
        
        # 3. 인덱스인 날짜 포맷은 아래와 같이 x축 속성 업데이트를 통해 설정합니다.
        fig_norm.update_xaxes(hoverformat="%Y-%m-%d")
        fig_norm.update_layout(hovermode="x unified")
        st.plotly_chart(fig_norm, use_container_width=True)

    with tab2:
        st.subheader("Top 10 종목 최근 1년 주가 변화 (USD)")
        
        fig_price = px.line(close_data, 
                            labels={'value': '주가 (USD)', 'Date': '날짜', 'variable': '종목'})
        fig_price.update_xaxes(hoverformat="%Y-%m-%d")
        fig_price.update_layout(hovermode="x unified")
        st.plotly_chart(fig_price, use_container_width=True)

    with tab3:
        st.subheader("최근 종가 데이터")
        # 최신 날짜가 위로 오도록 정렬하여 출력
        st.dataframe(close_data.sort_index(ascending=False).head(10))

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
