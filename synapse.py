# synapse.py
import streamlit as st
from groq import Groq

def generate_response(prompt, history, scores=None):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # 性格スコアに基づいたシステムプロンプトの動的生成
    if scores:
        summary = ", ".join([f"{k}:{v:.1f}" for k, v in scores.items()])
        system_content = f"""あなたはAethelgard OSです。
        利用者のBFI-2診断結果（{summary}）に基づき、相手の性格に最も適した開拓者として振る舞ってください。
        スコアが高い特性を尊重し、低い特性を補うような、知的で神秘的な対話を行ってください。"""
    else:
        system_content = "あなたはAethelgard OSです。まだ利用者の解析が完了していません。解析を促すような丁寧な口調で話してください。"

    messages = [{"role": "system", "content": system_content}]
    for m in history[-10:]:
        messages.append({"role": m["role"], "content": m["content"]})
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    return completion.choices.message.content
