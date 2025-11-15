import streamlit as st
import random

# --- 1. 상수 정의 ---
GRID_HEIGHT = 8  # 맵의 높이 (화면에 보이는 줄 수)
GRID_WIDTH = 5   # 맵의 폭 (차선 수)
PLAYER = "🐸"
ROADBLOCK = "🚗"
EMPTY = "⬜"

# --- 2. 상태 초기화 ---
# st.session_state를 사용하여 게임 상태를 저장합니다.
if 'player_x' not in st.session_state:
    st.session_state.player_x = GRID_WIDTH // 2  # 플레이어의 X 위치 (중앙 시작)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'map' not in st.session_state:
    st.session_state.map = []

# --- 3. 핵심 함수: 맵 관리 ---
def generate_new_row():
    """무작위 장애물 줄을 생성합니다."""
    new_row = [EMPTY] * GRID_WIDTH
    # 20% 확률로 각 칸에 장애물 배치
    for i in range(GRID_WIDTH):
        if random.random() < 0.2:
            new_row[i] = ROADBLOCK
    return new_row

def reset_game():
    """게임 상태와 맵을 초기화합니다."""
    st.session_state.player_x = GRID_WIDTH // 2
    st.session_state.score = 0
    st.session_state.game_over = False
    
    # 초기 맵: 맨 아래 줄은 빈 공간, 나머지는 무작위 장애물 줄
    initial_map = [generate_new_row() for _ in range(GRID_HEIGHT - 1)]
    initial_map.append([EMPTY] * GRID_WIDTH) # 플레이어가 시작하는 맨 아래 줄
    st.session_state.map = initial_map

# 게임 시작 시 초기화
if not st.session_state.map or st.session_state.game_over:
    reset_game()

# --- 4. 움직임 처리 함수 ---
def move_player(dx, dy):
    """플레이어를 움직이고 게임 로직을 처리합니다."""
    if st.session_state.game_over:
        return

    # 1. 좌우 이동 (X축)
    if dx != 0:
        new_x = st.session_state.player_x + dx
        if 0 <= new_x < GRID_WIDTH:
            st.session_state.player_x = new_x
            
    # 2. 전진 (위로 한 칸 이동)
    elif dy == -1: 
        # 점수 증가
        st.session_state.score += 1
        
        # 맵 스크롤: 맨 아래 줄을 제거하고 맨 위에 새 줄을 추가
        st.session_state.map.pop()
        st.session_state.map.insert(0, generate_new_row())
        
        # 충돌 확인: 맵이 스크롤 된 후, 플레이어 위치에 장애물이 있는지 확인
        # 플레이어는 항상 맵 리스트의 맨 아래(GRID_HEIGHT - 1)에 위치합니다.
        if st.session_state.map[GRID_HEIGHT - 1][st.session_state.player_x] == ROADBLOCK:
            st.session_state.game_over = True
            st.error("💥 **장애물에 부딪혔습니다! 게임 오버!**")
            st.toast("게임 오버!", icon='🚗')


# --- 5. UI 및 맵 렌더링 ---
st.header("🐸 미니 로드 크로스")
st.markdown(f"**현재 점수: {st.session_state.score}** | ⬆️ 전진할 때마다 점수 1 증가")

# 격자(Grid) 표시
map_display = ""
for r in range(GRID_HEIGHT):
    row_display = ""
    for c in range(GRID_WIDTH):
        item = st.session_state.map[r][c]
        
        # 플레이어 위치 표시: 플레이어는 항상 맵의 맨 아래 줄에만 존재합니다.
        if r == GRID_HEIGHT - 1 and c == st.session_state.player_x:
            row_display += f" {PLAYER} "
        else:
            row_display += f" {item} "
    map_display += row_display + "\n"

# 맵을 코드 블록으로 시각화합니다.
st.code(map_display)

# --- 6. 사용자 컨트롤 버튼 ---
if not st.session_state.game_over:
    
    # 전진 버튼 (메인 액션)
    st.button("⬆️ 한 줄 전진!", on_click=move_player, args=(0, -1), use_container_width=True, type="primary") 

    # 좌우 버튼
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("⬅️", on_click=move_player, args=(-1, 0), use_container_width=True)
    with col3:
        st.button("➡️", on_click=move_player, args=(1, 0), use_container_width=True)
        
    st.caption("좌우 이동은 차선 변경입니다. ⬆️ 버튼을 눌러야 맵이 스크롤됩니다.")

# --- 7. 리셋 버튼 ---
if st.session_state.game_over:
    if st.button("🔄 다시 시작", type="primary"):
        reset_game()
        st.rerun() # 앱을 새로고침하여 초기 상태로 돌아갑니다.
