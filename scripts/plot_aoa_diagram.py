import plotly.graph_objects as go
import networkx as nx

def plot_aoa_network(G, critical_path):
    # Use kamada_kawai layout for better node spacing
    pos = nx.kamada_kawai_layout(G)
    
    # Identify critical edges
    crit_edges = set(zip(critical_path[:-1], critical_path[1:])) if len(critical_path) > 1 else set()

    # Create figure
    fig = go.Figure()
    
    # Add edges with styling
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        is_critical = (u, v) in crit_edges
        
        # Edge line
        fig.add_trace(go.Scatter(
            x=[x0, x1, None], 
            y=[y0, y1, None],
            mode='lines',
            line=dict(
                color='#FF5252' if is_critical else '#757575',
                width=4 if is_critical else 2,
                dash='solid' if is_critical else 'dot'
            ),
            hoverinfo='none'
        ))
        
        # Arrow head
        fig.add_annotation(
            x=x1,
            y=y1,
            ax=x0,
            ay=y0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='#FF5252' if is_critical else '#757575'
        )
        
        # Activity label (above edge)
        activity = G.edges[u, v].get('Activity_id', f"{u}→{v}")
        fig.add_annotation(
            x=(x0+x1)/2,
            y=(y0+y1)/2 + 0.03,
            text=f"<b>{activity}</b>",
            showarrow=False,
            font=dict(size=12, color='#212121'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.5)',
            borderwidth=1
        )
        
        # Duration label (below edge)
        te = G.edges[u, v].get('TE', 0)
        fig.add_annotation(
            x=(x0+x1)/2,
            y=(y0+y1)/2 - 0.03,
            text=f"<i>TE: {te:.1f}</i>",
            showarrow=False,
            font=dict(size=10, color='#424242'),
            bgcolor='rgba(255,255,255,0.6)'
        )

    # Add nodes with styling
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=50,
            color='#82B1FF',
            line=dict(width=2, color='#2962FF')
        ),
        text=[str(i+1) for i in range(len(G.nodes()))],
        textposition="middle center",
        hoverinfo='none',
        textfont=dict(size=14, color='#0D47A1')
    ))

    # Layout configuration
    fig.update_layout(
        title='<b>Activity-on-Arrow Network Diagram</b>',
        titlefont=dict(size=20, color='#263238'),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode='closest'
    )
    
    return fig