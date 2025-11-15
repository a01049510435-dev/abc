import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import soundfile as sf # 오디오 파일을 읽기 위해 추가 (pip install soundfile)

# 1. 라이브러리 설치 안내
st.info("이 코드를 실행하려면 'pip install streamlit numpy matplotlib soundfile'이 필요합니다.")
st.title("🎶 간단한 소리 파형 분석기")

# 2. 오디오 입력 받기
uploaded_file = st.file_uploader("🎙️ 오디오 파일(.wav, .mp3)을 업로드하거나 녹음하세요:", type=["wav", "mp3"])

if uploaded_file is not None:
    st.success("✅ 오디오 파일 수신 완료. 파형 분석을 시작합니다.")

    try:
        # 3. 오디오 데이터 읽기 및 NumPy 배열로 변환
        # soundfile을 사용하여 파일에서 오디오 데이터와 샘플링 레이트(sr)를 읽습니다.
        audio_data, sr = sf.read(BytesIO(uploaded_file.read()))
        
        # 만약 스테레오(2채널)라면 첫 번째 채널만 사용 (파형을 단순화하기 위해)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]

        # 4. 시간 축 생성
        # 시간 축을 초 단위로 계산합니다.
        time = np.linspace(0., len(audio_data) / sr, len(audio_data))

        # 5. 파형 그래프 시각화 (matplotlib)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(time, audio_data, color='blue') # 시간 vs. 진폭(소리 크기)
        
        ax.set_title('소리 파형 (Waveform)', fontsize=14)
        ax.set_xlabel("시간 (Time, seconds)")
        ax.set_ylabel("진폭 (Amplitude)")
        ax.grid(True)
        plt.tight_layout()

        # 6. Streamlit에 그래프 표시
        st.pyplot(fig)
        st.caption(f"샘플링 속도: {sr} Hz, 총 길이: {time[-1]:.2f} 초")

    except Exception as e:
        st.error(f"오디오 처리 중 오류 발생. 지원되는 파일 형식인지 확인해주세요: {e}")
