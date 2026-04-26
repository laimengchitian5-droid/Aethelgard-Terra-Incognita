import streamlit as st
import time

# 自作モジュール
from evaluator import run_advanced_analysis, QUESTIONS_30
from constellation import draw_hologram
from synapse import get_ai_analysis

st.set_page_config(page_title="Aethelgard OS", layout="centered")

# CSS
st.markdown("<style>.stApp{background-color:#050505;color:#00ffff;}</style>", unsafe_allow_html=True)

# セッション初期化
if "step" not in st.session_state:
    st.session_state.update({"step": 0, "page": 0, "responses": {}, "analysis": None, "title_status": "none", "ai_msg": None})

# メイン処理
if st.session_state.step == 0:
    st.title("🛰️ Aethelgard-OS")
    if st.button("プロトコル：Standard(30) 承認"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    q_all = QUESTIONS_30
    curr = st.session_state.page
    start, end = curr * 10, min((curr + 1) * 10, len(q_all))
    
    st.write(f"### フェーズ {curr + 1} / 3")
    for i in range(start, end):
        st.markdown(f"**Q{i+1}: {q_all[i]}**")
        st.session_state.responses[i+1] = st.select_slider(
            "回答", options=[1, 2, 3, 4, 5],
            format_func=lambda x: {1:"否", 3:"中", 5:"然"}.get(x, ""),
            key=f"q_{i}", label_visibility="collapsed"
        )
    
    if st.button("次へ" if end < len(q_all) else "解析実行"):
        if end < len(q_all):
            st.session_state.page += 1
        else:
            st.session_state.analysis = run_advanced_analysis(st.session_state.responses)
            st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.title("📊 解析完了")
    res = st.session_state.analysis
    st.plotly_chart(draw_hologram(res, is_mobile=True), use_container_width=True)
    
    if not st.session_state.ai_msg:
        with st.spinner("AI解析中..."):
            st.session_state.ai_msg = get_ai_analysis(res, st.session_state.title_status)
    
    st.chat_message("assistant").write(st.session_state.ai_msg)
    
    if st.session_state.title_status == "none":
        c1, c2 = st.columns(2)
        if c1.button("称号受領"): st.session_state.title_status = "accepted"; st.rerun()
        if c2.button("拒絶"): st.session_state.title_status = "rejected"; st.rerun()
