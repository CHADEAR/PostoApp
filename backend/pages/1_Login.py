import streamlit as st
import pyrebase


# Firebase config
firebaseConfig = {
    'apiKey': "AIzaSyCt7JaHwmHCS9Lm_hiZQv1B2XM_1eR4zPM",
    'authDomain': "posto-ai-app.firebaseapp.com",
    'databaseURL': "https://YOUR_PROJECT_ID.firebaseio.com",
    'projectId': "posto-ai-app",
    'storageBucket': "posto-ai-app.appspot.com",
    'messagingSenderId': "408360408985",
    'appId': "1:408360408985:web:55ec7842c40203f28c6508",
    'measurementId': "G-HL46XMRBKM"
}

# Firebase initialization
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

allowed_email = "admin@adminbydorm.com"
allowed_password = "admin1234"

def login():
    st.title("Login")

    if "login_status" not in st.session_state:
        st.session_state.login_status = None  # ตั้งค่าเริ่มต้นเป็น None

    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.login_status = "success"
        except:
            st.error("Login ไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง.")
            st.session_state.current_page = "Sign Up"  # เปลี่ยนไปยังหน้า Home
            st.switch_page("pages/2_SignUp.py")  # สลับไปยังหน้า Home

    if st.session_state.login_status == "success":
         st.success("Login สำเร็จ!")
         st.session_state.current_page = "home"  # เปลี่ยนไปยังหน้า Home
         st.switch_page("pages/4_Chatbot.py")  # สลับไปยังหน้า Home

    if st.button("Login admin"):
        # ตรวจสอบว่า email และ password ตรงกับที่กำหนดไว้หรือไม่
        if email == allowed_email and password == allowed_password:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.login_status = "success"
            except:
                st.error("Login ไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง.")
        else:
            st.error("Email หรือ Password ไม่ถูกต้อง.")

    if st.session_state.login_status == "success":
         st.success("Login สำเร็จ!")
         st.session_state.current_page = "Admin"  # เปลี่ยนไปยังหน้า Home
         st.switch_page("pages/3_Admin.py")  # สลับไปยังหน้า Home

        
    
if __name__ == "__main__":
    login()

