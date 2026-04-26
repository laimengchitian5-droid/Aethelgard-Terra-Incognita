import streamlit as st

def init_style():
    st.markdown("""
        <style>
        /* メイン背景とテキスト */
        .stApp { background-color: #050a15; color: #e0f7ff; }
        
        /* チャット吹き出しのホログラム化 */
        .stChatMessage {
            background: rgba(0, 212, 255, 0.05);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
        }
        
        /* サイドバーのサイバー化 */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 20, 40, 0.9);
            border-right: 1px solid #00d4ff;
        }
        </style>
    """, unsafe_allow_html=True)
