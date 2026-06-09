import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="이차곡선 방정식 모델링", layout="wide")

@st.cache_data
def fetch_neo_data():
    """NASA API에서 소행성의 궤도 파라미터(a, e)만 추출합니다."""
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
        
        # 기하 수업의 쌍곡선 탐구를 위해 e > 1 데이터 추가 (a의 절댓값 사용)
        df.loc[len(df)] = {'Name': 'Oumuamua (쌍곡선 궤도)', 'e': 1.1995, 'a': 1.29}
        return df
    except Exception as e:
        st.error("데이터를 불러오는 중 오류가 발생했습니다.")
        return pd.DataFrame()

# 메인 UI
st.title("📐 기하: 이차곡선 방정식과 궤도 모델링")
st.markdown("주어진 $a$(장반경)와 $e$(이심률) 데이터를 활용하여 타원과 쌍곡선의 방정식을 세우고 좌표평면 위에 그래프를 그려봅시다.")

# 데이터 로드
df = fetch_neo_data()

if not df.empty:
    st.sidebar.header("데이터 및 곡선 선택")
    curve_type = st.sidebar.radio("탐색할 이차곡선:", ["타원 (0 < e < 1)", "쌍곡선 (e > 1)"])
    
    if curve_type == "타원 (0 < e < 1)":
        filtered_df = df[(df['e'] > 0) & (df['e'] < 1)]
        st.subheader("🟢 타원의 방정식 도출")
    else:
        filtered_df = df[df['e'] > 1]
        st.subheader("🔴 쌍곡선의 방정식 도출")

    if not filtered_df.empty:
        selected_neo = st.sidebar.selectbox("분석할 데이터 선택:", filtered_df['Name'])
        neo_info = filtered_df[filtered_df['Name'] == selected_neo].iloc[0]
        
        # 기하학적 파라미터
        e = neo_info['e']
        a = neo_info['a']
        c = a * e  # 초점의 x좌표 (c)
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.markdown("### 1. 파라미터 계산")
            st.write(f"- **주어진 데이터:** 장축의 반 $a = {a:.4f}$, 이심률 $e = {e:.4f}$")
            st.write(f"- **초점 좌표 계산:** 초점 $F(c, 0)$에서 $c = a \\times e = {c:.4f}$")
            
            st.markdown("### 2. 방정식 세우기")
            if e < 1:
                # 타원: a^2 = b^2 + c^2 -> b = sqrt(a^2 - c^2)
                b = np.sqrt(a**2 - c**2)
                st.write(f"- **단축의 반 계산:** $b = \\sqrt{{a^2 - c^2}} = {b:.4f}$")
                st.markdown("#### 최종 타원의 방정식:")
                st.latex(rf"\frac{{x^2}}{{{a**2:.4f}}} + \frac{{y^2}}{{{b**2:.4f}}} = 1")
            else:
                # 쌍곡선: c^2 = a^2 + b^2 -> b = sqrt(c^2 - a^2)
                b = np.sqrt(c**2 - a**2)
                st.write(f"- **켤레축의 반 계산:** $b = \\sqrt{{c^2 - a^2}} = {b:.4f}$")
                st.markdown("#### 최종 쌍곡선의 방정식:")
                st.latex(rf"\frac{{x^2}}{{{a**2:.4f}}} - \frac{{y^2}}{{{b**2:.4f}}} = 1")
                st.markdown("#### 점근선의 방정식:")
                st.latex(rf"y = \pm \frac{{{b:.4f}}}{{{a:.4f}}} x")
                
        with col2:
            st.markdown("### 3. 좌표평면 시각화")
            fig = go.Figure()
            
            # 수학적 좌표계 설정 (x축, y축)
            fig.add_hline(y=0, line_width=1, line_color="black", opacity=0.5)
            fig.add_vline(x=0, line_width=1, line_color="black", opacity=0.5)
            
            # 초점(F, F') 표시
            fig.add_trace(go.Scatter(x=[c, -c], y=[0, 0], mode='markers+text', 
                                     marker=dict(size=10, color='black'),
                                     text=['F(c, 0)', "F'(-c, 0)"], textposition="top center", name='초점'))
            
            # 꼭짓점 표시
            fig.add_trace(go.Scatter(x=[a, -a], y=[0, 0], mode='markers', 
                                     marker=dict(size=8, color='gray', symbol='cross'), name='꼭짓점'))

            # 곡선 그리기
            if e < 1:
                t = np.linspace(0, 2*np.pi, 200)
                x_vals = a * np.cos(t)
                y_vals = b * np.sin(t)
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='blue', width=2), name='타원'))
                
                # 단축 꼭짓점 표시
                fig.add_trace(go.Scatter(x=[0, 0], y=[b, -b], mode='markers', 
                                         marker=dict(size=8, color='gray', symbol='cross'), showlegend=False))
                
                axis_range = [-a*1.5, a*1.5]
            else:
                t = np.linspace(-2.5, 2.5, 200)
                # 쌍곡선 양쪽 가지
                x_pos = a * np.cosh(t)
                y_pos = b * np.sinh(t)
                fig.add_trace(go.Scatter(x=x_pos, y=y_pos, mode='lines', line=dict(color='red', width=2), name='쌍곡선 (x>0)'))
                fig.add_trace(go.Scatter(x=-x_pos, y=y_pos, mode='lines', line=dict(color='red', width=2), name='쌍곡선 (x<0)'))
                
                # 점근선 그리기 (y = b/a * x, y = -b/a * x)
                x_asymp = np.array([-c*2, c*2])
                fig.add_trace(go.Scatter(x=x_asymp, y=(b/a)*x_asymp, mode='lines', line=dict(color='green', dash='dash', width=1), name='점근선'))
                fig.add_trace(go.Scatter(x=x_asymp, y=-(b/a)*x_asymp, mode='lines', line=dict(color='green', dash='dash', width=1), showlegend=False))
                
                axis_range = [-c*2, c*2]

            fig.update_layout(
                xaxis=dict(title='x', range=axis_range, zeroline=False),
                yaxis=dict(title='y', scaleanchor="x", scaleratio=1, zeroline=False),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=20, r=20, t=30, b=20)
            )
            # 그리드 추가
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            
            st.plotly_chart(fig, use_container_width=True)

# --- 학생 탐구 질문 섹션 ---
st.markdown("---")
st.subheader("📝 기하 탐구 질문")
st.markdown("""
1. **타원의 결정 조건:** 계산된 $a$와 $b$, 그리고 초점 $c$의 관계를 피타고라스 정리($a^2 = b^2 + c^2$)와 연결하여 타원 위의 임의의 점 $P(x, y)$에서 두 초점까지의 거리의 합이 $2a$로 일정함을 수식으로 증명해 보자.
2. **이심률에 따른 개형 변화:** 이심률 $e$의 값이 $0$에 가까워질 때와 $1$에 가까워질 때, 방정식 $\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1$ 에서 $a$와 $b$의 비율은 어떻게 변하는가? 이를 바탕으로 타원의 모양 변화를 설명해 보자.
3. **쌍곡선의 점근선과 미래 예측:** 쌍곡선의 방정식에서 $x$의 값이 무한히 커질 때($x \\to \\infty$), 그래프가 직선 $y = \\frac{b}{a}x$ 에 한없이 가까워짐을 극한을 이용하여 설명해 보자. 이 성질을 이용하면 혜성이 영원히 태양계를 벗어날 때 어떤 직선 궤적에 수렴하는지 예측할 수 있을까?
""")
