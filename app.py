import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from io import BytesIO

# --- 1. 앱 제목 설정 ---
st.title("🎧 실시간 소리 스펙트로그램 분석기")
st.markdown("---")

# --- 2. 오디오 입력 위젯 (마이크 녹음) ---
# st.audio_input을 사용하여 사용자의 마이크로부터 오디오를 녹음합니다.
recorded_audio = st.audio_input(
    "🎙️ 실생활의 소리를 녹음하세요:",
    sample_rate=44100,  # 높은 품질의 오디오를 위해 샘플링 속도(Hz)를 높입니다.
    key="audio_recorder"
)

if recorded_audio is not None:
    st.success("✅ 오디오 녹음 완료! 분석을 시작합니다.")
    
    # 녹음된 오디오 데이터를 처리하는 과정
    try:
        # 3. 오디오 데이터를 NumPy 배열로 변환
        # Streamlit의 BytesIO 객체를 librosa로 로드하기 위해 사용
        audio_data, sr = librosa.load(
            BytesIO(recorded_audio.read()), 
            sr=None  # 원본 샘플링 속도 사용
        )
        
        # 4. 푸리에 변환 (FFT)을 통한 스펙트로그램 계산
        # N_FFT는 주파수 해상도를, HOP_LENGTH는 시간 해상도를 결정합니다.
        N_FFT = 2048  # FFT 창 크기 (정밀도)
        HOP_LENGTH = 512 # 겹치는 간격 (시간 부드러움)
        
        # S는 푸리에 변환된 주파수 진폭 (스펙트로그램)
        S = librosa.stft(audio_data, n_fft=N_FFT, hop_length=HOP_LENGTH)
        # 진폭을 데시벨(dB) 단위로 변환
        S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        
        # 5. 스펙트로그램 시각화 (matplotlib 사용)
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # librosa.display를 사용해 정교한 스펙트로그램을 그립니다.
        img = librosa.display.specshow(S_dB, 
                                       sr=sr, 
                                       hop_length=HOP_LENGTH, 
                                       x_axis='time', 
                                       y_axis='log', # 주파수 축을 로그 스케일로 (소리 분석에 유리)
                                       ax=ax)
        
        ax.set_title('정교한 스펙트로그램 (주파수 분석)', fontsize=14)
        ax.set_xlabel("시간 (Time)")
        ax.set_ylabel("주파수 (Frequency, Hz)")
        fig.colorbar(img, ax=ax, format='%+2.0f dB', label='진폭 (Amplitude)')
        plt.tight_layout()
        
        # 6. Streamlit에 그래프 표시
        st.pyplot(fig)
        st.caption(f"샘플링 속도: {sr} Hz, 총 길이: {audio_data.shape[0]/sr:.2f} 초")
        
    except Exception as e:
        st.error(f"오디오 처리 중 오류 발생: {e}")

st.markdown("---")
st.info("스펙트로그램은 소리의 **시간-주파수-진폭**을 동시에 보여주는 그래프입니다. 따뜻한 색일수록 해당 시간에 그 주파수의 소리가 크다는 것을 의미합니다.")
