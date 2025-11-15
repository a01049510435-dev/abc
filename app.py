import streamlit as st
import random

# --- 1. 게임 상수 설정 ---
MAX_AMMO = 10       # 최대 장전 탄약 수
HIT_PROBABILITY = 0.40 # 기본 명중률 (40%)
SCORE_PER_HIT = 10  # 명중 시 얻는 점수

# --- 2. 상태 초기화 ---
if 'ammo' not in st.session_state:
    st.session_state.ammo = MAX_AMMO
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_shots' not in st.session_state:
    st.session_state.total_shots = 0
if 'message' not in st.session_state:
    st.session_state.message = "게임을 시작하려면 '발사'하세요!"

st.title("🔫 Streamlit 정교한 사격 시뮬레이션")
st.caption("주의: 이 게임은 버튼 클릭 기반의 시뮬레이션입니다.")

# --- 3. 게임 로직 함수 ---
def shoot():
    """총을 발사하고 상태를 업데이트합니다."""
    
    if st.session_state.ammo <= 0:
        st.session_state.message = "🛑 **총알이 없습니다! 재장전하세요!**"
        return

    # 탄약 감소 및 총 발사 횟수 증가
    st.session_state.ammo -= 1
    st.session_state.total_shots += 1

    # 명중률 계산
    if random.random() < HIT_PROBABILITY:
        # 명중 시
        st.session_state.score += SCORE_PER_HIT
        st.session_state.message = f"🎯 **명중!** (+{SCORE_PER_HIT}점) | 남은 총알: {st.session_state.ammo}"
    else:
        # 빗맞음 시
        st.session_state.message = f"❌ 빗나갔습니다. | 남은 총알: {st.session_state.ammo}"
        
def reload():
    """총알을 재장전합니다."""
    if st.session_state.ammo == MAX_AMMO:
        st.session_state.message = "이미 탄창이 가득 찼습니다!"
    else:
        st.session_state.ammo = MAX_AMMO
        st.session_state.message = "🔄 **재장전 완료!** 탄창이 가득 찼습니다."

def calculate_accuracy():
    """명중률을 계산합니다."""
    if st.session_state.total_shots == 0:
        return 0.0
    hits = (st.session_state.score / SCORE_PER_HIT)
    return (hits / st.session_state.total_shots) * 100

# --- 4. UI 렌더링 및 상태 표시 ---

# 점수, 탄약, 명중률 표시 (가장 정교한 요소)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 점수", st.session_state.score)
with col2:
    st.metric("남은 총알", f"{st.session_state.ammo} / {MAX_AMMO}")
with col3:
    st.metric("명중률", f"{calculate_accuracy():.1f}%")

st.markdown("---")
st.subheader(st.session_state.message)

# 사격/재장전 버튼
col_shoot, col_reload = st.columns(2)

# 발사 버튼
with col_shoot:
    # 총알이 없으면 버튼 비활성화 (disabled=True)
    is_shoot_disabled = st.session_state.ammo <= 0
    st.button(
        "💥 발사! (Shoot!)", 
        on_click=shoot, 
        use_container_width=True, 
        type="primary",
        disabled=is_shoot_disabled
    )

# 재장전 버튼
with col_reload:
    # 탄약이 가득 차면 버튼 비활성화
    is_reload_disabled = st.session_state.ammo == MAX_AMMO
    st.button(
        "🔄 재장전 (Reload)", 
        on_click=reload, 
        use_container_width=True,
        disabled=is_reload_disabled
    )

st.markdown("---")

# 리셋 버튼
if st.button("게임 및 점수 리셋"):
    st.session_state.ammo = MAX_AMMO
    st.session_state.score = 0
    st.session_state.total_shots = 0
    st.session_state.message = "리셋되었습니다. 다시 시작하세요!"
    st.rerun()
