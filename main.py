import streamlit as st
import interface, synapse, database, constellation, telemetry, evolver, env_setup

# 初期設定
env_setup.check_env()
interface.init_style()

# セッション状態の管理
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- サイドバー構成 ---
with st.sidebar:
    interface.sidebar_content()
    telemetry.show_status()
    st.divider()
    constellation.draw_3d_map()
    stage = evolver.get_evolution_stage(len(st.session_state.messages))
    st.write(f"Current Status: **{stage}**")

# --- メインチャット画面 ---
st.title("🛡️ Aethelgard OS")
st.caption("Terra Incognita: Exploring the uncharted digital frontier.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("指令を入力..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # synapse.pyを通じてAI応答を取得
        response = synapse.generate_response(prompt, st.session_state.messages)
        st.markdown(response)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    database.save_log(prompt, response)
