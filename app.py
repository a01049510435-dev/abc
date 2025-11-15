import streamlit as st

# 1. 상태(점수) 초기화
# 'score'가 st.session_state에 없으면 0으로 초기화합니다.
if 'score' not in st.session_state:
    st.session_state.score = 0

st.title("버튼 클릭 게임 🕹️")
st.header(f"현재 점수: **{st.session_state.score}**")

# 2. 컨트롤 함수 (클릭 시 점수 증가)
def click_button():
    """버튼이 클릭될 때 점수를 1 증가시킵니다."""
    st.session_state.score += 1
    st.balloons() # 클릭할 때마다 풍선 효과를 줍니다.

# 3. 사용자 컨트롤 위젯 (버튼)
# 버튼을 누르면 on_click에 지정된 함수가 실행됩니다.
st.button(
    "클릭하여 점수 얻기!", 
    on_click=click_button, 
    use_container_width=True,
    type="primary" # 버튼을 강조합니다.
)

st.caption("새로고침(Rerun)을 해도 점수가 유지됩니다.")
