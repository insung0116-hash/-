# app.py

import streamlit as st
import qrcode
from PIL import Image
import io # 데이터를 메모리 버퍼에 저장하기 위해 임포트

# --- 페이지 설정 ---
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="🔗"
)

# --- 제목 및 설명 ---
st.title("🔗 나만의 QR 코드 생성기")
st.write("아래 입력창에 URL이나 텍스트를 입력하면 QR 코드가 생성됩니다.")

# --- 1. 사용자 입력 ---
# st.text_input은 텍스트 입력창을 만듭니다.
default_value = "https://www.google.com"
text_input = st.text_input(
    "QR 코드로 만들 URL이나 텍스트를 입력하세요:",
    default_value
)

# --- 2. QR 코드 생성 로직 ---
# st.button("버튼")을 누르면 'if'문 안의 코드가 실행됩니다.
if st.button("QR 코드 생성하기"):
    if not text_input.strip():
        # 입력값이 비어있을 경우 에러 메시지
        st.error("⚠️ 내용을 입력해주세요!")
    else:
        try:
            # QR 코드 생성
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text_input)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # --- 3. 이미지 표시 및 다운로드 ---
            
            # 이미지를 파일로 저장하지 않고, 메모리(BytesIO)에 바로 저장합니다.
            # 웹 앱에서는 파일을 직접 저장하는 것보다 이 방식이 훨씬 효율적입니다.
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.success("✅ QR 코드가 성공적으로 생성되었습니다!")
            
            # st.image()로 웹페이지에 이미지 표시
            st.image(byte_im, caption="생성된 QR 코드")

            # st.download_button()으로 다운로드 버튼 생성
            st.download_button(
                label="QR 코드 다운로드 (PNG)",
                data=byte_im,
                file_name="my_qrcode.png", # 다운로드될 파일 이름
                mime="image/png" # 파일 타입
            )
        
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
