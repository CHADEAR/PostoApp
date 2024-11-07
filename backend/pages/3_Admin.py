import streamlit as st

# ตั้งค่าหน้าเริ่มต้นของ Streamlit
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# ตรวจสอบว่าเป็นหน้า login หรือไม่
if st.session_state.current_page == "login":
    ShowSidebarNavigation = False

# ฟังก์ชันเพื่อปรับตำแหน่งปุ่มให้อยู่มุมขวาบน
def position_buttons():
    st.markdown(
        """
        <style>
        /* CSS สำหรับจัดตำแหน่งปุ่มให้อยู่มุมขวาบน */
        .top-right-button-container {
            position: fixed;
            top: 10px;
            right: 10px;
            display: flex;
            gap: 10px;
            z-index: 999;
        }
        </style>
        <div class="top-right-button-container">
            <form action="/pages/1_Login.py">
                <button type="submit">Login</button>
            </form>
            <form action="/pages/2_SignUp.py">
                <button type="submit">Sign Up</button>
            </form>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    # เรียกฟังก์ชันเพื่อแสดงปุ่มให้อยู่มุมขวาบน
    position_buttons()
    
    # ตรวจสอบสถานะของ current_page และเรียก switch_page ตามหน้า
    if st.session_state.current_page == "login":
        st.switch_page("pages/1_Login.py")  # ไปที่หน้า Login
    elif st.session_state.current_page == "sign_up":
        st.switch_page("pages/2_SignUp.py")  # ไปที่หน้า Sign Up
    elif st.session_state.current_page == "chat":
        st.switch_page("pages/4_Chatbot.py")  # ไปที่หน้า Chatbot
    elif st.session_state.current_page == "admin":
        st.switch_page("pages/3_Admin.py")  # ไปที่หน้า Admin

if __name__ == "__main__":
    main()
