import plotly.graph_objects as go

def draw_hologram(data, is_mobile=True):
    f, p = data["facets"], data["physics"]
    cat = list(f.keys())
    val = list(f.values())
    
    color = "rgba(0, 255, 255, 0.8)"
    if p['S'] > 12: color = "rgba(255, 50, 50, 0.9)"
    elif p['V'] > 40: color = "rgba(230, 230, 255, 1.0)"

    fig = go.Figure(go.Scatterpolar(r=val+[val], theta=cat+[cat], fill='toself', 
                                    line=dict(color=color, width=3),
                                    fillcolor=color.replace('0.8','0.2').replace('1.0','0.3')))
    fig.update_layout(polar=dict(bgcolor="black", radialaxis=dict(visible=True, range=)),
                      paper_bgcolor="black", showlegend=False, margin=dict(l=30, r=30, t=30, b=30),
                      height=450 if is_mobile else 600)
    return fig
 return fig
