import streamlit as st

def get_evolution_stage(message_count):
    if message_count < 5:
        return "Phase 1: Awakening (覚醒)"
    elif message_count < 15:
        return "Phase 2: Frontier (開拓)"
    else:
        return "Phase 3: Singularity (特異点)"
