import streamlit as st
import random

def show_status():
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Core Stability", f"{random.randint(95, 99)}%", "0.2%")
    with col2:
        st.metric("Synapse Load", f"{random.randint(20, 40)}%", "-5%")
