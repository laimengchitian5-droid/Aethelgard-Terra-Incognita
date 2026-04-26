# main.py
import streamlit as st
import interface, synapse, database, constellation, evaluator, env_setup
import plotly.express as px
import pandas as pd

env_setup.check_env()
interface.init_style()

if "messages" not in st.session_state: st.session_state.messages = []
if "aligned" not in st.session_state: st.session_state.aligned = False

# --- サイドバー ---
with st.sidebar:
    st.title("🛡️ Aethelgard")
    if st.session_state.aligned:
        # レーダーチャートの表示
        scores = st.session_state.scores
        df = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
        if st.button("再診断を行う"):
            st.session_state.aligned = False
            st.rerun()
    else:
        st.info("精神解析プロトコル未完了")

# --- メインコンテンツ ---
if not st.session_state.aligned:
    st.title("🌌 Core Alignment Protocol (BFI-2-S)")
    st.write("Aethelgard OSをあなたの精神に同調させます。30の質問に回答してください。")
    
    # 質問リスト（一部抜粋。実際は30問分記述）
    responses = {}
    questions = [
        "1. 社交的で、活発なほうだ", "2. 静かで、口数が少ないほうだ", 
        "3. 活気にあふれ、他人を惹きつける", "4. 恥ずかしがり屋で、控えめなほうだ",
        # ... 本来はここに30問分並べる
    ]
    
    for i in range(1, 31):
        responses[f"Q{i}"] = st.radio(f"項目 {i}", [1,2,3,4,5], index=2, horizontal=True, key=f"q_{i}")
        st.divider()

    if st.button("プロトコル実行（診断完了）"):
        st.session_state.scores = evaluator.calculate_bfi2_scores(responses)
        st.session_state.aligned = True
        st.rerun()

else:
    # 通常のチャット画面
    st.title("🛡️ Aethelgard OS")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("指令を入力..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # スコアを渡して応答生成
            res = synapse.generate_response(prompt, st.session_state.messages, st.session_state.scores)
            st.markdown(res)
        
        st.session_state.messages.append({"role": "assistant", "content": res})
        database.save_log(prompt, res)
