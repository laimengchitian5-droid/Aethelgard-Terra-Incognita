import streamlit as st
import time

# 自作モジュールのインポート
from evaluator import run_advanced_analysis, QUESTIONS_30
from constellation import draw_hologram
from synapse import get_ai_analysis

# --- 1. デザイン適用 ---
st.set_page_config(page_title="Aethelgard OS", layout="centered")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ffff; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; border: 1px solid #00ffff; background-color: rgba(0,255,255,0.1); color: #00ffff; }
    h1, h2, h3 { text-shadow: 0 0 10px #00ffff; }
</style>
""", unsafe_allow_html=True)

# --- 2. セッション初期化 ---
for key in ["step", "page", "responses", "analysis", "title_status", "ai_msg"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key in ["step", "page"] else ({} if key == "responses" else None)
if st.session_state.title_status is None: st.session_state.title_status = "none"

# --- 3. メインロジック ---
if st.session_state.step == 0:
    st.title("🛰️ Aethelgard-OS 起動")
    st.subheader("精神解析プロトコル：Terra-Incognita")
    if st.button("解析プロトコル：Standard(30) 承認"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    q_all = QUESTIONS_30
    curr = st.session_state.page
    start, end = curr * 10, min((curr + 1) * 10, len(q_all))
    
    st.write(f"### 📥 同期フェーズ {curr + 1} / 3")
    st.progress((curr + 1) / 3)
    
    for i in range(start, end):
        st.markdown(f"**Q{i+1}: {q_all[i]}**")
        st.session_state.responses[i+1] = st.select_slider(
            "選択", options=[1, 2, 3, 4, 5],
            format_func=lambda x: {1:"否", 2:"", 3:"中", 4:"", 5:"然"}.get(x),
            key=f"q_{i}", label_visibility="collapsed"
        )
    
    if st.button("次のフェーズへ" if end < len(q_all) else "最終解析実行"):
        if end < len(q_all):
            st.session_state.page += 1
        else:
            with st.spinner("テンセグリティ構築中..."):
                st.session_state.analysis = run_advanced_analysis(st.session_state.responses)
                st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.title("📊 解析結果")
    res = st.session_state.analysis
    st.plotly_chart(draw_hologram(res, is_mobile=True), use_container_width=True)
    
    if not st.session_state.ai_msg:
        with st.spinner("AI解析中..."):
            st.session_state.ai_msg = get_ai_analysis(res, st.session_state.title_status)
    
    st.chat_message("assistant").write(st.session_state.ai_msg)
    
    if st.session_state.title_status == "none":
        st.write("---")
        st.markdown("### 🎖️ 称号を受領しますか？")
        c1, c2 = st.columns(2)
        if c1.button("受領"): st.session_state.title_status = "accepted"; st.rerun()
        if c2.button("拒絶"): st.session_state.title_status = "rejected"; st.rerun()
