import streamlit as st
import os
from datetime import datetime

# 1. 基础配置与样式
st.set_page_config(page_title="Mood Barometer", page_icon="✨")

st.markdown("""
    <style>
    :root { --primary-color: #82C91E; }
    .stButton > button[kind="primary"] { background-color: #82C91E !important; color: white !important; border: none; }
    </style>
""", unsafe_allow_html=True)

# 2. 初始化状态
if 'selected_cat' not in st.session_state: st.session_state.selected_cat = None
if 'story_text' not in st.session_state: st.session_state.story_text = ""

# --- 3. 【左侧侧边栏】：专门放历史记录 ---
with st.sidebar:
    st.title("📖 History Archive")
    st.write("点击下方标签查看历史")
    tab_h, tab_s = st.tabs(["😊 HAPPY", "☁️ SAD"])

    def show_history(file_path, key_prefix):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for i, line in enumerate(reversed(lines)):
                    # 侧边栏空间有限，我们把删除按钮放下面
                    st.text(line.strip())
                    if st.button("🗑️ Delete", key=f"{key_prefix}_{i}"):
                        real_idx = len(lines) - 1 - i
                        lines.pop(real_idx)
                        with open(file_path, "w", encoding="utf-8") as fw:
                            fw.writelines(lines)
                        st.rerun()
                    st.write("---")
        else:
            st.info("No records yet.")

    with tab_h: show_history("happy_history.txt", "h")
    with tab_s: show_history("sad_history.txt", "s")

# --- 4. 【主界面】：专注记录心情 ---
st.title("✨ Mood Barometer ✨")
st.write("记录结束后，历史记录会自动同步到左侧抽屉。")
st.write("---")

# 输入区
mood_icons = ["☀️ Warmth", "🎁 Surprise", "🤣 Hilarious", "😊 Pleasant", "📚 Growth", 
              "🥀 Disappointed", "☁️ Low", "🔥 Angry", "💢 Frustrated", "🆘 Helpless"]
mood = st.selectbox("1. Mood Icon", mood_icons)
story = st.text_area("2. Story", value=st.session_state.story_text, placeholder="记录这一刻...", height=150)

# 分类按钮 (选中变绿)
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

# 存档按钮
st.write("---")
if st.button("🪄 Archive & Save", use_container_width=True, type="primary"):
    if st.session_state.selected_cat and story.strip():
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"[{time_str}] {mood} | {story.strip()}\n"
        
        file_name = f"{st.session_state.selected_cat.lower()}_history.txt"
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        # 清空
        st.session_state.story_text = ""
        st.session_state.selected_cat = None
        st.balloons()
        st.rerun()
    else:
        st.error("请先写点什么并选择 HAPPY 或 SAD 哦！")
