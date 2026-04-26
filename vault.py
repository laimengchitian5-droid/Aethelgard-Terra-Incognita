import streamlit as st

def get_secret(key_name):
    # Streamlit CloudのSecretsから安全に取得
    try:
        return st.secrets[key_name]
    except:
        st.error(f"Secret '{key_name}' が設定されていません。")
        return None
