import streamlit as st

# ตั้งค่าหน้าเริ่มต้นของ Streamlit
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# ตรวจสอบว่าเป็นหน้า login หรือไม่
if st.session_state.current_page == "login":
    ShowSidebarNavigation = False

def main():
    # เพิ่มข้อความยินดีต้อนรับและรูปตรงกลางหน้าจอ
    if st.session_state.current_page == "home":
        # สร้างคอลัมน์เพื่อจัดตำแหน่งตรงกลาง
        col1, col2, col3 = st.columns([1, 2, 1])  # คอลัมน์ที่สองจะใหญ่กว่าเพื่อวางข้อความและรูป

        with col2:
            st.header("ยินดีต้อนรับสู่แอปพลิเคชั่น POSTO")  # ข้อความต้อนรับ
            st.image("backend/2.png", caption="Welcome Image", use_column_width=True)  # ใส่รูปภาพ

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
