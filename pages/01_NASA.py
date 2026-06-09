import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 페이지 레이아웃 설정
st.set_page_config(page_title="우주 기하학 실험실", layout="wide")

# --- 데이터 로딩 함수 ---
@st.cache_data
def get_nasa_data():
    """NASA NeoWs API에서 실제 소행성 데이터를 가져옵니다."""
    try:
        url = "https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY"
        res = requests.get(url).json()
        neos = res.get('near_earth_objects', [])
        data = []
        for n in neos:
            orb = n.get('orbital_data', {})
            data.append({
                '이름': n.get('name'),
                '이심률(e)': float(orb.get('eccentricity', 0)),
                '장반경(a)': float(orb.get('semi_major_axis', 0))
            })
        # 교육용 성간 천체 오무아무아 데이터 추가
        data.append({'이름': '1I/Oumuamua', '이심률(e)': 1.199, '장반경(a)': -1.27})
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

# --- 사이드바: 모드 선택 ---
st.sidebar.title("🔭 탐구 모드")
mode = st.sidebar.radio("원하는 활동을 선택하세요:", ["NASA 실데이터 분석", "가상 궤도 실험실 (이심률 조절)"])

# --- 메인 화면 시작 ---
st.title("🛰️ 기하: 이차곡선과 천체 궤도 탐구")
st.markdown("---")

if mode == "가상 궤도 실험실 (이심률 조절)":
    st.subheader("🛠️ 이심률($e$) 조절을 통한 궤도 설계")
    st.info("이심률 슬라이더를 움직여보세요. 궤도의 종류가 어떻게 변하나요?")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 학생이 직접 변경할 수 있는 파라미터
        e_val = st.slider("이심률 (Eccentricity, e)", 0.0, 2.0, 0.5, 0.01)
        a_val = st.slider("장반경 (Semi-major axis, a)", 0.5, 5.0, 1.5, 0.1)
        
        # 기하학적 분류 판정
        if e_val == 0:
            orbit_type = "원 (Circle)"
            color = "blue"
        elif 0 < e_val < 1:
            orbit_type = "타원 (Ellipse)"
            color = "green"
        elif e_val == 1:
            orbit_type = "포물선 (Parabola)"
            color = "yellow"
        else:
            orbit_type = "쌍곡선 (Hyperbola)"
            color = "red"
            
        st.success(f"현재 궤도 형태: **{orbit_type}**")
        
        # 수식 도출 (학생이 필기할 수 있도록 제공)
        if 0 <= e_val < 1:
            b_val = a_val * np.sqrt(1 - e_val**2)
            st.latex(rf"\frac{{x^2}}{{{a_val**2:.2f}}} + \frac{{y^2}}{{{b_val**2:.2f}}} = 1")
        elif e_val > 1:
            b_val = a_val * np.sqrt(e_val**2 - 1)
            st.latex(rf"\frac{{x^2}}{{{a_val**2:.2f}}} - \frac{{y^2}}{{{b_val**2:.2f}}} = 1")
            
        st.markdown("""
        **📝 탐구 활동:**
        1. 이심률이 **0.99에서 1.01**로 변할 때 그래프의 끝부분(개곡선 여부)을 관찰하세요.
        2. 타원 궤도에서 초점($c=ae$)의 위치를 계산해보고 태양의 위치와 비교해 보세요.
        """)

    with col2:
        # 시각화 로직
        fig = go.Figure()
        # 태양 (초점)
        c = a_val * e_val
        fig.add_trace(go.Scatter(x=[c if e_val < 1 else -c], y=[0], mode='markers', marker=dict(size=12, color='orange'), name='태양 (초점)'))
        
        # 곡선 그리기
        if e_val < 1: # 타원 및 원
            t = np.linspace(0, 2*np.pi, 200)
            b = a_val * np.sqrt(1 - e_val**2)
            x, y = a_val * np.cos(t), b * np.sin(t)
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color), name=orbit_type))
        elif e_val == 1: # 포물선 (근사치 처리)
            x = np.linspace(-2, 10, 200)
            p = a_val # 준선 관련 파라미터로 가정
            y = np.sqrt(4 * p * (x + p))
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color), name="포물선(위쪽)"))
            fig.add_trace(go.Scatter(x=x, y=-y, mode='lines', line=dict(color=color), name="포물선(아래쪽)"))
        else: # 쌍곡선
            t = np.linspace(-2, 2, 200)
            b = a_val * np.sqrt(e_val**2 - 1)
            x, y = a_val * np.cosh(t), b * np.sinh(t)
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color), name=orbit_type))
            
        fig.update_layout(xaxis=dict(range=[-7, 7]), yaxis=dict(range=[-5, 5], scaleanchor="x", scaleratio=1))
        st.plotly_chart(fig, use_container_width=True)

else:
    # 기존 NASA 데이터 모드
    df = get_nasa_data()
    st.subheader("🌍 NASA NEO(근지구천체) 데이터 분석")
    if not df.empty:
        selected = st.selectbox("분석할 소행성 선택", df['이름'])
        row = df[df['이름'] == selected].iloc[0]
        st.write(f"**이심률:** {row['이심률(e)']} | **장반경:** {row['장반경(a)']} AU")
        # (이하 기존 시각화 로직 동일)

st.markdown("---")
st.caption("수업 지원 도구: 2022 개정 교육과정 고교 기하 (이차곡선 실생활 응용 파트)")
