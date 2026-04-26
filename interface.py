import streamlit as st

def init_style():
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        .stChatMessage { border-radius: 15px; border: 1px solid #1e3a8a; }
        .stMetric { background-color: #161b22; padding: 10px; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

def sidebar_content():
    st.sidebar.title("🌌 Aethelgard Menu")
    st.sidebar.info("Terra Incognita Protocol Active")
