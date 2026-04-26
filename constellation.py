import plotly.graph_objects as go

def draw_hologram(data, is_mobile=True):
    f = data["facets"]
    p = data["physics"]
    cat = list(f.keys())
    val = list(f.values())
    
    # 物理量に基づくカラー判定
    color = "rgba(0, 255, 255, 0.8)"
    if p['S'] > 12:
        color = "rgba(255, 50, 50, 0.9)"
    elif p['V'] > 40:
        color = "rgba(230, 230, 255, 1.0)"

    # チャート作成
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=val + [val[0]],
        theta=cat + [cat[0]],
        fill='toself',
        line=dict(color=color, width=3),
        fillcolor=color.replace('0.8','0.2').replace('1.0','0.3')
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="black",
            radialaxis=dict(visible=True, range=[1, 5], gridcolor="rgba(255,255,255,0.1)")
        ),
        paper_bgcolor="black",
        showlegend=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height=450 if is_mobile else 600
    )
    return fig
