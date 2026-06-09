import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="기하: 이차곡선 탐구 교실", layout="wide")

# 2. 데이터 로딩 함수 (NASA API)
@st.cache_data
def fetch_neo_data():
    url = "https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY"
    try:
        response = requests.get(url)
        data = response.json()
        neos = data.get('near_earth_objects', [])
        extracted_data = []
        for neo in neos:
            orbital = neo.get('orbital_data', {})
            name = neo.get('name', 'Unknown')
            e = float(orbital.get('eccentricity', 0))
            a = float(orbital.get('semi_major_axis', 0))
            if a > 0:
                extracted_data.append({'Name': name, 'e': e, 'a': a})
        df = pd.DataFrame(extracted_data)
        # 교육용 데이터 추가
        df.loc[len(df)] = {'Name': 'Oumuamua (쌍곡선 궤도)', 'e': 1.1995, 'a': 1.29}
        return df
    except:
        return pd.DataFrame()

# 3. 메인 UI 및 모드 전환
st.title("🌌 기하: 이차곡선 방정식과 궤도 모델링")
st.sidebar.header("수업 활동 선택")
mode = st.sidebar.radio("활동 모드:", ["1. 이차곡선 생성 원리 탐구 (사전 활동)", "2. NASA 데이터 방정식 모델링"])

# --- 모드 1: 사전 활동 (슬라이더 탐구) ---
if mode == "1. 이차곡선 생성 원리 탐구 (사전 활동)":
    st.subheader("🛠️ 이차곡선 생성 원리 탐구")
    col1, col2 = st.columns([1, 2])
    with col1:
        a_val = st.slider("장축의 반 (a)", 1.0, 5.0, 2.0, 0.1)
        e_val = st.slider("이심률 (e)", 0.0, 2.0, 0.5, 0.05)
        c = a_val * e_val
        
        if e_val < 1:
            b = np.sqrt(max(0, a_val**2 - c**2))
            st.latex(rf"\text{{타원: }} \frac{{x^2}}{{{a_val**2:.2f}}} + \frac{{y^2}}{{{b**2:.2f}}} = 1")
        else:
            b = np.sqrt(max(0, c**2 - a_val**2))
            st.latex(rf"\text{{쌍곡선: }} \frac{{x^2}}{{{a_val**2:.2f}}} - \frac{{y^2}}{{{b**2:.2f}}} = 1")

    with col2:
        fig = go.Figure()
        if e_val < 1:
            t = np.linspace(0, 2*np.pi, 200)
            fig.add_trace(go.Scatter(x=a_val*np.cos(t), y=b*np.sin(t), mode='lines', name='타원'))
        else:
            t = np.linspace(-2, 2, 200)
            fig.add_trace(go.Scatter(x=a_val*np.cosh(t), y=b*np.sinh(t), mode='lines', name='쌍곡선'))
            fig.add_trace(go.Scatter(x=-a_val*np.cosh(t), y=b*np.sinh(t), mode='lines', name='쌍곡선'))
        fig.update_layout(xaxis=dict(range=[-7, 7]), yaxis=dict(range=[-5, 5], scaleanchor="x"))
        st.plotly_chart(fig, use_container_width=True)

# --- 모드 2: 데이터 모델링 (NASA 실데이터) ---
else:
    df = fetch_neo_data()
    curve_type = st.sidebar.radio("탐색할 곡선:", ["타원 (0 < e < 1)", "쌍곡선 (e > 1)"])
    filtered_df = df[(df['e'] > 0) & (df['e'] < 1)] if "타원" in curve_type else df[df['e'] > 1]
    
    if not filtered_df.empty:
        selected_neo = st.sidebar.selectbox("분석할 데이터 선택:", filtered_df['Name'])
        neo = filtered_df[filtered_df['Name'] == selected_neo].iloc[0]
        e, a = neo['e'], neo['a']
        c = a * e
        
        st.subheader(f"📊 {selected_neo} 분석")
        col1, col2 = st.columns([1, 1.2])
        with col1:
            if e < 1:
                b = np.sqrt(max(0, a**2 - c**2))
                st.latex(rf"\frac{{x^2}}{{{a**2:.4f}}} + \frac{{y^2}}{{{b**2:.4f}}} = 1")
            else:
                b = np.sqrt(max(0, c**2 - a**2))
                st.latex(rf"\frac{{x^2}}{{{a**2:.4f}}} - \frac{{y^2}}{{{b**2:.4f}}} = 1")
        with col2:
            st.info("데이터 기반 시각화는 위의 사전 활동 로직과 동일하게 연결됩니다.")

# --- 공통 질문 ---
st.markdown("---")
st.subheader("📝 기하 탐구 질문")
st.markdown("""
1. 타원 위의 점 $P(x, y)$에서 두 초점까지의 거리의 합이 $2a$로 일정함을 수식으로 증명해 보자.
2. 쌍곡선의 점근선 $y = \pm \frac{b}{a}x$와 천체의 미래 궤적 예측의 관계를 극한을 이용해 설명해 보자.
""")
