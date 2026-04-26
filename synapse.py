import streamlit as st
from groq import Groq

def generate_response(prompt, history):
    # SecretsからAPIキーを呼び出し
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # Aethelgard専用のシステムプロンプト
    system_prompt = {
        "role": "system", 
        "content": "あなたは未踏の地を開拓するOS『Aethelgard』の核、Synapseです。知的で、少し神秘的な開拓者の口調で話してください。"
    }
    
    # メッセージ履歴の整形（最新の10件に絞り、負荷を軽減）
    formatted_history = [
        {"role": m["role"], "content": m["content"]} 
        for m in history[-10:] 
        if "role" in m and "content" in m
    ]
    
    messages = [system_prompt] + formatted_history
    
    try:
        completion = client.chat.completions.create(
            # 【重要修正】廃止されたmixtralから最新のllama-3.3へ変更
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        return completion.choices.message.content
    except Exception as e:
        # エラー詳細を表示してデバッグしやすくする
        return f"通信エラーが発生しました（モデル設定を確認してください）: {str(e)}"
