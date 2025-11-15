import streamlit as st
import random

# --- 1. 게임 설정 ---
GRID_SIZE = 5 # 맵 크기 (5x5)
PLAYER = "🐸"
GOAL = "🏆"
ROADBLOCK = "🚗"

# --- 2. 상태 초기화 ---
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = [GRID_SIZE - 1, GRID_SIZE // 2] # 시작 위치 (맨 아래 중앙)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'map' not in st.session_state:
    st.session_state.map = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# --- 3. 맵 생성 함수 ---
def initialize_map():
    """맵에 무작위로 장애물과 목표 지점을 배치합니다."""
    new_map = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # 맵에 무작위 장애물 배치 (약 15% 확률)
    for r in range(GRID_SIZE - 1): # 마지막 줄(시작 위치) 제외
        for c in range(GRID_SIZE):
            if random.random() < 0.15: 
                new_map[r][c] = ROADBLOCK
                
    # 목표 지점 배치 (맨 위 줄의 랜덤 위치)
    goal_col = random.randint(0, GRID_SIZE - 1)
    new_map[0][goal_col] = GOAL
    
    st.session_state.map = new_map

# 맵이 초기화되지 않았다면 초기화
if not st.session_state.map or st.session_state.game_over:
    initialize_map()


# --- 4. 움직임 처리 함수 ---
def move_player(dr, dc):
    """플레이어의 위치를 업데이트하고 충돌을 확인합니다."""
    if st.session_state.game_over:
        return

    r, c = st.session_state.player_pos
    new_r, new_c = r + dr, c + dc

    # 경계 확인
    if 0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE:
        st.session_state.player_pos = [new_r, new_c]
        
        # 충돌 및 목표 확인
        target_cell = st.session_state.map[new_r][new_c]
        
        if target_cell == ROADBLOCK:
