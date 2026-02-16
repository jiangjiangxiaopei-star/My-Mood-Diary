import streamlit as st
import os

# 1. 基础配置
st.set_page_config(page_title="Mood Barometer", page_icon="✨")

# 统一绿色样式
st.markdown("""
    <style>
    :root { --primary-color: #82C91E; }
    .stButton > button[kind="primary"] { background-color: #82C91E !important; color: white !important; border: none; }
    </style>
""", unsafe_allow_html=True)

# 2. 初始化状态 (用于存档后自动清空)
if 'selected_cat' not in st.session_state: st.session_state.selected_cat = None
if 'story_text' not in st.session_state: st.session_state.story_text = ""

st.title("✨ Mood Barometer ✨")

# --- 输入区 ---
mood_icons = ["☀️ Warmth", "🎁 Surprise", "🤣 Hilarious", "😊 Pleasant", "📚 Growth"]
mood = st.selectbox("1. Mood Icon", mood_icons)
story = st.text_area("2. Story", value=st.session_state.story_text, placeholder="Tell your story...")

# --- 3. Category (选中变绿) ---
st.write("3. Category")
col_h, col_s = st.columns(2)

h_type = "primary" if st.session_state.selected_cat == "HAPPY" else "secondary"
if col_h.button("HAPPY", type=h_type, use_container_width=True):
    st.session_state.selected_cat = "HAPPY"
    st.rerun()

s_type = "primary" if st.session_state.selected_cat == "SAD" else "secondary"
if col_s.button("SAD", type=s_type, use_container_width=True):
    st.session_state.selected_cat = "SAD"
    st.rerun()

# --- 保存逻辑 ---
if st.button("🪄 Archive & Save", use_container_width=True, type="primary"):
    if st.session_state.selected_cat and story.strip():
        # 存档后重置界面
        st.session_state.story_text = ""
        st.session_state.selected_cat = None
        st.balloons()
        st.rerun()
