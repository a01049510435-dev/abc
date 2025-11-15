import streamlit as st
import random

# --- 1. 상태 초기화 ---
if 'score' not in st.session_state:
    st.session_state.score = 50 # 시작 점수
if 'dice1' not in st.session_state:
    st.session_state.dice1 = 1
if 'dice2' not in st.session_state:
    st.session_state.dice2 = 1

st.title("🍀 행운의 7 맞히기 게임")
st.markdown("규칙: 두 주사위 합이 7이면 **+20점**을 얻고, 아니면 **-5점**을 잃습니다.")

# --- 2. 게임 로직 함수 ---
def roll_dice():
    """두 주사위를 굴리고 점수를 업데이트합니다."""
    
    # 칩(점수)이 0 이하면 게임 진행 불가
    if st.session_state.score <= 0:
        st.session_state.game_message = "😭 칩이 부족합니다! 리셋하세요."
        return

    # 주사위 굴리기
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    st.session_state.dice1 = d1
    st.session_state.dice2 = d2
    
    total = d1 + d2
    
    # 승패 및 점수 계산
    if total == 7:
        st.session_state.score += 20
        st.session_state.game_message = f"🎉 **대박!** 합이 7입니다! **+20점** 획득!"
        st.balloons()
    else:
        st.session_state.score -= 5
        st.session_state.game_message = f"아쉽습니다. 합은 {total}입니다. **-5점** 차감."

# --- 3. UI 렌더링 ---

# 현재 점수 표시
st.subheader(f"💰 현재 점수: **{st.session_state.score}**점")

# 주사위 결과 표시 (더블 대시보드 형식)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("첫 번째 주사위", st.session_state.dice1)
with col2:
    st.metric("두 번째 주사위", st.session_state.dice2)
with col3:
    st.metric("주사위 합계", st.session_state.dice1 + st.session_state.dice2)
    
st.markdown("---")

# 게임 메시지 표시
if 'game_message' in st.session_state:
    st.write(st.session_state.game_message)
    
# 버튼
col_roll, col_reset = st.columns(2)

with col_roll:
    is_disabled = st.session_state.score <= 0
    st.button(
        "주사위 굴리기!", 
        on_click=roll_dice, 
        use_container_width=True, 
        type="primary",
        disabled=is_disabled
    )

with col_reset:
    if st.button("게임 리셋 (50점 시작)"):
        st.session_state.score = 50
        st.session_state.dice1 = 1
        st.session_state.dice2 = 1
        st.session_state.game_message = "게임을 다시 시작합니다."
        st.rerun()
