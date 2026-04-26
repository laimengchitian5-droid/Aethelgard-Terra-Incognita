import plotly.graph_objects as go
import numpy as np
import streamlit as st

# 旧：3D星系マップ（サイドバー用）
def draw_3d_map():
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
        plot_bgcolor='rgba(0,0,0,0)',
        height=200
    )
    st.plotly_chart(fig, use_container_width=True)

# 新：次世代ホログラム・レーダーチャート
def draw_hologram_radar(scores):
    categories = list(scores.keys())
    values = list(scores.values())
    
    # 閉じた多角形にするため、最初の要素を最後に追加
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    # 1. メインのレーザーライン（主骨格）
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(0, 212, 255, 0.15)',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8, color='#fff', symbol='diamond'),
        name='Aethelgard Core'
    ))

    # 2. 中心コア（パルス演出）
    fig.add_trace(go.Scatterpolar(
        r=[0], theta=[categories[0]],
        marker=dict(size=18, color='rgba(0, 212, 255, 0.8)', symbol='circle'),
        hoverinfo='none'
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True, range=[0, 5],
                gridcolor='rgba(0, 212, 255, 0.1)',
                linecolor='rgba(0, 212, 255, 0.2)',
                tickfont=dict(color='#00d4ff', size=9)
            ),
            angularaxis=dict(
                gridcolor='rgba(0, 212, 255, 0.2)',
                linecolor='rgba(0, 212, 255, 0.5)',
                tickfont=dict(color='#e0f7ff', size=11)
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=35, r=35, t=35, b=35),
        height=350
    )
    return fig
