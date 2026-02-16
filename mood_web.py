import streamlit as st
import os
from datetime import datetime

# 1. Page Config & Style
st.set_page_config(page_title="Mood Barometer", page_icon="✨")

st.markdown("""
    <style>
    :root { --primary-color: #82C91E; }
    .stButton > button[kind="primary"] { background-color: #82C91E !important; color: white !important; border: none; }
    </style>
""", unsafe_allow_html=True)

# 2. State Initialization
if 'selected_cat' not in st.session_state: st.session_state.selected_cat = None
if 'story_text' not in st.session_state: st.session_state.story_text = ""
if 'location_val' not in st.session_state: st.session_state.location_val = ""

# --- 3. Navigation Menu ---
st.sidebar.title("📌 Menu")
page = st.sidebar.radio("Go to:", ["Log Mood", "View History"])

# --- 4. Page: Log Mood ---
if page == "Log Mood":
    st.title("✨ Mood Barometer")
    st.write("Capture your moment with time and location.")
    st.write("---")

    # Input Fields
    mood_icons = ["☀️ Warmth", "🎁 Surprise", "🤣 Hilarious", "😊 Pleasant", "📚 Growth", 
                  "🥀 Disappointed", "☁️ Low", "🔥 Angry", "💢 Frustrated", "🆘 Helpless"]
    mood = st.selectbox("1. Select Mood Icon", mood_icons)
    
    # Location Field
    location = st.text_input("2. Location 📍", value=st.session_state.location_val, placeholder="Where are you?")
    
    # Story Input
    story = st.text_area("3. Your Story", value=st.session_state.story_text, placeholder="What's happening?", height=150)

    # Category Selection
    st.write("4. Select Category")
    col_h, col_s = st.columns(2)

    h_type = "primary" if st.session_state.selected_cat == "HAPPY" else "secondary"
    if col_h.button("HAPPY", type=h_type, use_container_width=True):
        st.session_state.selected_cat = "HAPPY"
        st.rerun()

    s_type = "primary" if st.session_state.selected_cat == "SAD" else "secondary"
    if col_s.button("SAD", type=s_type, use_container_width=True):
        st.session_state.selected_cat = "SAD"
        st.rerun()

    # Save Button
    st.write("---")
    if st.button("🪄 Archive & Save", use_container_width=True, type="primary"):
        if st.session_state.selected_cat and story.strip():
            # 自动生成当前时间
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            loc_display = location if location.strip() else "Unknown Location"
            
            # 存档格式：[时间] 地点 | 图标 | 内容
            log_entry = f"[{time_str}] @{loc_display} | {mood} | {story.strip()}\n"
            
            # Save to file
            file_name = f"{st.session_state.selected_cat.lower()}_history.txt"
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(log_entry)
            
            # Reset fields
            st.session_state.selected_cat = None
            st.session_state.story_text = "" 
            st.session_state.location_val = ""
            st.balloons()
            st.success("Saved successfully! Jiangjiang is awesome! ✨")
            st.rerun()
        else:
            st.error("Please select a category and write your story.")

# --- 5. Page: View History ---
elif page == "View History":
    st.title("📖 History Archive")
    st.write("Browse your past records by time and place.")
    
    tab_h, tab_s = st.tabs(["😊 HAPPY Records", "☁️ SAD Records"])

    def show_history(file_path, key_prefix):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for i, line in enumerate(reversed(lines)):
                    c1, c2 = st.columns([0.85, 0.15])
                    c1.text(line.strip())
                    if c2.button("🗑️", key=f"{key_prefix}_{i}"):
                        real_idx = len(lines) - 1 - i
                        lines.pop(real_idx)
                        with open(file_path, "w", encoding="utf-8") as fw:
                            fw.writelines(lines)
                        st.rerun()
        else:
            st.info("No records found.")

    with tab_h: show_history("happy_history.txt", "h_view")
    with tab_s: show_history("sad_history.txt", "s_view")
