import streamlit as st
import os
import pandas as pd
from model import read_name_from_image, crop_and_read_names, save_to_csv, count_names_in_csv

def change_colors():
    style = """
        <style>
            #upload-parcel-image {
                color: #333366;
            }
            .st-emotion-cache-bm2z3a {
                background-color: #f0f0f0;
            }
            .st-emotion-cache-h4xjwg, .st-emotion-cache-1dp5vir {
                background-color: #ff5f5f;
            }
            .stText {
                color: #333366;
            }
            .st-emotion-cache-1erivf3, .st-emotion-cache-15hul6a {
                background-color: #333366;
            }
            .stButton>button {
                background-color: #f9e75e;
                color: #333366;
            }
            .stButton>button:hover {
                background-color: #f9e75e;
            }
            .st-emotion-cache-12fmjuu {
                background-color: #FF5F5F;
                color: white;
            }
            .st-emotion-cache-1vt4y43 {
                background-color: #C4D7FF;
            }
            .logout-button {
                position: fixed;
                top: 50px;
                right: 10px;
                background-color: #f9e75e;
                color: #333366;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                z-index: 1000;
            }
            .logout-button:hover {
                background-color: #f0c75e;
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def check_login():
    if "login_status" not in st.session_state or not st.session_state.login_status:
        st.warning("กรุณา Login ก่อนเข้าหน้าอื่น")
        st.session_state.current_page = "Login"
        st.switch_page("pages/1_Login.py")

    if "email" not in st.session_state or st.session_state.email != "admin@adminbydorm.com":
        st.warning("คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        st.stop()

def logout():
    if "login_status" in st.session_state:
        st.session_state.login_status = False
    if "email" in st.session_state:
        st.session_state.email = None
    st.success("Logout สำเร็จ!")
    st.session_state.current_page = "login"
    st.switch_page("pages/1_Login.py")
    st.experimental_rerun()

# สร้างโฟลเดอร์สำหรับอัปโหลดถ้าไม่มี
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_FILE = 'backend/names.csv'

def Admin():
    change_colors()
    check_login()
    st.title("Upload Parcel Image")
    uploaded_file = st.file_uploader("Select Files", type=['jpg', 'png'])
        
    if uploaded_file is not None:
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        detected_names, boxes = read_name_from_image(image_path)
    
        if detected_names:
            cropped_names = crop_and_read_names(image_path, boxes)
            save_to_csv(cropped_names)
            st.write("Detected Names: ", ", ".join(detected_names))
            st.write("Cropped Names: ", ", ".join(cropped_names))
            st.write("Name Counts: ", count_names_in_csv().to_dict(orient='records'))
        else:
            st.warning("ไม่พบชื่อในภาพ")
    
    # ปุ่ม Logout ที่มุมขวาบน
    st.markdown(
        '<button class="logout-button" onclick="window.location.href=\'pages/1_Login.py\'">Logout</button>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    Admin()
