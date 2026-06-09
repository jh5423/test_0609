import streaㅜmlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="NASA 데이터로 그리는 이차곡선", layout="wide")

@st.cache_data
def fetch_neo_data():
    """NASA NeoWs API를 통해 소행성 데이터를 가져옵니다."""
    url = "https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        neos = data.get('near_earth_objects', [])
        
        extracted_data = []
        for neo in neos:
            orbital = neo.get('orbital_data', {})
            name = neo.get('name', 'Unknown')
            e = float(orbital.get('eccentricity', 0))
            a = float(orbital.get('semi_major_axis', 0))
            
            # 유효한 궤도 데이터가 있는 경우만 추가
            if a > 0:
                extracted_data.append({'Name': name, 'e (이심률)': e, 'a (장반경)': a})
        
        df = pd.DataFrame(extracted_data)
        
        # 수업을 위해 e > 1 인 쌍곡선 데이터(오무아무아) 강제 추가
        oumuamua_data = {'Name': '1I/Oumuamua (성간 천체)', 'e (이심률)': 1.1995, 'a (장반경)': -1.29} # 쌍곡선의 a는 음수로 표기되기도 하나, 계산을 위해 절댓값 사용
        df.loc[len(df)] = oumuamua_data
        
        return df
    else:
        st.error("NASA API에서 데이터를 불러오지 못했습니다.")
        return pd.DataFrame()

# 메인 UI
st.title("🌌 NASA 소행성 데이터와 이차곡선의 세계")
st.markdown("NASA의 근지구천체(NEO) 데이터를 분석하여 소행성과 혜성의 궤도를 직접 모델링해 봅시다.")

# 데이터 불러오기
df = fetch_neo_data()

if not df.empty:
    st.sidebar.header("궤도 설정")
    orbit_type = st.sidebar.radio("탐구할 궤도 형태를 선택하세요:", ["타원 궤도 (0 < e < 1)", "쌍곡선 궤도 (e > 1)"])
    
    if orbit_type == "타원 궤도 (0 < e < 1)":
        filtered_df = df[(df['e (이심률)'] > 0) & (df['e (이심률)'] < 1)]
        st.subheader("🪐 타원 궤도 소행성 분석")
    else:
        filtered_df = df[df['e (이심률)'] > 1]
        st.subheader("☄️ 쌍곡선 궤도 천체 분석")
        st.info("이심률이 1보다 큰 천체는 태양계의 중력을 벗어나 스쳐 지나가는 성간 천체(예: 오무아무아)입니다.")

    if not filtered_df.empty:
        selected_neo = st.sidebar.selectbox("분석할 천체를 선택하세요:", filtered_df['Name'])
        neo_info = filtered_df[filtered_df['Name'] == selected_neo].iloc[0]
        
        e = neo_info['e (이심률)']
        a = abs(neo_info['a (장반경)']) # 장반경의 크기
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 천체 궤도 데이터")
            st.write(f"- **천체 이름:** {selected_neo}")
            st.write(f"- **궤도 이심률 ($e$):** {e:.4f}")
            st.write(f"- **장축의 반 ($a$):** {a:.4f} AU")
            
            if e < 1:
                # 타원: b = a * sqrt(1 - e^2)
                b = a * np.sqrt(1 - e**2)
                st.write(f"- **단축의 반 ($b$):** {b:.4f} AU")
                st.markdown("### 📐 타원의 방정식")
                st.latex(rf"\frac{{x^2}}{{{a**2:.4f}}} + \frac{{y^2}}{{{b**2:.4f}}} = 1")
            else:
                # 쌍곡선: b = a * sqrt(e^2 - 1)
                b = a * np.sqrt(e**2 - 1)
                st.write(f"- **켤레축의 반 ($b$):** {b:.4f} AU")
                st.markdown("### 📐 쌍곡선의 방정식")
                st.latex(rf"\frac{{x^2}}{{{a**2:.4f}}} - \frac{{y^2}}{{{b**2:.4f}}} = 1")
                
        with col2:
            st.markdown("### 궤도 시각화")
            fig = go.Figure()
            
            # 태양(초점) 그리기
            c = a * e # 중심에서 초점까지의 거리
            if e < 1:
                sun_x = c
            else:
                sun_x = -c # 쌍곡선의 경우 태양의 위치를 왼쪽 초점으로 가정
                
            fig.add_trace(go.Scatter(x=[sun_x], y=[0], mode='markers', marker=dict(size=15, color='orange'), name='Sun (Focus)'))
            
            t = np.linspace(0, 2*np.pi, 100)
            if e < 1:
                x = a * np.cos(t)
                y = b * np.sin(t)
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'{selected_neo} Orbit'))
            else:
                t_hyper = np.linspace(-2, 2, 100)
                # 오른쪽 쌍곡선
                x_pos = a * np.cosh(t_hyper)
                y_pos = b * np.sinh(t_hyper)
                fig.add_trace(go.Scatter(x=x_pos, y=y_pos, mode='lines', line=dict(color='red'), name=f'{selected_neo} Trajectory'))

            fig.update_layout(
                xaxis_title='x (AU)', yaxis_title='y (AU)',
                yaxis=dict(scaleanchor="x", scaleratio=1), # x, y 비율 동일하게
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

# --- 학생 탐구 질문 섹션 ---
st.markdown("---")
st.subheader("💡 스스로 탐구해 보기")
st.markdown("""
1. **궤도의 모양과 이심률:** 선택한 소행성의 이심률($e$) 값을 바꿔가며 시각화한다면, $e$가 0에 가까워질 때와 1에 가까워질 때 궤도의 모양은 어떻게 변하나요?
2. **초점의 의미:** 시각화된 그래프에서 태양은 타원(또는 쌍곡선)의 중심이 아닌 초점(Focus)에 위치해 있습니다. 케플러 제1법칙과 이차곡선의 초점을 연결하여 설명해 보세요.
3. **미래 궤적 예측:** 이심률이 1보다 큰 오무아무아와 같은 천체는 태양계를 영원히 벗어나게 됩니다. 도출된 쌍곡선의 방정식을 이용해 천체가 한없이 멀어질 때 점근선에 가까워지는 성질을 바탕으로, 이 천체가 최종적으로 향하는 방향(기울기)을 계산해 보세요.
""")
