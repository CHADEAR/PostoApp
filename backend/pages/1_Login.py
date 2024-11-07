import streamlit as st
import pyrebase

def change_colors():
    style = """
        <style>
            #login {
                color: #333366;
            }
            input[type="email"], input[type="password"] {
                color: #333366;
            }
            .st-emotion-cache-uef7qa {
                color: #333366;
            }
            .stTextInput > div > div > input {
                background-color: #FCFAEE;
            }
            label {
                color: #333366;
                font-weight: bold;
            }
            .stButton>button {
                background-color: #f9e75e;
                color: #333366;
            }
            .stButton>button:hover {
                background-color: #f9e75e;
            }
            footer {
                visibility: hidden;
            }
            #MainMenu {
                visibility: hidden;
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

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
    change_colors()
    st.sidebar.title("Login")

    if "login_status" not in st.session_state:
        st.session_state.login_status = None

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.login_status = "success"
        except:
            st.sidebar.error("Login ไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง.")
            st.session_state.current_page = "Sign Up"
            st.switch_page("pages/2_SignUp.py")

    if st.session_state.login_status == "success":
        st.sidebar.success("Login สำเร็จ!")
        st.session_state.current_page = "home"
        st.switch_page("pages/4_Chatbot.py")

    if st.sidebar.button("Login admin"):
        if email == allowed_email and password == allowed_password:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.email = email
                st.session_state.login_status = "success"
            except:
                st.sidebar.error("Login ไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง.")
        else:
            st.sidebar.error("Email หรือ Password ไม่ถูกต้อง.")

    if st.session_state.login_status == "success":
        st.sidebar.success("Login สำเร็จ!")
        st.session_state.current_page = "Admin"
        st.switch_page("pages/3_Admin.py")

if __name__ == "__main__":
    login()
