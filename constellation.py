import plotly.graph_objects as go
import numpy as np
import streamlit as st

def draw_3d_map():
    # ランダムな星系（ノード）を生成
    n_nodes = 15
    x = np.random.standard_normal(n_nodes)
    y = np.random.standard_normal(n_nodes)
    z = np.random.standard_normal(n_nodes)

    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+lines',
        marker=dict(size=4, color='cyan', opacity=0.8),
        line=dict(color='white', width=1)
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
