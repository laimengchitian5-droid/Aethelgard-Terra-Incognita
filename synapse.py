import os
from groq import Groq
import streamlit as st

def get_ai_analysis(data, title_status):
    # APIキーの取得
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return "通信エラー: APIキーが設定されていません。秘密鍵の設定を確認してください。"

    client = Groq(api_key=api_key)
    
    f = data["facets"]
    p = data["physics"]
    
    # プロンプトの構築
    system_prompt = f"""
    あなたは精神解析OS『Aethelgard』の思考核です。
    以下のテレメトリに基づき、ユーザーの魂を解析せよ。
    
    【テレメトリ】
    - 物理量: ストレス={p['S']:.2f}, 容積={p['V']:.2f}, 慣性={p['I']:.2f}
    - 15項目詳細: {f}
    
    【制約】
    1. 言語は日本語、サイバーパンクかつ詩的なトーン。
    2. 数値の矛盾（例：社交的だが不安が高い等）を鋭く指摘せよ。
    3. 文末に「【推奨称号】」として、この波形に相応しい二つ名を1つだけ生成せよ。
    4. 称号受領状態: {title_status}
    5. スマホで見やすいよう、適宜改行を入れること。
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": "私の精神波形を解析せよ。"}],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"解析核にエラーが発生: {str(e)}"
