import streamlit as st
from groq import Groq

def generate_response(prompt, history):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    system_prompt = {
        "role": "system", 
        "content": "あなたは未踏の地を開拓するOS『Aethelgard』の核、Synapseです。知的で、少し神秘的な開拓者の口調で話してください。"
    }
    
    formatted_history = [
        {"role": m["role"], "content": m["content"]} 
        for m in history[-10:] 
        if "role" in m and "content" in m
    ]
    
    messages = [system_prompt] + formatted_history
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        # 【修正箇所】choicesの最初の要素[0]を指定して取得します
        return completion.choices[0].message.content
    except Exception as e:
        return f"システムエラー: {str(e)}"
