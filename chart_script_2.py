import plotly.graph_objects as go
import json

# Parse the provided data
data = {"root": {"name": "CoinMarketCap Handler", "children": [{"name": "Quotes API", "data": ["Price", "Volume", "Market Cap", "24h Change"]}, {"name": "Listings API", "data": ["Rankings", "Symbols", "Market Data"]}, {"name": "Info API", "data": ["Descriptions", "Social Links", "Logos"]}, {"name": "Global Metrics API", "data": ["Total Market Cap", "BTC Dominance", "Volume"]}]}}

# Create figure
fig = go.Figure()

# Define positions
root_pos = (0, 2)
api_positions = [(-3, 1), (-1, 1), (1, 1), (3, 1)]
data_positions = [
    [(-3, 0), (-3, -0.3), (-3, -0.6), (-3, -0.9)],  # Quotes API data
    [(-1, 0), (-1, -0.3), (-1, -0.6)],  # Listings API data
    [(1, 0), (1, -0.3), (1, -0.6)],  # Info API data
    [(3, 0), (3, -0.3), (3, -0.6)]  # Global Metrics API data
]

# Colors
root_color = '#ECEBD5'  # Light green
api_color = '#1FB8CD'   # Strong cyan
data_color = '#5D878F'  # Cyan

# Add root box
fig.add_shape(
    type="rect",
    x0=root_pos[0]-1, y0=root_pos[1]-0.15,
    x1=root_pos[0]+1, y1=root_pos[1]+0.15,
    fillcolor=root_color,
    line=dict(color="black", width=2)
)

# Add root text
fig.add_annotation(
    x=root_pos[0], y=root_pos[1],
    text="CoinMarketCap<br>Handler",
    showarrow=False,
    font=dict(size=14, color="black", family="Arial Black"),
    align="center"
)

# Add API boxes and connecting lines
api_names = ["Quotes API", "Listings API", "Info API", "Global Metrics"]
for i, (pos, name) in enumerate(zip(api_positions, api_names)):
    # Add connecting line from root to API
    fig.add_shape(
        type="line",
        x0=root_pos[0], y0=root_pos[1]-0.15,
        x1=pos[0], y1=pos[1]+0.15,
        line=dict(color="black", width=2)
    )
    
    # Add API box
    fig.add_shape(
        type="rect",
        x0=pos[0]-0.6, y0=pos[1]-0.15,
        x1=pos[0]+0.6, y1=pos[1]+0.15,
        fillcolor=api_color,
        line=dict(color="black", width=2)
    )
    
    # Add API text (abbreviated)
    short_name = name.replace(" API", "")
    fig.add_annotation(
        x=pos[0], y=pos[1],
        text=short_name,
        showarrow=False,
        font=dict(size=12, color="white", family="Arial Bold"),
        align="center"
    )

# Add data items
all_data = [
    ["Price", "Volume", "Market Cap", "24h Change"],
    ["Rankings", "Symbols", "Market Data"],
    ["Descriptions", "Social Links", "Logos"],
    ["Total Mkt Cap", "BTC Dominance", "Volume"]
]

for i, (api_pos, data_items, positions) in enumerate(zip(api_positions, all_data, data_positions)):
    for j, (data_item, data_pos) in enumerate(zip(data_items, positions)):
        # Add connecting line from API to data
        fig.add_shape(
            type="line",
            x0=api_pos[0], y0=api_pos[1]-0.15,
            x1=data_pos[0], y1=data_pos[1]+0.1,
            line=dict(color="gray", width=1)
        )
        
        # Add data box
        fig.add_shape(
            type="rect",
            x0=data_pos[0]-0.5, y0=data_pos[1]-0.1,
            x1=data_pos[0]+0.5, y1=data_pos[1]+0.1,
            fillcolor=data_color,
            line=dict(color="black", width=1)
        )
        
        # Add data text (abbreviated to fit 15 char limit)
        short_data = data_item[:15] if len(data_item) <= 15 else data_item[:12] + "..."
        fig.add_annotation(
            x=data_pos[0], y=data_pos[1],
            text=short_data,
            showarrow=False,
            font=dict(size=10, color="white"),
            align="center"
        )

# Update layout
fig.update_layout(
    title="CoinMarketCap Handler Structure",
    showlegend=False,
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    plot_bgcolor="white"
)

# Update axes ranges
fig.update_xaxes(range=[-4, 4])
fig.update_yaxes(range=[-1.2, 2.5])

# Save the chart
fig.write_image("coinmarketcap_org_chart.png")