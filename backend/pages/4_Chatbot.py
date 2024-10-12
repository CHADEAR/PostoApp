import streamlit as st
import pandas as pd
from streamlit_chat import message
import os

def check_login():
    if "login_status" not in st.session_state or not st.session_state.login_status:
        st.warning("กรุณา Login ก่อนเข้าหน้าอื่น")
        st.session_state.current_page = "Login"
        st.switch_page("pages/1_Login.py")

# กำหนดค่าเริ่มต้นสำหรับ messages
st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

# สร้างโฟลเดอร์สำหรับอัปโหลดถ้าไม่มี
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_FILE = 'backend/names.csv'

def chat():
    check_login()

    # ใช้ CSS สำหรับ fix text input ให้ติดอยู่ที่ด้านล่างของหน้าจอ
    st.markdown(
        """
        <style>
        .body{
            padding:0;
            margin:0;
            box-sizing: border-box;
            width:100%;
            height:100%;
        }
        .stTextInput {
            position: fixed;
            bottom: 0;
            width: 70%;
            margin-bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <nav style="width:100%; background-color:#FF5F5F; height:10vh; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 24px;">POST</span>
        </nav>
        """,
        unsafe_allow_html=True
    )

    # ฟังก์ชันสำหรับการตรวจสอบคำถามใน CSV
    def check_question_in_csv(question):
        try:
            df = pd.read_csv(CSV_FILE)
            return question in df['name'].values
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ CSV: {e}")
            return False
    
    # ฟังก์ชันที่จัดการคำถาม
    def handle_chat(question):
        if question:
            if check_question_in_csv(question):
                return f"✅ คำถาม '{question}' ถูกพบใน CSV."
            else:
                return f"❌ คำถาม '{question}' ไม่ถูกพบใน CSV."
        return "🚫 กรุณาถามคำถามที่ถูกต้อง."
    
    # ฟังก์ชันสำหรับการส่งข้อความ
    def on_input_change():
        user_input = st.session_state.user_input
        if user_input:
            st.session_state.past.append(user_input)
            answer = handle_chat(user_input)
            st.session_state.generated.append(answer)
            st.session_state.user_input = ""

    # ตรวจสอบการตั้งค่า session_state
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    # แสดงข้อความใน container
    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"user_{i}")
            message(st.session_state['generated'][i], key=f"bot_{i}")

    # ช่องป้อนข้อความ
    st.text_input("ถามคำถามของคุณที่นี่:", on_change=on_input_change, key="user_input")

if __name__ == "__main__":
    chat()
