import streamlit as st
import requests
from datetime import datetime
import os

# 页面基本设置
st.set_page_config(page_title="蒋蒋的心情晴雨表 Web", page_icon="✨")

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

if 'selected_cat' not in st.session_state:
    st.session_state.selected_cat = None

if col_h.button("HAPPY", type="primary" if st.session_state.selected_cat=="HAPPY" else "secondary", use_container_width=True):
    st.session_state.selected_cat = "HAPPY"
if col_s.button("SAD", type="primary" if st.session_state.selected_cat=="SAD" else "secondary", use_container_width=True):
    st.session_state.selected_cat = "SAD"

st.write("---")

# 存档按钮
if st.button("🪄 Archive & Save", use_container_width=True):
    if st.session_state.selected_cat and story.strip():
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log = f"[{time_str}] @{location} | {mood} | {story}\n"
        
        file_name = "happy_history.txt" if st.session_state.selected_cat == "HAPPY" else "sad_history.txt"
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(log)
        
        st.balloons()
        st.toast("存档成功！蒋蒋真棒 ✨")
        
        # 自动清空
        st.session_state.loc = ""
        st.session_state.selected_cat = None
        st.rerun()
    else:
        st.error("请确保选择了分类并填写了故事内容哦！")

# 底部查看历史
st.write("### 📖 查看历史记录")
tab1, tab2 = st.tabs(["😊 HAPPY View", "☁️ SAD View"])
with tab1:
    if os.path.exists("happy_history.txt"):
        with open("happy_history.txt", "r", encoding="utf-8") as f:
            st.text(f.read())
with tab2:
    if os.path.exists("sad_history.txt"):
        with open("sad_history.txt", "r", encoding="utf-8") as f:
            st.text(f.read())