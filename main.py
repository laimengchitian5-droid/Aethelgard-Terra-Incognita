import streamlit as st
import interface, synapse, database, constellation, evaluator, env_setup
import pandas as pd

# 1. システム初期化
env_setup.check_env()
interface.init_style()

# 2. セッション状態の管理
if "messages" not in st.session_state: st.session_state.messages = []
if "aligned" not in st.session_state: st.session_state.aligned = False

# --- サイドバー構成 ---
with st.sidebar:
    st.title("🛡️ Aethelgard")
    
    if st.session_state.aligned:
        # 称号のサイバーパンク表示 (手順3の統合)
        p_type = evaluator.get_personality_type(st.session_state.scores)
        st.markdown(f"""
            <div style="padding:15px; border-radius:10px; border:1px solid #00d4ff; 
                        background:rgba(0,212,255,0.1); text-align:center; margin-bottom:20px;
                        box-shadow: 0 0 15px rgba(0,212,255,0.2);">
                <span style="color:#00d4ff; font-size:0.7rem; letter-spacing:2px;">USER IDENTIFIED AS</span><br>
                <span style="color:white; font-size:1.1rem; font-weight:bold;">{p_type['title']}</span>
            </div>
        """, unsafe_allow_html=True)

        # ホログラム・レーダーチャートの表示
        fig = constellation.draw_hologram_radar(st.session_state.scores)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # 解析ステータス
        with st.expander("📝 Analysis Detail"):
            st.write(p_type['desc'])
            st.divider()
            col1, col2 = st.columns(2)
            with col1: st.metric("Sync", "98.2%")
            with col2: st.metric("Core", "Stable")
        
        st.divider()
        if st.button("🔄 再解析プロトコル"):
            st.session_state.aligned = False
            st.rerun()
    else:
        st.info("精神解析プロトコル：未完了")
        constellation.draw_3d_map()

# --- メインコンテンツ ---
if not st.session_state.aligned:
    st.title("🌌 Core Alignment Protocol (BFI-2-S)")
    st.caption("Aethelgard OS：精神構造のデジタル・アラインメントを実行します。")
    st.info("各項目について、自分にどの程度当てはまるか選択してください。")

    # BFI-2-S 全30問
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
    for i, q in enumerate(questions):
        responses[f"Q{i+1}"] = st.select_slider(q, options=[1, 2, 3, 4, 5], value=3, key=f"bfi_{i}")

    if st.button("プロトコル実行（診断完了）", type="primary"):
        with st.spinner("精神構造を走査中..."):
            st.session_state.scores = evaluator.calculate_bfi2_scores(responses)
            st.session_state.aligned = True
            st.rerun()

else:
    # --- チャットインターフェース ---
    st.title("🛡️ Aethelgard OS")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("指令を入力..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 称号を考慮した応答生成
            res = synapse.generate_response(prompt, st.session_state.messages, st.session_state.scores)
            st.markdown(res)
        
        st.session_state.messages.append({"role": "assistant", "content": res})
        database.save_log(prompt, res)
