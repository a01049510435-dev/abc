import streamlit as st
import random

st.title("🎲 초간단 주사위 던지기")

# 1. 주사위 굴리기 함수
def roll_dice():
    """1부터 6까지의 무작위 숫자를 생성합니다."""
    # 1에서 6 사이의 숫자를 랜덤으로 선택합니다.
    result = random.randint(1, 6)
    st.session_state.last_result = result
    
# 2. 상태 초기화 (결과를 저장)
if 'last_result' not in st.session_state:
    st.session_state.last_result = 1 # 초기값

# 3. 결과 표시
st.header(f"주사위 결과: **{st.session_state.last_result}**")

# 4. 버튼 (컨트롤)
st.button(
    "주사위 굴리기!", 
    on_click=roll_dice, 
    use_container_width=True, 
    type="primary"
)
