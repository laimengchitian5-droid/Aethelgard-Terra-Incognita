import streamlit as st
from groq import Groq
import interface, synapse, database, constellation

# 1. ページ基本設定
st.set_page_config(page_title="Aethelgard OS", layout="wide")

# 2. セキュリティ：SecretsからAPIキーを取得
# CloudのSettings > Secretsに「GROQ_API_KEY」として保存する前提
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. セッション（記憶）の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. サイドバー：既存の3Dマップを表示
with st.sidebar:
    st.title("🛡️ System Monitor")
    constellation.draw_3d_map() # 既存の3D描画関数を呼び出し

# 5. メインUI：チャット履歴の表示
st.title("Aethelgard OS")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 入力処理
if prompt := st.chat_input("指令を入力してください..."):
    # ユーザー入力を保存・表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの応答生成（ストリーミング形式）
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # synapse.pyからシステムプロンプト等を取得する形に連結可能
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        
        for chunk in completion:
            if chunk.choices.delta.content:
                full_response += chunk.choices.delta.content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    # 履歴保存とログ記録
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    database.save_log(prompt, full_response) # 既存のログ保存関数を呼び出し
