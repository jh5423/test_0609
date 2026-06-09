import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="나의 MBTI 진로 탐색기",
    page_icon="🧭",
    layout="centered"
)

# 메인 타이틀
st.title("🧭 나의 MBTI 진로 탐색기 🚀")
st.markdown("고등학교 생활, 내 적성과 진로가 고민되나요? **MBTI**를 통해 나에게 찰떡인 직업과 학과를 알아보세요! ✨")
st.divider()

# MBTI 데이터 딕셔너리 (대표적인 4가지 유형 예시 - 필요에 따라 16개로 확장 가능)
mbti_data = {
    "INTJ": {
        "nickname": "전략적인 완성주의자 ♟️",
        "traits": "분석적이고 논리적인 사고를 즐겨요. 복잡한 문제를 구조화하고 해결하는 데 탁월한 능력을 가지고 있죠!",
        "reason": "데이터의 이면을 파악하고 논리적인 패턴을 찾아내는 일은, INTJ의 치밀하고 분석적인 성향과 완벽하게 일치하기 때문이에요.",
        "majors": ["통계학과 📊", "데이터사이언스학과 💻", "수학교육과 📐", "소프트웨어공학과 ⚙️"],
        "careers": [
            {"name": "데이터 분석가 (Data Analyst)", "outlook": "⭐⭐⭐⭐⭐ (매우 밝음: AI와 빅데이터의 발전으로 모든 산업군에서 수요가 폭발적으로 증가하고 있습니다.)"},
            {"name": "인공지능 연구원", "outlook": "⭐⭐⭐⭐⭐ (매우 밝음: 미래 기술의 핵심으로, 지속적인 성장이 보장되는 분야입니다.)"}
        ]
    },
    "ENFP": {
        "nickname": "열정적인 스파크 🎇",
        "traits": "창의적이고 에너지가 넘치며, 새로운 가능성을 탐구하고 사람들과 소통하는 것을 진심으로 좋아해요!",
        "reason": "정해진 규칙과 틀보다는, 자유롭고 창의적인 환경에서 타인과 교감하며 아이디어를 실현할 때 가장 빛나는 유형이기 때문이에요.",
        "majors": ["미디어커뮤니케이션학과 🎬", "심리학과 🧠", "문화콘텐츠학과 🎨", "교육학과 📚"],
        "careers": [
            {"name": "콘텐츠 크리에이터 / 기획자", "outlook": "⭐⭐⭐⭐ (밝음: 개인 미디어와 숏폼 콘텐츠 시장의 확대로 독창적인 기획자의 가치가 높아지고 있습니다.)"},
            {"name": "심리 상담사", "outlook": "⭐⭐⭐⭐ (밝음: 사회가 복잡해지며 멘탈 케어의 중요성이 커져, AI가 대체하기 힘든 인간적인 직업으로 각광받습니다.)"}
        ]
    },
    "ISTJ": {
        "nickname": "신중한 원칙주의자 📋",
        "traits": "책임감이 강하고 현실적이며, 맡은 바를 끝까지 정확하게 해내는 꼼꼼함을 자랑해요.",
        "reason": "체계적인 환경에서 명확한 사실과 데이터를 바탕으로 일관성 있게 목표를 달성하는 일에 가장 큰 보람을 느끼기 때문이에요.",
        "majors": ["경영학과 🏢", "회계학과 🧮", "행정학과 🏛️", "컴퓨터공학과 🖥️"],
        "careers": [
            {"name": "정보보안 전문가", "outlook": "⭐⭐⭐⭐⭐ (매우 밝음: 디지털 전환 시대에 보안의 중요성이 극대화되어 안정적이고 수요가 높습니다.)"},
            {"name": "공인회계사 / 재무 분석가", "outlook": "⭐⭐⭐ (보통~밝음: AI가 보조 역할을 하겠지만, 최종적인 판단과 전략적 분석은 여전히 전문가의 몫입니다.)"}
        ]
    },
    "ESFJ": {
        "nickname": "다정다감한 조력자 🤝",
        "traits": "타인을 돕는 것을 좋아하고 공감 능력이 뛰어나며, 사람들과 협력하여 조화로운 결과를 만들어내요.",
        "reason": "다른 사람의 성장을 돕고, 따뜻한 소통을 통해 긍정적인 영향을 미칠 수 있는 환경에서 큰 에너지를 얻기 때문이에요.",
        "majors": ["교육학과 / 사범대 🏫", "간호학과 🏥", "사회복지학과 💛", "호텔경영학과 🛎️"],
        "careers": [
            {"name": "중고등학교 교사", "outlook": "⭐⭐⭐ (안정적: 학령인구는 감소하지만, 학생 개개인의 맞춤형 학습과 정서 발달을 이끄는 멘토로서의 역할은 더 중요해집니다.)"},
            {"name": "의료/보건 전문가", "outlook": "⭐⭐⭐⭐ (밝음: 고령화 사회 및 건강에 대한 관심 증가로 꾸준한 수요가 예상됩니다.)"}
        ]
    }
}

# 사용자 입력 받기
st.subheader("💡 나의 MBTI는?")
mbti_options = ["선택해주세요", "INTJ", "ENFP", "ISTJ", "ESFJ"] # 전체 16개로 수정하여 사용하세요.
selected_mbti = st.selectbox("아래에서 본인의 MBTI를 골라주세요!", mbti_options, label_visibility="collapsed")

if selected_mbti != "선택해주세요":
    data = mbti_data[selected_mbti]
    
    st.markdown(f"### 🎉 당신은 **{data['nickname']}** 이군요!")
    
    # 탭을 사용하여 정보 가독성 높이기
    tab1, tab2, tab3 = st.tabs(["🌟 성향 & 강점", "🎓 추천 학과", "💼 추천 직업 & 전망"])
    
    with tab1:
        st.info(f"**[{selected_mbti}의 특징]**\n\n{data['traits']}")
        st.success(f"**[이런 진로가 잘 맞는 이유]**\n\n{data['reason']}")
        
    with tab2:
        st.write("대학에 진학한다면 이런 전공들이 흥미로울 거예요!")
        for major in data['majors']:
            st.markdown(f"- **{major}**")
            
    with tab3:
        st.write("미래를 빛낼 추천 직업과 향후 전망입니다. 🔭")
        for career in data['careers']:
            with st.expander(f"📌 {career['name']}", expanded=True):
                st.markdown(f"**향후 전망:** {career['outlook']}")
                
    st.divider()
    st.caption("※ 진로는 언제든 바뀔 수 있어요! 위 내용은 참고만 하고, 여러분의 심장이 뛰는 진짜 꿈을 찾아가길 응원합니다. 화이팅! 🔥")
