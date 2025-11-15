import streamlit as st
import numpy as np

# --- 1. 상수 및 맵 설정 ---
PACMAN = "🟡"
DOT = "⚫"
WALL = "⬛"
EMPTY = "⬜"

# 2x2 맵 (벽과 점)
INITIAL_MAP = [
    [WALL, WALL, WALL, WALL],
    [WALL, DOT,  DOT,  WALL],
    [WALL, DOT,  DOT,  WALL],
    [WALL, WALL, WALL, WALL]
]

# --- 2. 상태 초기화 ---
if 'pos' not in st.session_state:
    st.session_state.pos = (1, 1) # (y, x)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'map' not in st.session_state:
    st.session_state.map = INITIAL_MAP # 맵 상태 복사

# --- 3. 핵심 로직: 팩맨 이동 및 처리 ---
def move_pacman(dy, dx):
    """팩맨을 움직이고 충돌/점 획득을 처리합니다."""
    cy, cx = st.session_state.pos
    ny, nx = cy + dy, cx + dx
    
    # 1. 벽 충돌 확인
    if st.session_state.map[ny][nx] == WALL:
        st.info("⚠️ 벽입니다!")
        return
        
    # 2. 팩맨 위치 업데이트
    st.session_state.pos = (ny, nx)
    
    # 3. 점 획득 확인
    if st.session_state.map[ny][nx] == DOT:
        st.session_state.score += 10
        st.session_state.map[ny][nx] = EMPTY # 점을 빈 공간으로 변경
        st.toast("점 획득!", icon='🟡')

# --- 4. 맵 렌더링 ---
def render_map():
    """현재 상태를 반영하여 맵을 표시합니다."""
    map_display = ""
    for r in range(len(st.session_state.map)):
        row_display = ""
        for c in range(len(st.session_state.map[0])):
            pos = (r, c)
            
            if pos == st.session_state.pos:
                row_display += f" {PACMAN} "
            else:
                row_display += f" {st.session_state.map[r][c]} "
        map_display += row_display + "\n"
    st.code(map_display)


# --- 5. UI 및 컨트롤 통합 ---
st.title("🟡 초간단 키보드 제어 시뮬레이션")
st.markdown(f"**점수:** `{st.session_state.score}`")

render_map()

# ⚠️ 이 부분이 키보드 입력을 처리해야 하는 부분입니다.
st.info("키보드 제어 기능을 활성화하려면 **외부 컴포넌트**를 사용해야 합니다.")

# (실제 키보드 이벤트 리스너 코드는 컴포넌트에 의해 자동으로 삽입된다고 가정)

# 디버깅/테스트용 버튼 (키보드 컴포넌트 없이 테스트할 때 사용)
st.caption("디버깅/테스트용: 버튼을 눌러 이동하세요")

col1, col2, col3 = st.columns(3)
with col2: st.button("⬆️", on_click=
