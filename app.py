import streamlit as st
import random

# --- 1. 상태 초기화 ---
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = 0 # 0: 시작, 1: 중간, 2: 목표
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

st.title("🌱 최소 이동 시뮬레이션")

# --- 2. 맵 표시 ---
def display_map():
    """현재 플레이어 위치에 따라 맵을 표시합니다."""
    
    # 텍스트 기반 맵: [시작] -> [중간] -> [목표]
    cells = ["⬜", "⬜", "🏆"] 
    
    if st.session_state.player_pos < len(cells):
        cells[st.session_state.player_pos] = "🐸" # 현재 위치 표시
        
    st.code(" ".join(cells))

# --- 3. 이동 처리 함수 ---
def try_move():
    """이동 버튼 클릭 시 로직 처리"""
    if st.session_state.game_over:
        return
        
    # 50% 확률로 장애물에 걸림 (게임 오버)
    if st.session_state.player_pos == 1 and random.random() < 0.5:
        st.session_state.game_over = True
        st.error("💥 **장애물! 게임 오버!**")
        return

    # 다음 칸으로 이동
    st.session_state.player_pos += 1
    
    # 목표 지점 도착
    if st.session_state.player_pos >= 2:
        st.session_state.game_over = True
        st.balloons()
        st.success("🏆 **성공!** 목표에 도착했습니다!")
        

# --- 4. UI 렌더링 ---
display_map()

if not st.session_state.game_over:
    st.button(
        "➡️ 한 칸 이동 시도", 
        on_click=try_move, 
        use_container_width=True, 
        type="primary"
    )
else:
    if st.button("🔄 다시 시작"):
        st.session_state.player_pos = 0
        st.session_state.game_over = False
        st.rerun() # 앱을 새로고침하여 초기 상태로 돌아갑니다.
