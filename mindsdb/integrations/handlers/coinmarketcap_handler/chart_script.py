import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Create the figure
fig = go.Figure()

# Define component positions for a top-down flowchart with proper colors
components = {
    # Level 0 - User input
    "User SQL Query": {"x": 0, "y": 6.5, "color": "#1FB8CD", "width": 1.5, "height": 0.4},
    
    # Level 1 - MindsDB (blue)
    "MindsDB Instance": {"x": 0, "y": 5.5, "color": "#1FB8CD", "width": 1.8, "height": 0.4},
    
    # Level 2 - Handler (green)
    "CoinMarketCap Handler": {"x": 0, "y": 4.5, "color": "#ECEBD5", "width": 2.2, "height": 0.4},
    
    # Level 3 - Tables (purple)
    "Quotes Table": {"x": -3, "y": 3.5, "color": "#944454", "width": 1.3, "height": 0.35},
    "Listings Table": {"x": -1, "y": 3.5, "color": "#944454", "width": 1.3, "height": 0.35},
    "Info Table": {"x": 1, "y": 3.5, "color": "#944454", "width": 1.3, "height": 0.35},
    "Global Metrics": {"x": 3, "y": 3.5, "color": "#944454", "width": 1.3, "height": 0.35},
    
    # Level 4 - API (orange)
    "CoinMarketCap API": {"x": 0, "y": 2.5, "color": "#FFC185", "width": 2, "height": 0.4},
    
    # Connection parameters
    "api_key": {"x": -1.5, "y": 1.5, "color": "#D2BA4C", "width": 1, "height": 0.3},
    "sandbox mode": {"x": 1.5, "y": 1.5, "color": "#D2BA4C", "width": 1.2, "height": 0.3},
}

# Add rectangular boxes for each component
for name, props in components.items():
    # Create rectangle
    fig.add_shape(
        type="rect",
        x0=props["x"] - props["width"]/2,
        y0=props["y"] - props["height"]/2,
        x1=props["x"] + props["width"]/2,
        y1=props["y"] + props["height"]/2,
        fillcolor=props["color"],
        line=dict(color="black", width=1)
    )
    
    # Add text label with white color for dark backgrounds
    text_color = "white" if name in ["Quotes Table", "Listings Table", "Info Table", "Global Metrics"] else "black"
    fig.add_annotation(
        x=props["x"],
        y=props["y"],
        text=name,
        showarrow=False,
        font=dict(size=9, color=text_color),
        xanchor="center",
        yanchor="middle"
    )

# Add arrows showing data flow with proper direction
def add_arrow(start_name, end_name, offset_x=0):
    start = components[start_name]
    end = components[end_name]
    
    start_x = start["x"] + offset_x
    start_y = start["y"] - start["height"]/2
    end_x = end["x"] + offset_x
    end_y = end["y"] + end["height"]/2
    
    # Add arrow line
    fig.add_shape(
        type="line",
        x0=start_x, y0=start_y,
        x1=end_x, y1=end_y,
        line=dict(color="gray", width=2)
    )
    
    # Add arrowhead
    fig.add_annotation(
        x=end_x, y=end_y,
        ax=start_x, ay=start_y,
        xref="x", yref="y",
        axref="x", ayref="y",
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor="gray",
        showarrow=True,
        text=""
    )

# Add main data flow arrows
add_arrow("User SQL Query", "MindsDB Instance")
add_arrow("MindsDB Instance", "CoinMarketCap Handler")
add_arrow("CoinMarketCap Handler", "Quotes Table", -0.5)
add_arrow("CoinMarketCap Handler", "Listings Table", -0.2)
add_arrow("CoinMarketCap Handler", "Info Table", 0.2)
add_arrow("CoinMarketCap Handler", "Global Metrics", 0.5)
add_arrow("CoinMarketCap Handler", "CoinMarketCap API")

# Add connection parameter arrows
fig.add_annotation(
    x=components["api_key"]["x"], y=components["api_key"]["y"] + 0.15,
    ax=components["CoinMarketCap API"]["x"] - 0.5, ay=components["CoinMarketCap API"]["y"] - 0.2,
    arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="gray",
    showarrow=True, text=""
)

fig.add_annotation(
    x=components["sandbox mode"]["x"], y=components["sandbox mode"]["y"] + 0.15,
    ax=components["CoinMarketCap API"]["x"] + 0.5, ay=components["CoinMarketCap API"]["y"] - 0.2,
    arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="gray",
    showarrow=True, text=""
)

# Add API endpoints box
fig.add_shape(
    type="rect",
    x0=-1.5, y0=0.5, x1=1.5, y1=1,
    fillcolor="#5D878F",
    line=dict(color="black", width=1)
)

fig.add_annotation(
    x=0, y=0.75,
    text="API Endpoints:<br>/v1/crypto/quotes<br>/v1/crypto/listings<br>/v2/crypto/info<br>/v1/global-metrics",
    showarrow=False,
    font=dict(size=8, color="white"),
    xanchor="center",
    yanchor="middle"
)

# Add file structure as a proper hierarchy
file_x_start = 4.5
file_y_start = 5.5
files = [
    "__init__.py",
    "__about__.py", 
    "handler.py",
    "tables.py",
    "connection_args.py",
    "requirements.txt",
    "README.md",
    "setup.py"
]

# File structure title
fig.add_annotation(
    x=file_x_start, y=file_y_start + 0.3,
    text="Handler Files:",
    showarrow=False,
    font=dict(size=10, color="black", family="Arial Black"),
    xanchor="center"
)

# Add individual file boxes
for i, filename in enumerate(files):
    y_pos = file_y_start - (i * 0.25)
    fig.add_shape(
        type="rect",
        x0=file_x_start - 0.6, y0=y_pos - 0.08,
        x1=file_x_start + 0.6, y1=y_pos + 0.08,
        fillcolor="#B4413C",
        line=dict(color="black", width=1)
    )
    
    fig.add_annotation(
        x=file_x_start, y=y_pos,
        text=filename,
        showarrow=False,
        font=dict(size=7, color="white"),
        xanchor="center",
        yanchor="middle"
    )

# Add data flow direction indicator
fig.add_annotation(
    x=-4, y=6.5,
    text="Data Flow ↓",
    showarrow=False,
    font=dict(size=12, color="black", family="Arial Black"),
    xanchor="left"
)

# Update layout
fig.update_layout(
    title="CoinMarketCap Handler Architecture",
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-5, 6]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 7]
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Save the chart
fig.write_image("coinmarketcap_architecture.png")