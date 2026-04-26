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
    
    # 【修正ポイント】historyから "role" と "content" だけを抽出して整形
    # これにより、Streamlit特有の余計なデータが混ざるのを防ぎます
    formatted_history = [
        {"role": m["role"], "content": m["content"]} 
        for m in history 
        if "role" in m and "content" in m
    ]
    
    messages = [system_prompt] + formatted_history
    
    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0.7
        )
        return completion.choices.message.content
    except Exception as e:
        return f"通信エラーが発生しました: {str(e)}"
