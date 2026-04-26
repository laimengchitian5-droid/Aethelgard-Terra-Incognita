import streamlit as st
import time

# 自作モジュールのインポート
from evaluator import run_advanced_analysis, QUESTIONS_30
from constellation import draw_hologram
from synapse import get_ai_analysis

# --- 1. システム設定・デザイン適用 ---
st.set_page_config(page_title="Aethelgard OS", layout="centered", initial_sidebar_state="collapsed")

# サイバーパンクCSS
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ffff; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; border: 1px solid #00ffff; background-color: rgba(0,255,255,0.1); color: #00ffff; border-radius: 0; transition: 0.3s; }
    .stButton>button:hover { background-color: #00ffff; color: #000; box-shadow: 0 0 15px #00ffff; }
    h1, h2, h3 { text-shadow: 0 0 10px #00ffff; }
    .stProgress > div > div > div { background-color: #00ffff; }
</style>
""", unsafe_allow_html=True)

# --- 2. セッション状態の初期化 ---
if "step" not in st.session_state:
    st.session_state.update({
        "step": 0,          # 0:起動, 1:診断, 2:解析結果, 3:対話モード
        "page": 0,          # 診断のページ(10問ずつ)
        "responses": {},    # 回答データ
        "analysis": None,   # 演算結果
        "title_status": "none", # none, accepted, rejected
        "ai_msg": None
    })

# --- 3. フェーズ：OS起動・プロトコル選択 ---
if st.session_state.step == 0:
    st.title("🛰️ Aethelgard-OS")
    st.write("---")
    st.subheader("精神解析プロトコル：Terra-Incognita")
    st.info("警告：このOSは、あなたの深層心理を物理構造として再構築します。")
    
    # 質問数は現在Standard(30)に固定（拡張可能）
    if st.button("解析プロトコル：Standard(30) 承認"):
        st.session_state.step = 1
        st.rerun()

# --- 4. フェーズ：多段階診断インターフェース ---
elif st.session_state.step == 1:
    q_all = QUESTIONS_30
    total_q = len(q_all)
    current_page = st.session_state.page
    start_idx = current_page * 10
    end_idx = min(start_idx + 10, total_q)
    
    st.write(f"### 📥 データ同期フェーズ {current_page + 1} / {total_q // 10}")
    st.progress((current_page + 1) / (total_q // 10))
    
    for i in range(start_idx, end_idx):
        st.markdown(f"**Q{i+1}: {q_all[i]}**")
        st.session_state.responses[i+1] = st.select_slider(
            "選択肢", options=[1, 2, 3, 4, 5], 
            labels={1: "否", 3: "中", 5: "然"},
            key=f"q_slider_{i}", label_visibility="collapsed"
        )
        st.write("") # スペース

    # ナビゲーション
    if st.button("次のデータ層へ" if end_idx < total_q else "最終解析・テンセグリティ構築"):
        if end_idx < total_q:
            st.session_state.page += 1
            st.rerun()
        else:
            with st.spinner("精神波形を物理構造に変換中..."):
                # 解析実行
                st.session_state.analysis = run_advanced_analysis(st.session_state.responses)
                time.sleep(2) # 演出
                st.session_state.step = 2
                st.rerun()

# --- 5. フェーズ：解析結果 ＆ 称号受領 ---
elif st.session_state.step == 2:
    st.title("📊 解析完了：精神位相構造")
    res = st.session_state.analysis
    
    # ホログラム描画
    fig = draw_hologram(res, is_mobile=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # 物理パラメータ表示
    p = res["physics"]
    st.write(f"**構造ストレス:** {p['S']:.2f} | **精神容積:** {p['V']:.2f} | **レジリエンス:** {p['I']:.2f}")

    # AI解析テキストの取得
    if not st.session_state.ai_msg:
        with st.chat_message("assistant"):
            msg = get_ai_analysis(res, st.session_state.title_status)
            st.write(msg)
            st.session_state.ai_msg = msg
    else:
        st.chat_message("assistant").write(st.session_state.ai_msg)

    # 称号プロトコル
    if st.session_state.title_status == "none":
        st.write("---")
        st.markdown("### 🎖️ 提示された称号をプロファイルに刻みますか？")
        c1, c2 = st.columns(2)
        if c1.button("受領：称号を承認"):
            st.session_state.title_status = "accepted"
            st.success("称号が承認されました。以後、OSはこの名であなたを認識します。")
            time.sleep(1)
            st.rerun()
        if c2.button("拒絶：名もなき者として進む"):
            st.session_state.title_status = "rejected"
            st.warning("定義を拒絶しました。あなたは不確定のまま観測を続けます。")
            time.sleep(1)
            st.rerun()
    else:
        if st.button("対話ターミナルを継続"):
            st.info("これより先は、記録された称号を元に対話を深めます。")
