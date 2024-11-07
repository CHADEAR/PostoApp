import streamlit as st
import pandas as pd
from streamlit_chat import message
import os

# ตรวจสอบสถานะ login
def check_login():
    if "login_status" not in st.session_state or not st.session_state.login_status:
        st.warning("กรุณา Login ก่อนเข้าหน้าอื่น")
        st.session_state.current_page = "Login"
        st.switch_page("pages/1_Login.py")

# กำหนดค่าเริ่มต้นสำหรับ messages
st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

# ฟังก์ชัน logout
def logout():
    if "login_status" in st.session_state:
        st.session_state.login_status = False
    if "email" in st.session_state:
        st.session_state.email = None  # ลบอีเมลออกจาก session
    st.success("Logout สำเร็จ!")
    st.session_state.current_page = "login"  # เปลี่ยนไปที่หน้า Login
    st.switch_page("pages/1_Login.py")  # สลับไปยังหน้า Home
    st.experimental_rerun()  # รีเฟรชหน้า

# สร้างโฟลเดอร์สำหรับอัปโหลดถ้าไม่มี
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_FILE = 'backend/names.csv'

# ฟังก์ชันตรวจสอบคำถามใน CSV
def check_question_in_csv(question):
    try:
        df = pd.read_csv(CSV_FILE)
        # ตรวจสอบชื่อในคอลัมน์ 'name' ว่ามีชื่อผู้รับพัสดุหรือไม่
        if question in df['name'].values:
            return df[df['name'] == question]['count'].values[0]  # คืนค่าจำนวนพัสดุที่มี
        else:
            return 0  # หากไม่พบชื่อใน CSV
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ CSV: {e}")
        return 0

# ฟังก์ชันที่จัดการคำถาม
def handle_chat(question):
    if question:
        count = check_question_in_csv(question)
        if count > 0:
            return f"✅ พัสดุของ {question} มาถึงแล้วครับ (จำนวนพัสดุ: {count} ชิ้น)"
        else:
            return f"❌ พัสดุของ {question} ยังไม่มาถึงครับ"
    return "🚫 กรุณาใส่ชื่อผู้รับพัสดุ"

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

# ส่วนที่แสดงข้อความ
with chat_placeholder.container():
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=f"user_{i}")
        message(st.session_state['generated'][i], key=f"bot_{i}")

# ช่องป้อนข้อความ
st.text_input("ใส่ชื่อผู้รับพัสดุ :", on_change=on_input_change, key="user_input")

# ฟังก์ชัน logout
if st.button("Logout"):
    logout()  # เรียกฟังก์ชัน logout

if __name__ == "__main__":
    check_login()  # ตรวจสอบสถานะการ login
    chat()  # เรียกใช้งานฟังก์ชัน chatbot
