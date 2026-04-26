import streamlit as st
from evaluator import run_advanced_analysis
from constellation import draw_hologram
from synapse import get_ai_response

# 1. セッション初期化
if "step" not in st.session_state: st.session_state.update({"step": 0, "responses": {}, "title_status": "none"})

# 2. プロトコル選択画面
if st.session_state.step == 0:
    st.title("🛰️ Aethelgard OS 起動")
    mode = st.select_slider("解析精度を選択", options=["Lite (15問)", "Standard (30問)", "Full (60問)"])
    if st.button("プロトコルをロード"):
        st.session_state.q_count = 15 if "Lite" in mode else (30 if "Standard" in mode else 60)
        st.session_state.step = 1
        st.rerun()

# 3. 10問ずつページ切り替え診断
elif st.session_state.step == 1:
    # 10問表示・回答収集ロジック
    # (回答が完了したら st.session_state.step = 2 へ)
    pass

# 4. 最終解析・ホログラム・称号選択
elif st.session_state.step == 2:
    results = run_advanced_analysis(st.session_state.responses, st.session_state.q_count)
    st.plotly_chart(draw_hologram(results))
    
    msg = get_ai_response(results, st.session_state.title_status)
    st.chat_message("assistant").write(msg)
    
    # 称号選択UI
    if st.session_state.title_status == "none":
        c1, c2 = st.columns(2)
        if c1.button("称号を刻む"): 
            st.session_state.title_status = "accepted"; st.rerun()
        if c2.button("定義を拒絶する"): 
            st.session_state.title_status = "rejected"; st.rerun()
