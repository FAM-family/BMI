import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="2025 BMI Interactive Avatar", layout="wide")
st.title("⚖️ BMI Visualizer with Dynamic Avatar")

# --- SIDEBAR: Inputs ---
st.sidebar.header("Input Measurements")
weight = st.sidebar.slider("Weight (kg)", min_value=30, max_value=150, value=70, step=1)
total_inches = st.sidebar.slider("Height (inches)", min_value=36, max_value=96, value=68, step=1)

# --- CALCULATIONS ---
height_m = total_inches * 0.0254
bmi = round(weight / (height_m**2), 2)
feet, inches = total_inches // 12, total_inches % 12

# Standard Categories
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

# --- COLUMN 1: BMI CATEGORY MAP ---
with plot_col:
    weights_grid = np.linspace(30, 150, 100)
    heights_grid = np.linspace(36, 96, 100)
    W, H = np.meshgrid(weights_grid, heights_grid)
    BMI_z = W / ((H * 0.0254)**2)

    fig_map = go.Figure()
    fig_map.add_trace(go.Contour(
        z=BMI_z, x=weights_grid, y=heights_grid,
        colorscale=[[0, 'blue'], [0.185, 'blue'], [0.185, 'green'], [0.25, 'green'], 
                    [0.25, 'orange'], [0.3, 'orange'], [0.3, 'red'], [1, 'red']],
        showscale=False, contours=dict(showlines=False), opacity=0.3, hoverinfo='skip'
    ))
    
    # Legend Traces
    for cat in categories:
        fig_map.add_trace(go.Scatter(x=[None], y=[None], mode='markers', 
                                    marker=dict(size=12, color=cat['color'], symbol='square'), name=cat['name']))

    fig_map.add_trace(go.Scatter(x=[weight], y=[total_inches], mode="markers+text",
                                text=[f"YOU"], textposition="top center", name="Current",
                                marker=dict(color='black', size=15, symbol='diamond')))

    fig_map.update_layout(title="BMI Map", xaxis_title="Weight (kg)", yaxis_title="Height (in)", height=500)
    st.plotly_chart(fig_map, use_container_width=True)

# --- COLUMN 2: DYNAMIC HUMAN AVATAR ---
with avatar_col:
    # Calculate Scaling Factors for Avatar
    # Base height at 68 inches, Base width at 70 kg
    h_scale = total_inches / 68
    w_scale = (weight / 70) ** 0.5 # Square root scaling prevents looking too distorted

    fig_avatar = go.Figure()

    # Define an SVG-like human shape (Head, Torso, Limbs) using coordinates
    # We multiply Y by h_scale and X by w_scale
    avatar_color = current_cat["color"]
    
    # Simple Stylized Human Shape
    fig_avatar.add_trace(go.Scatter(
        x=[0], y=[1.8 * h_scale], mode="markers", 
        marker=dict(size=40 * w_scale, color=avatar_color), showlegend=False
    )) # Head
    
    fig_avatar.add_shape(type="rect", x0=-0.4 * w_scale, y0=0.8 * h_scale, x1=0.4 * w_scale, y1=1.6 * h_scale,
                        fillcolor=avatar_color, line_color=avatar_color) # Torso
    
    fig_avatar.add_shape(type="line", x0=-0.2 * w_scale, y0=0, x1=-0.2 * w_scale, y1=0.8 * h_scale,
                        line=dict(color=avatar_color, width=15 * w_scale)) # Left Leg
    
    fig_avatar.add_shape(type="line", x0=0.2 * w_scale, y0=0, x1=0.2 * w_scale, y1=0.8 * h_scale,
                        line=dict(color=avatar_color, width=15 * w_scale)) # Right Leg

    fig_avatar.update_layout(
        title=f"Body Preview ({current_cat['name']})",
        xaxis=dict(range=[-2, 2], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 2.5], showgrid=False, zeroline=False, showticklabels=False),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_avatar, use_container_width=True)
