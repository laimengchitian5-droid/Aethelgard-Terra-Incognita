import streamlit as st
from groq import Groq

def generate_response(prompt, history):
    # SecretsからAPIキーを呼び出し
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # Aethelgard専用のシステムプロンプト（性格付け）
    system_prompt = {
        "role": "system", 
        "content": "あなたは未踏の地を開拓するOS『Aethelgard』の核、Synapseです。知的で、少し神秘的な開拓者の口調で話してください。"
    }
    
    messages = [system_prompt] + history
    
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=messages,
        temperature=0.7
    )
    return completion.choices[0].message.content
