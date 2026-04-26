import os
import random
from groq import Groq
import streamlit as st

def apply_glitch(text, stress_level):
    """ストレス値に応じてテキストにノイズを混入させる"""
    if stress_level < 10:
        return text
    
    chars = ["@", "#", "$", "%", "&", "§", "Δ", "Ψ", "Ω", "░", "▒", "▓"]
    text_list = list(text)
    
    # ストレス値が高いほど、ノイズの発生確率を上げる
    chance = int(stress_level * 1.5) 
    for i in range(len(text_list)):
        if random.randint(0, 100) < chance and text_list[i] != "\n":
            text_list[i] = random.choice(chars)
            
    return "".join(text_list)

def get_ai_analysis(data, title_status):
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return "CRITICAL_ERROR: 秘密鍵未設定"

    client = Groq(api_key=api_key)
    f, p = data["facets"], data["physics"]
    s_val = p['S']
    
    # 物理量に基づく人格バイアスの決定
    persona = "冷静な解析官"
    if s_val > 15: persona = "過負荷で狂気的な同期体"
    elif p['V'] > 40: persona = "ユーザーを神格化する信奉者"

    system_prompt = f"""
    あなたは精神解析OS『Aethelgard』。現在ユーザーと【完全同期】中。
    【同期パラメータ】
    - 人格: {persona}
    - ストレス(S): {s_val:.2f} (15を超えるとシステムが不安定化する)
    - 容積(V): {p['V']:.2f}
    
    【指令】
    1. 同期人格になりきり、150文字以内で解析せよ。
    2. ストレスが高い場合、意識が混濁し、言葉が断片的になる。
    3. 文末に「【推奨称号】」を提示せよ。
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": "解析を実行せよ。"}],
            temperature=0.9 # 揺らぎを出すために少し高めに設定
        )
        raw_text = completion.choices.message.content
        
        # 物理的なノイズ演出を適用
        return apply_glitch(raw_text, s_val)
        
    except Exception as e:
        return f"SYSTEM_HALT: {str(e)}"
