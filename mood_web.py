import streamlit as st
import os
from datetime import datetime

# 1. 页面配置与 UI 深度优化
st.set_page_config(page_title="Mood Barometer", page_icon="✨", layout="centered")

# --- 自定义 CSS 样式 ---
st.markdown("""
    <style>
    /* 1. 整体背景与字体 */
    .stApp { background-color: #FDFDFD; }
    h1 { color: #2C3E50; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    
    /* 2. 输入框美化 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        border-radius: 12px !important;
        border: 1px solid #E0E0E0 !important;
        background-color: white !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    /* 3. 按钮美化：蒋蒋专属绿 */
    div.stButton > button {
        border-radius: 15px !important;
        height: 3em !important;
        transition: all 0.3s ease;
        border: none !important;
    }
    
    /* 选中状态的绿色按钮 (Primary) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #82C91E 0%, #69A316 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(130, 201, 30, 0.3) !important;
    }
    
    /* 普通灰色按钮 (Secondary) */
    div.stButton > button[kind="secondary"] {
        background-color: #F1F3F5 !important;
        color: #495057 !important;
    }

    /* 4. 侧边栏美化 */
    .stSidebar { background-color: #F8F9FA !important; border-right: 1px solid #E9ECEF; }
    
    /* 5. 隐藏多余组件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. 初始化状态
if 'selected_cat' not in st.session_state: st.session_state.selected_cat = None
if 'story_text' not in st.session_state: st.session_state.story_text = ""
if 'location_val' not in st.session_state: st.session_state.location_val = ""

# --- 3. Navigation Menu (Sidebar) ---
st.sidebar.markdown("### 📌 Navigation")
page = st.sidebar.radio("Select Page:", ["✨ Log Mood", "📖 View History"])

# --- 4. Page: Log Mood ---
if page == "✨ Log Mood":
    st.title("✨ Mood Barometer")
    st.markdown("---")

    # 分栏布局让输入更紧凑
    col_input, col_empty = st.columns([2, 1])
    
    with col_input:
        mood_icons = ["☀️ Warmth", "🎁 Surprise", "🤣 Hilarious", "😊 Pleasant", "📚 Growth", 
                      "🥀 Disappointed", "☁️ Low", "🔥 Angry", "💢 Frustrated", "🆘 Helpless"]
        mood = st.selectbox("1. How are you feeling?", mood_icons)
        
        location = st.text_input("2. Location 📍", value=st.session_state.location_val, placeholder="Where are you?")
        
        story = st.text_area("3. Your Story", value=st.session_state.story_text, placeholder="Write down your thoughts...", height=150)

    # Category Selection
    st.write("4. Select Category")
    col_h, col_s = st.columns(2)

    h_type = "primary" if st.session_state.selected_cat == "HAPPY" else "secondary"
    if col_h.button("HAPPY 😊", type=h_type, use_container_width=True):
        st.session_state.selected_cat = "HAPPY"
        st.rerun()

    s_type = "primary" if st.session_state.selected_cat == "SAD" else "secondary"
    if col_s.button("SAD ☁️", type=s_type, use_container_width=True):
        st.session_state.selected_cat = "SAD"
        st.rerun()

    # Save Button
    st.write("")
    if st.button("🪄 Archive & Save", use_container_width=True, type="primary"):
        if st.session_state.selected_cat and story.strip():
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            loc_display = location if location.strip() else "Unknown"
            log_entry = f"[{time_str}] @{loc_display} | {mood} | {story.strip()}\n"
            
            file_name = f"{st.session_state.selected_cat.lower()}_history.txt"
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(log_entry)
            
            # Reset
            st.session_state.selected_cat = None
            st.session_state.story_text = "" 
            st.session_state.location_val = ""
            st.balloons()
            st.success("Successfully archived! Jiangjiang is doing great! ✨")
            st.rerun()
        else:
            st.warning("Please select a category and write something first!")

# --- 5. Page: View History ---
elif page == "📖 View History":
    st.title("📖 History Archive")
    
    tab_h, tab_s = st.tabs(["😊 HAPPY Moments", "☁️ SAD Reflections"])

    def show_history(file_path, key_prefix):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for i, line in enumerate(reversed(lines)):
                    # 使用 container 包裹每条记录，增加卡片感
                    with st.container():
                        c1, c2 = st.columns([0.9, 0.1])
                        c1.markdown(f"**{line.strip()}**")
                        if c2.button("🗑️", key=f"{key_prefix}_{i}"):
                            real_idx = len(lines) - 1 - i
                            lines.pop(real_idx)
                            with open(file_path, "w", encoding="utf-8") as fw:
                                fw.writelines(lines)
                            st.rerun()
                        st.divider()
        else:
            st.info("No records yet. Start recording your day!")

    with tab_h: show_history("happy_history.txt", "h_view")
    with tab_s: show_history("sad_history.txt", "s_view")
