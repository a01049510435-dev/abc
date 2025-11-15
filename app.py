import streamlit as st
import random

# 1. 정답 숫자 설정
# st.session_state를 사용하여 앱을 새로고침해도 정답이 유지되도록 합니다.
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 10)
    st.session_state.guess_made = False

st.title("🤫 1부터 10 사이 숫자 맞히기 게임")
st.write("랜덤으로 선택된 숫자를 맞춰보세요!")

# 2. 사용자로부터 숫자 입력 받기
guess = st.number_input(
    "당신의 예상 숫자를 입력하세요 (1~10):",
    min_value=1,
    max_value=10,
    step=1,
    key='guess_input'
)

# 3. '정답 확인' 버튼
if st.button("정답 확인"):
    st.session_state.guess_made = True
    
    # 4. 정답 비교 및 결과 표시
    if guess == st.session_state.secret_number:
        st.success("🎉 축하합니다! 정답입니다! 🎉")
        st.balloons() # 정답일 때 풍선 효과
        # 새 게임을 위해 정답을 변경합니다.
        st.session_state.secret_number = random.randint(1, 10) 
        st.session_state.guess_made = False
        
    elif guess < st.session_state.secret_number:
        st.warning(f"👆 틀렸습니다. 정답은 {guess}보다 **더 큰** 숫자입니다.")
        
    else: # guess > st.session_state.secret_number
        st.warning(f"👇 틀렸습니다. 정답은 {guess}보다 **더 작은** 숫자입니다.")

# 게임을 다시 시작하고 싶을 때 버튼을 눌러 정답을 바꿀 수 있습니다.
if st.button("새 게임 시작"):
    st.session_state.secret_number = random.randint(1, 10)
    st.session_state.guess_made = False
    st.info("새로운 비밀 숫자가 설정되었습니다. 다시 시작하세요!")
