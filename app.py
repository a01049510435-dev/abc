import streamlit as st
import time
import random

# --- 1. 상태 및 시간 초기화 ---
# 'state'를 사용하여 0: 대기, 1: 준비, 2: 결과 상태를 관리합니다.
if 'state' not in st.session_state:
    st.session_state.state = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0

st.title("⚡ 초간단 반응 속도 측정기")
st.markdown("---")

# --- 2. 버튼 클릭 핸들러 ---
def handle_click():
    """클릭할 때마다 상태를 전환하고 시간을 기록합니다."""
    
    # 상태 0: 대기 중 -> 준비 시작
    if st.session_state.state == 0:
        st.session_state.state = 1
        st.session_state.start_time = time.time()
        
    # 상태 1: 준비 시작 -> 결과 계산 (반응 속도 측정)
    elif st.session_state.state == 1:
        end_time = time.time()
        reaction_time_ms = (end_time - st.session_state.start_time) * 1000
        st.session_state.reaction_time = reaction_time_ms
        st.session_state.state = 2 # 결과 상태로 전환
    
    # 상태 2: 결과 -> 재시작
    elif st.session_state.state == 2:
        st.session_state.state = 0 # 초기 상태로 돌아가 재시작

# --- 3. UI 렌더링 (상태별 메시지 및 버튼 표시) ---

button_label = "테스트 시작"
button_type = "primary"
message = "아래 버튼을 눌러 측정을 시작하세요."

if st.session_state.state == 1:
    button_label = "클릭!"
    button_type = "success"
    message = "🟢 **버튼이 초록색일 때 바로 클릭하세요!**"

elif st.session_state.state == 2:
    button_label = "다시 시작"
    reaction_time = st.session_state.reaction_time
    message = f"⏱️ **측정 완료! 당신의 반응 속도는 {reaction_time:.2f} ms 입니다!**"
    
    if reaction_time < 200:
        st.balloons()
        st.success("매우 빠릅니다! 200ms 미만!")

# 현재 메시지 표시
st.header(message)

# 메인 컨트롤 버튼
st.button(
    button_label, 
    on_click=handle_click, 
    use_container_width=True, 
    type=button_type
)
