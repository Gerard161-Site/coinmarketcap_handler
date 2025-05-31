import plotly.graph_objects as go
import pandas as pd

# Create the flowchart
fig = go.Figure()

# Define main components with proper colors and positioning
components = [
    # Main vertical flow - properly aligned
    {"name": "User", "x": 2, "y": 6, "color": "#1FB8CD", "size": 30, "shape": "circle"},
    {"name": "SQL Query", "x": 2, "y": 5.2, "color": "lightgray", "size": 25, "shape": "square"},
    {"name": "MindsDB Instance", "x": 2, "y": 4.4, "color": "#1FB8CD", "size": 35, "shape": "square"},
    {"name": "CoinMarketCap Handler", "x": 2, "y": 3.6, "color": "#ECEBD5", "size": 40, "shape": "square"},
    
    # Tables row - evenly spaced horizontally  
    {"name": "Quotes Table", "x": 0.8, "y": 2.8, "color": "#5D878F", "size": 30, "shape": "square"},
    {"name": "Listings Table", "x": 1.6, "y": 2.8, "color": "#5D878F", "size": 30, "shape": "square"},
    {"name": "Info Table", "x": 2.4, "y": 2.8, "color": "#5D878F", "size": 30, "shape": "square"},
    {"name": "Global Metrics", "x": 3.2, "y": 2.8, "color": "#5D878F", "size": 30, "shape": "square"},
    
    # API - centered below tables
    {"name": "CoinMarketCap API", "x": 2, "y": 1.8, "color": "#FFC185", "size": 40, "shape": "square"},
]

# Add main components
for comp in components:
    fig.add_trace(go.Scatter(
        x=[comp['x']],
        y=[comp['y']],
        mode='markers+text',
        marker=dict(
            size=comp['size'],
            color=comp['color'],
            line=dict(width=2, color='white'),
            symbol='square' if comp['shape'] == 'square' else 'circle'
        ),
        text=comp['name'],
        textposition='middle center',
        textfont=dict(size=12, color='black', family='Arial Bold'),
        showlegend=False,
        hoverinfo='text',
        hovertext=comp['name']
    ))

# Add thick bidirectional arrows for main flow
main_arrows = [
    # User to SQL Query
    {"x": [2, 2], "y": [5.85, 5.35], "color": "darkblue", "width": 4},
    # SQL Query to MindsDB
    {"x": [2, 2], "y": [5.05, 4.55], "color": "darkblue", "width": 4},
    # MindsDB to Handler
    {"x": [2, 2], "y": [4.25, 3.75], "color": "darkgreen", "width": 4},
]

for arrow in main_arrows:
    # Forward arrow
    fig.add_trace(go.Scatter(
        x=arrow['x'],
        y=arrow['y'],
        mode='lines',
        line=dict(color=arrow['color'], width=arrow['width']),
        showlegend=False,
        hoverinfo='skip'
    ))
    # Return arrow (slightly offset)
    fig.add_trace(go.Scatter(
        x=[arrow['x'][1] + 0.05, arrow['x'][0] + 0.05],
        y=[arrow['y'][1], arrow['y'][0]],
        mode='lines',
        line=dict(color=arrow['color'], width=arrow['width'], dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Handler to tables connections
table_connections = [
    {"x": [1.9, 0.8], "y": [3.5, 2.9]},
    {"x": [1.95, 1.6], "y": [3.5, 2.9]},
    {"x": [2.05, 2.4], "y": [3.5, 2.9]},
    {"x": [2.1, 3.2], "y": [3.5, 2.9]},
]

for conn in table_connections:
    # To table
    fig.add_trace(go.Scatter(
        x=conn['x'],
        y=conn['y'],
        mode='lines',
        line=dict(color='darkgreen', width=3),
        showlegend=False,
        hoverinfo='skip'
    ))
    # From table (bidirectional)
    fig.add_trace(go.Scatter(
        x=[conn['x'][1], conn['x'][0]],
        y=[conn['y'][1] - 0.05, conn['y'][0] - 0.05],
        mode='lines',
        line=dict(color='purple', width=3, dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Tables to API connections
api_connections = [
    {"x": [0.8, 1.9], "y": [2.65, 1.95]},
    {"x": [1.6, 1.95], "y": [2.65, 1.95]},
    {"x": [2.4, 2.05], "y": [2.65, 1.95]},
    {"x": [3.2, 2.1], "y": [2.65, 1.95]},
]

for conn in api_connections:
    # To API
    fig.add_trace(go.Scatter(
        x=conn['x'],
        y=conn['y'],
        mode='lines',
        line=dict(color='purple', width=3),
        showlegend=False,
        hoverinfo='skip'
    ))
    # From API (bidirectional)
    fig.add_trace(go.Scatter(
        x=[conn['x'][1], conn['x'][0]],
        y=[conn['y'][1] + 0.05, conn['y'][0] + 0.05],
        mode='lines',
        line=dict(color='orange', width=3, dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Connection parameters (near API)
params = [
    {"name": "api_key", "x": 1.2, "y": 1.4, "color": "#B4413C"},
    {"name": "sandbox", "x": 2.8, "y": 1.4, "color": "#B4413C"},
]

for param in params:
    fig.add_trace(go.Scatter(
        x=[param['x']],
        y=[param['y']],
        mode='markers+text',
        marker=dict(size=15, color=param['color'], symbol='square'),
        text=param['name'],
        textposition='middle center',
        textfont=dict(size=10, color='white', family='Arial Bold'),
        showlegend=False,
        hoverinfo='text',
        hovertext=param['name']
    ))

# API endpoints (below API)
endpoints = [
    {"name": "/quotes", "x": 0.8, "y": 1.2, "color": "#D2BA4C"},
    {"name": "/listings", "x": 1.6, "y": 1.2, "color": "#D2BA4C"},
    {"name": "/info", "x": 2.4, "y": 1.2, "color": "#D2BA4C"},
    {"name": "/metrics", "x": 3.2, "y": 1.2, "color": "#D2BA4C"},
]

for endpoint in endpoints:
    fig.add_trace(go.Scatter(
        x=[endpoint['x']],
        y=[endpoint['y']],
        mode='markers+text',
        marker=dict(size=18, color=endpoint['color'], symbol='square'),
        text=endpoint['name'],
        textposition='middle center',
        textfont=dict(size=9, color='black', family='Arial Bold'),
        showlegend=False,
        hoverinfo='text',
        hovertext=endpoint['name']
    ))

# Handler Files section (right side)
files_header = {"name": "Handler Files", "x": 5.2, "y": 4.5, "color": "#964325"}
fig.add_trace(go.Scatter(
    x=[files_header['x']],
    y=[files_header['y']],
    mode='markers+text',
    marker=dict(size=35, color=files_header['color'], symbol='square'),
    text=files_header['name'],
    textposition='middle center',
    textfont=dict(size=12, color='white', family='Arial Bold'),
    showlegend=False,
    hoverinfo='text',
    hovertext=files_header['name']
))

# Individual files
files = [
    {"name": "handler.py", "x": 5.2, "y": 4.1, "color": "#944454"},
    {"name": "tables.py", "x": 5.2, "y": 3.8, "color": "#944454"},
    {"name": "__init__.py", "x": 5.2, "y": 3.5, "color": "#944454"},
    {"name": "__about__.py", "x": 5.2, "y": 3.2, "color": "#944454"},
    {"name": "connection.py", "x": 5.2, "y": 2.9, "color": "#944454"},
    {"name": "requirements", "x": 5.2, "y": 2.6, "color": "#944454"},
]

for file in files:
    fig.add_trace(go.Scatter(
        x=[file['x']],
        y=[file['y']],
        mode='markers+text',
        marker=dict(size=20, color=file['color'], symbol='square'),
        text=file['name'],
        textposition='middle center',
        textfont=dict(size=10, color='white', family='Arial Bold'),
        showlegend=False,
        hoverinfo='text',
        hovertext=file['name']
    ))

# Add flow labels
labels = [
    {"text": "SQL Query", "x": 2.3, "y": 5.6, "color": "darkblue"},
    {"text": "API Request", "x": 2.3, "y": 4.8, "color": "darkgreen"},
    {"text": "DataFrame Response", "x": 2.3, "y": 4.0, "color": "darkgreen"},
]

for label in labels:
    fig.add_trace(go.Scatter(
        x=[label['x']],
        y=[label['y']],
        mode='text',
        text=label['text'],
        textfont=dict(size=11, color=label['color'], family='Arial Bold'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Update layout
fig.update_layout(
    title="CoinMarketCap Handler Integration",
    xaxis=dict(
        range=[0, 6],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[1, 6.5],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

fig.write_image("coinmarketcap_flowchart.png", width=1200, height=800)