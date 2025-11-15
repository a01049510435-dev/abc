import streamlit as st
import random

# 1. 상태(Score) 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'shots_fired' not in st.session_state:
    st.session_state.shots_fired = 0
if 'message' not in st.session_state:
    st.session_state.message = "게임 시작!"

st.title("🔫 Streamlit 슈팅 시뮬레이션")
st.markdown("---")

# 2. 게임 로직 함수
def shoot_target():
    """총알을 발사하고 점수를 업데이트하는 함수"""
    st.session_state.shots_fired += 1
    
    # 30% 확률로 명중 (Hit)
    if random.random() < 0.3:
        st.session_state.score += 10
        st.session_state.message = "🎯 명중! (+10점)"
    else:
        st.session_state.score -= 1 # 빗맞췄을 때 패널티
        st.session_state.message = "❌ 빗나감... (-1점)"

# 3. 게임 상태 표시
col1, col2 = st.columns(2)
with col1:
    st.metric("현재 점수 (SCORE)", st.session_state.score)
with col2:
    st.metric("총 발사 횟수 (SHOTS)", st.session_state.shots_fired)
    
st.subheader(st.session_state.message)

# 4. '발사' 버튼 (가장 중요한 상호작용)
# 버튼을 누르는 것이 '총을 쏘는' 행위라고 가정합니다.
st.markdown("##") # 공간 확보
if st.button("💥 발사! (Shoot!)", use_container_width=True):
    shoot_target()
    
# 5. 간단한 시각적 요소 추가 (조준경 흉내)
# 이 이미지는 실제 Streamlit 앱에서는 표시되지 않고, 사용자에게 시각적 힌트를 줍니다.
st.markdown("---")
st.caption("실제 FPS와 달리 이미지가 움직이거나 적이 없습니다.")
st.image("https://via.placeholder.com/600x200?text=<<+Target+Area+>>", use_column_width=True)
