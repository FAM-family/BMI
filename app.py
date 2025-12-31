import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="2025 BMI Tracker", layout="wide")
st.title("⚖️ BMI Visualizer with Fixed Color Zones")

# --- SIDEBAR: Inputs ---
st.sidebar.header("Input Measurements")
weight = st.sidebar.slider("Weight (kg)", min_value=30, max_value=150, value=70, step=1)
total_inches = st.sidebar.slider("Height (inches)", min_value=36, max_value=96, value=68, step=1)

# --- CALCULATIONS ---
height_m = total_inches * 0.0254
bmi = round(weight / (height_m**2), 2)
feet, inches = total_inches // 12, total_inches % 12

categories = [
    {"name": "Underweight", "color": "blue", "range": (0, 18.5)},
    {"name": "Normal", "color": "green", "range": (18.5, 25)},
    {"name": "Overweight", "color": "orange", "range": (25, 30)},
    {"name": "Obese", "color": "red", "range": (30, 100)}
]
current_cat = next((c for c in categories if c["range"][0] <= bmi < c["range"][1]), categories[-1])

# --- DISPLAY METRICS ---
res1, res2, res3 = st.columns(3)
res1.metric("Height", f"{feet}' {inches}\"")
res2.metric("Weight", f"{weight} kg")
res3.metric("BMI", f"{bmi}", delta=current_cat["name"], delta_color="normal")

plot_col, avatar_col = st.columns([2, 1])

with plot_col:
    w_grid = np.linspace(30, 150, 100)
    h_grid = np.linspace(36, 96, 100)
    W, H = np.meshgrid(w_grid, h_grid)
    BMI_z = W / ((H * 0.0254)**2)

    # DISCONTINUOUS COLORSCALE: Defines blocks of color instead of a gradient
    # Normalize BMI values 0-50 to 0.0-1.0
    d_colors = [
        [0, 'blue'], [18.5/50, 'blue'],         # Underweight block
        [18.5/50, 'green'], [25/50, 'green'],   # Normal block (Green Area)
        [25/50, 'orange'], [30/50, 'orange'],   # Overweight block
        [30/50, 'red'], [1, 'red']              # Obese block
    ]

    fig_map = go.Figure()
    fig_map.add_trace(go.Contour(
        z=BMI_z, x=w_grid, y=h_grid,
        zmin=0, zmax=50,
        colorscale=d_colors,
        showscale=False, 
        contours=dict(showlines=False, coloring='heatmap'),
        opacity=0.4, hoverinfo='skip'
    ))
    
    for cat in categories:
        fig_map.add_trace(go.Scatter(x=[None], y=[None], mode='markers', 
                                    marker=dict(size=12, color=cat['color'], symbol='square'), name=cat['name']))

    # WHITE MARKER with black outline
    fig_map.add_trace(go.Scatter(
        x=[weight], y=[total_inches], mode="markers+text",
        text=[f"YOU ({bmi})"], textposition="top center", name="Your Position",
        marker=dict(color='white', size=15, symbol='diamond', line=dict(color='black', width=2))
    ))

    fig_map.update_layout(title="BMI Map (Normal Zone in Green)", xaxis_title="Weight (kg)", yaxis_title="Height (in)", height=500)
    # Using theme=None ensures Streamlit doesn't overwrite your colors
    st.plotly_chart(fig_map, use_container_width=True, theme=None)

with avatar_col:
    h_scale, w_scale = total_inches / 68, (weight / 70) ** 0.5
    fig_avatar = go.Figure()
    avatar_color = current_cat["color"]
    
    fig_avatar.add_trace(go.Scatter(x=[0], y=[1.8 * h_scale], mode="markers", 
                                    marker=dict(size=40 * w_scale, color=avatar_color), showlegend=False)) 
    fig_avatar.add_shape(type="rect", x0=-0.4 * w_scale, y0=0.8 * h_scale, x1=0.4 * w_scale, y1=1.6 * h_scale,
                        fillcolor=avatar_color, line_color=avatar_color) 
    fig_avatar.add_shape(type="line", x0=-0.2 * w_scale, y0=0, x1=-0.2 * w_scale, y1=0.8 * h_scale,
                        line=dict(color=avatar_color, width=15 * w_scale)) 
    fig_avatar.add_shape(type="line", x0=0.2 * w_scale, y0=0, x1=0.2 * w_scale, y1=0.8 * h_scale,
                        line=dict(color=avatar_color, width=15 * w_scale)) 

    fig_avatar.update_layout(title="Body Preview", xaxis=dict(range=[-2, 2], visible=False), 
                            yaxis=dict(range=[0, 2.5], visible=False), height=500, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_avatar, use_container_width=True, theme=None)
