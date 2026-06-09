import streamlit as st
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="나만의 맞춤 운동 찾기",
    page_icon="🏃‍♀️",
    layout="centered"
)

# 운동 데이터베이스 (점수 계산 및 추천을 위한 정보)
exercise_db = [
    {
        "name": "수영 🏊",
        "description": "관절에 무리 없이 전신 근력과 심폐지구력을 기를 수 있는 최고의 운동입니다.",
        "benefits": ["무릎/허리 관절 부담 최소화", "뛰어난 칼로리 소모", "전신 밸런스 향상"],
        "how_to": "처음에는 킥판을 잡고 발차기부터 시작하세요. 주 2~3회 강습을 통해 기초 자세를 잡는 것을 추천합니다.",
        "video_url": "https://www.youtube.com/watch?v=Fq2s7bB4hZg", # 수영 초보 가이드 예시
        "tags": {"goal": "심폐지구력", "type": "혼자", "place": "실내", "impact": "low"}
    },
    {
        "name": "요가 / 필라테스 🧘‍♀️",
        "description": "굳어있는 몸을 풀어주고 삐뚤어진 체형을 교정하며, 마음의 안정을 찾는 데 탁월합니다.",
        "benefits": ["유연성 증가 및 자세 교정", "코어 근력 강화", "스트레스 감소 및 멘탈 힐링"],
        "how_to": "무리가 가지 않는 선에서 시작하세요. 호흡에 집중하며 동작을 천천히 따라하는 것이 핵심입니다.",
        "video_url": "https://www.youtube.com/watch?v=v7sn-d0E_iw", # 요가소년 15분 전신 스트레칭
        "tags": {"goal": "유연성/자세교정", "type": "혼자/클래스", "place": "실내", "impact": "low"}
    },
    {
        "name": "가벼운 러닝 (조깅) 🏃",
        "description": "특별한 장비 없이 신발만 있으면 당장 시작할 수 있는 가장 접근성 좋은 유산소 운동입니다.",
        "benefits": ["심폐지구력 및 체력 극대화", "우울감 감소 및 리프레시 효과", "하체 근력 강화"],
        "how_to": "처음부터 뛰지 마세요! 5분 걷고 1분 뛰는 '인터벌 러닝'으로 시작하여 천천히 뛰는 시간을 늘려보세요.",
        "video_url": "https://www.youtube.com/watch?v=0-X7VbX3l4I", # 초보 러닝 가이드
        "tags": {"goal": "심폐지구력", "type": "혼자/크루", "place": "야외", "impact": "high"}
    },
    {
        "name": "홈트레이닝 (맨몸 운동) 🏠",
        "description": "집에서 유튜브를 보며 나만의 페이스로 안전하고 꾸준하게 할 수 있는 운동입니다.",
        "benefits": ["이동 시간 0분, 최고의 효율", "타인의 시선에서 자유로움", "기초 체력 및 근력 향상"],
        "how_to": "하루 15분, 스트레칭과 가벼운 맨몸 근력 운동(스쿼트, 플랭크 등) 영상으로 가볍게 시작하세요.",
        "video_url": "https://www.youtube.com/watch?v=swRNeYw1JkY", # 가벼운 홈트
        "tags": {"goal": "근력/다이어트", "type": "혼자", "place": "실내", "impact": "medium"}
    },
    {
        "name": "웨이트 트레이닝 (헬스) 🏋️‍♂️",
        "description": "탄탄한 몸매와 근력을 원한다면 필수! 기구를 이용해 원하는 부위를 집중적으로 타겟팅합니다.",
        "benefits": ["기초대사량 증가 (살 안 찌는 체질)", "체형 조각 및 근육량 증가", "자신감 뿜뿜"],
        "how_to": "처음 1~2달은 머신 위주로 가볍게 자극을 느끼거나, PT를 통해 정확한 자세를 배우는 것이 부상 방지에 좋습니다.",
        "video_url": "https://www.youtube.com/watch?v=QzeG2r9E4tU", # 헬스장 초보
        "tags": {"goal": "근력/다이어트", "type": "혼자", "place": "실내", "impact": "medium"}
    },
    {
        "name": "등산 / 트레킹 ⛰️",
        "description": "자연의 맑은 공기를 마시며 성취감과 하체 근력을 동시에 얻을 수 있는 액티비티입니다.",
        "benefits": ["탁월한 멘탈 케어 및 스트레스 해소", "강력한 하체 근력 및 심폐지구력", "정상에서의 쾌감"],
        "how_to": "동네의 낮고 완만한 둘레길부터 시작하세요. 무릎 보호를 위해 등산화와 스틱은 필수입니다!",
        "video_url": "https://www.youtube.com/watch?v=2zLwZ3P0Ew4", # 초보 등산
        "tags": {"goal": "스트레스해소", "type": "혼자/모임", "place": "야외", "impact": "high"}
    },
    {
        "name": "크로스핏 / F45 💦",
        "description": "다 같이 땀 흘리며 파이팅 넘치게 한계에 도전하는 고강도 그룹 운동입니다.",
        "benefits": ["단시간 폭발적인 칼로리 소모", "근력과 유산소를 동시에", "끈끈한 커뮤니티와 동기부여"],
        "how_to": "체력이 약해도 괜찮습니다! 코치가 개인 수준에 맞춰 무게와 동작을 조정(스케일링)해 줍니다.",
        "video_url": "https://www.youtube.com/watch?v=tzD9BkXAQwc", # 크로스핏 입문
        "tags": {"goal": "근력/다이어트", "type": "그룹", "place": "실내", "impact": "high"}
    },
    {
        "name": "배드민턴 / 테니스 🏸",
        "description": "지루한 운동은 가라! 공을 치는 재미에 푹 빠지다 보면 어느새 땀이 비 오듯 쏟아집니다.",
        "benefits": ["순발력 및 민첩성 향상", "스트레스 해소와 재미 보장", "파트너와 함께하는 즐거움"],
        "how_to": "가까운 동호회나 레슨에 등록해 라켓 잡는 법부터 배우세요. 다치기 쉬우니 충분한 스트레칭이 필요합니다.",
        "video_url": "https://www.youtube.com/watch?v=91R5-L5Hl_M", # 테니스/배드민턴 기초
        "tags": {"goal": "스트레스해소", "type": "그룹", "place": "야외/실내", "impact": "medium"}
    }
]

st.title("🩺 나만의 맞춤 운동 찾기 🔍")
st.markdown("""
운동을 해야 하는 건 알지만, **어떤 운동이 나에게 맞는지** 몰라서 망설이셨나요?
딱 1분만 투자해서 6가지 질문에 답해보세요. 현재 건강 상태와 취향을 분석해 
당신에게 **가장 잘 맞는 운동과 시작하는 방법**을 알려드립니다! 💪
""")
st.divider()

# 폼을 사용하여 결과가 한 번에 계산되도록 함
with st.form("exercise_form"):
    st.subheader("📝 나의 현재 상태와 취향 알려주기")
    
    # Q1. 관절 상태 (가장 중요 - 고위험 운동 필터링용)
    q1 = st.selectbox(
        "1. 현재 가장 불편하거나 통증이 있는 부위가 있나요? (관절 상태 확인)",
        ["없음 (아주 건강해요!)", "무릎이나 발목 (하체 관절이 약함)", "허리나 목 (디스크나 뻐근함이 있음)", "어깨나 손목 (상체 관절이 약함)"]
    )
    
    # Q2. 현재 체력 수준
    q2 = st.radio(
        "2. 평소 숨쉬기 외에 신체 활동을 얼마나 하시나요?",
        ["거의 안 함 (기초 체력 제로)", "가벼운 산책이나 스트레칭 정도 (입문)", "주 2~3회 꾸준히 땀 흘려 운동 중 (중급 이상)"]
    )
    
    # Q3. 운동 목적
    q3 = st.selectbox(
        "3. 이번 운동을 통해 '가장' 얻고 싶은 한 가지는 무엇인가요?",
        ["체중 감량 및 근력 강화 (탄탄한 몸)", "심폐지구력 및 체력 증진 (지치지 않는 체력)", "유연성 증가 및 체형/자세 교정", "스트레스 해소 및 멘탈 힐링"]
    )
    
    # Q4. 선호하는 운동 방식
    q4 = st.radio(
        "4. 어떤 방식으로 운동할 때 더 힘이 나나요?",
        ["혼자 조용히 내 페이스에 맞춰서 집중하기", "사람들과 어울리거나 파이팅 넘치는 분위기에서 다 같이!"]
    )
    
    # Q5. 선호하는 장소
    q5 = st.radio(
        "5. 실내와 야외 중 어디가 더 끌리나요?",
        ["실내 (집, 헬스장, 스튜디오 등 날씨 영향 없는 곳)", "야외 (공원, 산, 강변 등 탁 트인 자연)"]
    )
    
    # Q6. 투자 가능 시간
    q6 = st.select_slider(
        "6. 하루에 운동에 투자할 수 있는 시간은 어느 정도인가요?",
        options=["15~30분 (바쁨)", "1시간 정도 (보통)", "2시간 이상 (여유)"]
    )
    
    submitted = st.form_submit_button("✨ 나에게 맞는 운동 결과 보기 ✨", use_container_width=True)

if submitted:
    with st.spinner('당신의 답변을 분석하며 최적의 운동을 찾고 있습니다... 🤖💭'):
        time.sleep(1.5) # 분석하는 듯한 효과 부여
        
        # 각 운동에 대한 점수 초기화
        scores = {ex['name']: 0 for ex in exercise_db}
        
        for ex in exercise_db:
            name = ex['name']
            tags = ex['tags']
            
            # 1. 통증 부위에 따른 감점 및 가산점 (가장 중요한 필터)
            if "무릎" in q1 or "허리" in q1:
                if tags['impact'] == "high":
                    scores[name] -= 50  # 관절에 무리 가는 운동 크게 감점 (러닝, 크로스핏 등)
                if name == "수영 🏊" or name == "요가 / 필라테스 🧘‍♀️":
                    scores[name] += 20  # 관절에 좋은 운동 강력 추천
            
            # 2. 운동 목적 매칭
            if "근력" in q3 and "근력" in tags['goal']: scores[name] += 10
            if "심폐" in q3 and "심폐지구력" in tags['goal']: scores[name] += 10
            if "유연성" in q3 and "자세교정" in tags['goal']: scores[name] += 10
            if "스트레스" in q3 and "스트레스" in tags['goal']: scores[name] += 10
            
            # 3. 운동 방식 매칭
            if "혼자" in q4 and "혼자" in tags['type']: scores[name] += 10
            if "사람들" in q4 and ("그룹" in tags['type'] or "클래스" in tags['type'] or "모임" in tags['type']): scores[name] += 10
            
            # 4. 장소 매칭
            if "실내" in q5 and "실내" in tags['place']: scores[name] += 10
            if "야외" in q5 and "야외" in tags['place']: scores[name] += 10

            # 5. 시간 매칭 (짧은 시간이면 홈트 우선 추천 등)
            if "15~30분" in q6 and name == "홈트레이닝 (맨몸 운동) 🏠": scores[name] += 15

        # 점수 기준 내림차순 정렬
        sorted_exercises = sorted(exercise_db, key=lambda x: scores[x['name']], reverse=True)
        top_1 = sorted_exercises[0]
        top_2 = sorted_exercises[1]

        st.success("분석 완료! 당신에게 딱 맞는 운동을 찾았습니다. 🎉")
        st.divider()
        
        # 1위 운동 출력
        st.markdown("### 🥇 1순위 추천 운동: " + top_1['name'])
        st.write(top_1['description'])
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### ✨ 이런 점이 좋아요!")
            for benefit in top_1['benefits']:
                st.markdown(f"✔️ {benefit}")
        with col2:
            st.markdown("#### 👟 이렇게 시작해 보세요!")
            st.info(top_1['how_to'])
            
        # 유튜브 추천 영상
        with st.expander("📺 기초 입문을 위한 추천 영상 보기", expanded=True):
            st.video(top_1['video_url'])
            st.caption("영상을 보며 가볍게 분위기를 파악하거나 집에서 바로 따라해 보세요!")

        st.divider()

        # 2위 운동 출력 (서브 추천)
        st.markdown("### 🥈 2순위 추천 운동: " + top_2['name'])
        st.write("1순위 운동이 조금 부담스럽다면, 이 운동은 어떨까요?")
        
        col3, col4 = st.columns([1, 1])
        with col3:
            st.markdown("#### ✨ 이런 점이 좋아요!")
            for benefit in top_2['benefits']:
                st.markdown(f"✔️ {benefit}")
        with col4:
            st.markdown("#### 👟 이렇게 시작해 보세요!")
            st.info(top_2['how_to'])
            
        with st.expander("📺 기초 입문을 위한 추천 영상 보기", expanded=False):
            st.video(top_2['video_url'])

        st.divider()
        st.markdown("### 💡 오늘부터 바로 시작해 볼까요?")
        st.markdown("**'시작이 반이다'**라는 말이 있죠. 영상의 플레이 버튼을 누르는 것부터가 운동의 시작입니다. 무리하지 말고 즐겁게 운동하며 건강한 나를 만나보세요! 화이팅! 🚀")
