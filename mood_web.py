import streamlit as st
import requests
from datetime import datetime
import os

# 页面基本设置
st.set_page_config(page_title="蒋蒋的心情晴雨表 Web", page_icon="✨")
st.markdown("""
    <style>
    /* 蒋蒋专属：统一将 primary 颜色定义为护眼绿色 */
    :root {
        --primary-color: #82C91E;
    }
    .stButton > button[kind="primary"] {
        background-color: #82C91E;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)
# 自定义绿色按钮样式
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #E0E0E0; color: black; border: none; }
    div.stButton > button:active { background-color: #82C91E !important; color: white !important; }
    .st-emotion-cache-19rxjzo { background-color: #82C91E !important; color: white !important; } /* 选中后的绿色 */
    </style>
""", unsafe_allow_html=True)

def get_location():
    try:
        res = requests.get("http://ip-api.com/json/?lang=zh-CN", timeout=2).json()
        return res.get('city', '广州')
    except: return "Guangzhou"

st.title("✨ Mood Barometer Web ✨")
st.write("---")

# 1. 心情图标
mood_icons = ["☀️ Warmth", "🎁 Surprise", "🤣 Hilarious", "😊 Pleasant", "📚 Growth", 
              "🥀 Disappointed", "☁️ Low", "🔥 Angry", "💢 Frustrated", "🆘 Helpless"]
mood = st.selectbox("1. Mood Icon", mood_icons)

# 2. 地点
if 'loc' not in st.session_state:
    st.session_state.loc = get_location()
location = st.text_input("2. Location 📍", value=st.session_state.loc)

# 3. 故事
story = st.text_area("3. Story", placeholder="Tell your story...", height=150)

# 4. 分类选择 (统一绿色方案)
st.write("4. Category")
col_h, col_s = st.columns(2)

# --- 4. Category 分类区域 ---
st.write("4. Category")
col_h, col_s = st.columns(2)

# 初始化选中状态
if 'selected_cat' not in st.session_state:
    st.session_state.selected_cat = None

# HAPPY 按钮逻辑：如果选中了就用 primary（绿色），没选中就用 secondary（灰色）
h_type = "primary" if st.session_state.web_selected_cat == "HAPPY" else "secondary"
if col_h.button("HAPPY", type=h_type, use_container_width=True):
    st.session_state.web_selected_cat = "HAPPY"
    st.rerun() # 立即刷新让颜色生效

# SAD 按钮逻辑
s_type = "primary" if st.session_state.web_selected_cat == "SAD" else "secondary"
if col_s.button("SAD", type=s_type, use_container_width=True):
    st.session_state.web_selected_cat = "SAD"
    st.rerun()

# 存档按钮
if st.button("🪄 Archive & Save", use_container_width=True):
    if st.session_state.selected_cat and story.strip():
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log = f"[{time_str}] @{location} | {mood} | {story}\n"
        
        file_name = "happy_history.txt" if st.session_state.selected_cat == "HAPPY" else "sad_history.txt"
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(log)
        
        st.balloons()
        st.toast("存档成功！蒋蒋�