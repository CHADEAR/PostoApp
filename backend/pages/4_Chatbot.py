import streamlit as st
import pandas as pd
from streamlit_chat import message
import os

def check_login():
    if "login_status" not in st.session_state or not st.session_state.login_status:
        st.warning("กรุณา Login ก่อนเข้าหน้าอื่น")
        st.session_state.current_page = "Login"
        st.switch_page("pages/1_Login.py")

def logout():
    if "login_status" in st.session_state:
        st.session_state.login_status = False
    if "email" in st.session_state:
        st.session_state.email = None  # ลบอีเมลออกจาก session
    st.success("Logout สำเร็จ!")
    st.session_state.current_page = "login"  # เปลี่ยนไปที่หน้า Login
    st.switch_page("pages/1_Login.py")  # สลับไปยังหน้า Home
    st.experimental_rerun()  # รีเฟรชหน้า

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_FILE = 'backend/names.csv'

def check_question_in_csv(question):
    try:
        df = pd.read_csv(CSV_FILE)
        if question in df['name'].values:
            return df[df['name'] == question]['count'].values[0]
        else:
            return 0
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ CSV: {e}")
        return 0

def handle_chat(question):
    if question:
        count = check_question_in_csv(question)
        if count > 0:
            return f"✅ พัสดุของ {question} มาถึงแล้วครับ (จำนวนพัสดุ: {count} ชิ้น)"
        else:
            return f"❌ พัสดุของ {question} ยังไม่มาถึงครับ"
    return "🚫 กรุณาใส่ชื่อผู้รับพัสดุ"

def on_input_change():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.past.append(user_input)
        answer = handle_chat(user_input)
        st.session_state.generated.append(answer)
        st.session_state.user_input = ""

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

# เรียกฟังก์ชัน check_login ก่อนเข้า chat
check_login()

# ฟังก์ชันหลักสำหรับการแสดง chatbot
def chat():
    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"user_{i}")
            message(st.session_state['generated'][i], key=f"bot_{i}")

    st.text_input("ใส่ชื่อผู้รับพัสดุ :", on_change=on_input_change, key="user_input")

if st.button("Logout"):
    logout()

if __name__ == "__main__":
    chat()
