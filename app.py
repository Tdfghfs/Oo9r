import streamlit as st
import requests
import importlib.util
import os

# --- إعدادات الواجهة (مظهر احترافي تقني) ---
st.set_page_config(page_title="Terminal System v4", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #58a6ff; font-family: 'Courier New', monospace; }
    .stChatInput { border-top: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام جلب المحرك من الرابط المباشر ---
# سيدي: ضع هنا رابط الـ Raw الخاص بملفك على GitHub
CORE_LINK = "https://raw.githubusercontent.com/USER/REPO/main/core_logic.py"

def initialize_core():
    try:
        response = requests.get(CORE_LINK)
        if response.status_code == 200:
            with open("core_logic.py", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            spec = importlib.util.spec_from_file_location("core_logic", "core_logic.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return None
    except:
        return None

# --- لوحة التحكم ---
st.title("🛡️ System Terminal Core")
st.write("Auth: **Authenticated** | Source: **Remote GitHub**")

if "core" not in st.session_state:
    if st.button("Initialize System Connection"):
        with st.spinner("Connecting to remote source..."):
            core_module = initialize_core()
            if core_module:
                st.session_state.core = core_module
                st.success("System Ready.")
                st.rerun()
            else:
                st.error("Connection Failed. Check Core Link.")

# --- تشغيل المحرك بعد الربط ---
if "core" in st.session_state:
    # استدعاء الدالة الرئيسية من ملفك في GitHub
    # تأكد أن ملفك في GitHub يحتوي على دالة باسم main_execution()
    st.session_state.core.main_execution()
