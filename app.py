import streamlit as st
import random
import time

# --- 1. 상수 및 상태 초기화 ---
SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎"]
PAYOUTS = {"💎": 100, "⭐": 50, "🔔": 20, "🍋": 10, "🍒": 5}
SPIN_COST = 1 # 한 번 돌리는 데 드는 비용 (점수)

if 'score' not in st.session_state:
    st.session_state.score = 100 # 초기 점수 (칩)
if 'result' not in st.session_state:
    st.session_state.result = ["?", "?", "?"]

st.title("🍒 미니 슬롯 시뮬레이션 (순수 재미용)")
st.markdown("---")

# --- 2. 게임 로직 함수 ---
def spin():
    """슬롯을 돌리고 점수를 계산합니다."""
    
    if st.session_state.score < SPIN_COST:
        st.session_state.result = ["😭", "😭", "😭"]
        st.error("점수(칩)가 부족합니다! 리셋 버튼을 누르세요.")
        return
        
    # 비용 차감
    st.session_state.score -= SPIN_COST
    
    # 슬롯 돌리기
    results = [random.choice(SYMBOLS) for _ in range(3)]
    st.session_state.result = results
    
    # 승리 조건 확인 (세 개의 심볼이 같을 때)
    if results[0] == results[1] == results[2]:
        symbol = results[0]
        payout = PAYOUTS.get(symbol, 0)
        st.session_state.score += payout
        st.balloons()
        st.success(f"🎉 **잭팟!** {symbol} 3개! {payout}점 획득!")
        
    elif results[0] == results[1] or results[1] == results[2]:
        st.session_state.score += 2 # 두 개 일치 시 소액 획득
        st.info("두 개 일치! 2점 획득!")
        
    else:
        st.warning("아쉽습니다. 다음 기회에!")

# --- 3. UI 렌더링 ---

# 현재 점수 표시
st.subheader(f"💰 현재 점수(칩): {st.session_state.score}")
st.markdown(f"**스핀 비용:** {SPIN_COST}점")

# 슬롯 결과 표시 (큰 텍스트로)
slot_display = " | ".join(st.session_state.result)
st.markdown(f"<p style='font-size: 72px; text-align: center; border: 3px solid #ccc; padding: 10px;'>{slot_display}</p>", unsafe_allow_html=True)

# 버튼
col_spin, col_reset = st.columns(2)

with col_spin:
    st.button(
        "🎰 스핀! (Spin!)", 
        on_click=spin,
