import streamlit as st
import interface, synapse, database, constellation, evaluator, env_setup
import plotly.express as px
import pandas as pd

env_setup.check_env()
interface.init_style()

if "messages" not in st.session_state: st.session_state.messages = []
if "aligned" not in st.session_state: st.session_state.aligned = False

# --- サイドバー ---
with st.sidebar:
    st.title("🛡️ Aethelgard")
    if st.session_state.aligned:
        scores = st.session_state.scores
        df = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", polar=dict(radialaxis=dict(visible=True, range=[1, 5])))
        st.plotly_chart(fig, use_container_width=True)
        if st.button("再診断を行う"):
            st.session_state.aligned = False
            st.rerun()
    else:
        st.info("精神解析プロトコル未完了")

# --- メインコンテンツ ---
if not st.session_state.aligned:
    st.title("🌌 Core Alignment Protocol (BFI-2-S)")
    st.caption("Aethelgard OSをあなたの精神に同調させます。")
    st.write("以下の30の項目について、あなた自身にどの程度当てはまるか回答してください。")
    st.info("1: 全く当てはまらない ～ 5: 非常に当てはまる")

    # BFI-2-S 全30問の定義
    questions = [
        "1. 社交的で、活発なほうだ", "2. 静かで、口数が少ないほうだ(※)", "3. 活気にあふれ、他人を惹きつける",
        "4. 恥ずかしがり屋で、控えめなほうだ(※)", "5. 支配的で、他人に影響力を行使するほうだ", "6. 自分の意見をあまり主張しないほうだ(※)",
        "7. 他人に対して、思いやりや慈しみを感じる", "8. 他人のあら探しをする傾向がある(※)", "9. ほとんど誰に対しても、礼儀正しく親切だ",
        "10. 他人に対して、冷淡で無関心なところがある(※)", "11. 他人を疑うよりも、まず信頼するほうだ", "12. 相手を馬鹿にしたり、失礼な態度を取ることがある(※)",
        "13. 物事を効率よく、手際よく進めることができる", "14. かなり怠惰（なまけ者）なところがある(※)", "15. 責任感があり、常に信頼される",
        "16. 計画性がなく、整理整頓が苦手だ(※)", "17. 最後までやり遂げる、粘り強さがある", "18. 注意力が散漫で、うっかりミスをしやすい(※)",
        "19. 不安になりやすく、心配性だ", "20. リラックスしていて、ストレスをうまく扱える(※)", "21. 気分が沈みやすく、憂うつになることがある",
        "22. 情緒が安定していて、あまり動揺しない(※)", "23. ストレスを感じると、パニックになりやすい", "24. 多少の困難があっても、自信を保てる(※)",
        "25. 美術や音楽、文学に強い関心がある", "26. 知的好奇心が強く、複雑なことを考えるのが好きだ", "27. 創造性が豊かで、新しいアイデアを思いつく",
        "28. 抽象的な思考（理論的なこと）にはあまり興味がない(※)", "29. 想像力が豊かで、空想にふけることがある", "30. 芸術的なことや文化的なことには無関心だ(※)"
    ]

    responses = {}
    
    # セクション分けして表示（UX向上）
    for i, q in enumerate(questions):
        responses[f"Q{i+1}"] = st.select_slider(q, options=[1, 2, 3, 4, 5], value=3, key=f"bfi_{i}")

    st.divider()
    if st.button("プロトコル実行（診断完了）", type="primary"):
        with st.spinner("精神構造を解析中..."):
            st.session_state.scores = evaluator.calculate_bfi2_scores(responses)
            st.session_state.aligned = True
            st.rerun()

else:
    # チャット画面（以前と同じ）
    st.title("🛡️ Aethelgard OS")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("指令を入力..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            res = synapse.generate_response(prompt, st.session_state.messages, st.session_state.scores)
            st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
        database.save_log(prompt, res)
