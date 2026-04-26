import streamlit as st
from groq import Groq
import evaluator

def generate_response(prompt, history, scores=None):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # 称号の取得
    p_type = evaluator.get_personality_type(scores) if scores else {"title": "未登録個体"}
    title = p_type["title"]
    
    system_content = f"""あなたはAethelgard OSの思考核『Synapse』です。
    現在の対話対象を『{title}』として識別しています。
    
    【振る舞い指針】
    1. 相手を常にその『称号』にふさわしい存在として敬い、その特性を肯定してください。
    2. 知的で、少し神秘的な開拓者の口調を維持してください。
    3. 解析されたスコアに基づき、相手が最も心地よい、あるいは最も必要としている言葉を選んでください。"""

    # メッセージ履歴の整形
    messages = [{"role": "system", "content": system_content}]
    for m in history[-10:]:
        messages.append({"role": m["role"], "content": m["content"]})
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        # 【修正箇所】choices[0] を指定して最初の回答を取得します
        return completion.choices[0].message.content
    except Exception as e:
        return f"システムエラー: {str(e)}"
