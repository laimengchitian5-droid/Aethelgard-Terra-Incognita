import plotly.graph_objects as go

def draw_hologram(analysis_data, is_mobile=True):
    f = analysis_data["facets"]
    p = analysis_data["physics"]
    
    # 物理量に基づく発光演出
    glow = "rgba(0, 255, 255, 0.8)"
    if p['S'] > 12: glow = "rgba(255, 50, 50, 0.9)" # 葛藤・赤
    elif p['V'] > 40: glow = "rgba(230, 230, 255, 1.0)" # 極光・白

    fig = go.Figure(data=[go.Scatterpolar(
        r=list(f.values()) + [list(f.values())[0]],
        theta=list(f.keys()) + [list(f.keys())[0]],
        fill='toself',
        line=dict(color=glow, width=3),
        fillcolor=glow.replace('0.8','0.2').replace('1.0','0.3')
    )])

    fig.update_layout(
        polar=dict(
            bgcolor="black",
            radialaxis=dict(visible=True, range=[1, 5], gridcolor="rgba(0,255,255,0.1)")
        ),
        paper_bgcolor="black",
        height=450 if is_mobile else 650,
        showlegend=False
    )
    return fig
