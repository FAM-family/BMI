import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="2025 Standard BMI Visualizer", layout="wide")
st.title("⚖️ Standard BMI Visualizer with Body Preview")

# --- SIDEBAR: Core Inputs ---
st.sidebar.header("Measurements")
weight = st.sidebar.slider("Select Weight (kg)", min_value=30, max_value=150, value=70, step=1)
total_inches = st.sidebar.slider("Select Height (inches)", min_value=36, max_value=96, value=68, step=1)

# --- CALCULATIONS ---
# Standard adult BMI formula: kg / (meters^2)
height_m = total_inches * 0.0254
bmi = round(weight / (height_m**2), 2)
feet, inches = total_inches // 12, total_inches % 12

# Standard Global BMI Categories
categories = [
    {"name": "Underweight", "color": "blue", "range": (0, 18.5)},
    {"name": "Normal Weight", "color": "green", "range": (18.5, 25)},
    {"name": "Overweight", "color": "orange", "range": (25, 30)},
    {"name": "Obese", "color": "red", "range": (30, 100)}
]
current_cat = next((c for c in categories if c["range"] <= bmi < c["range"]), categories[-1])

# --- RESULTS SECTION ---
st.subheader("Profile Results")
res1, res2, res3 = st.columns(3)
res1.metric("Height", f"{feet}' {inches}\"")
res2.metric("Weight", f"{weight} kg")
res3.metric("BMI", f"{bmi}", delta=current_cat["name"], delta_color="normal")

plot_col, avatar_col = st.columns(2)

# --- COLUMN 1: BMI CATEGORY MAP ---
with plot_col:
    w_grid = np.linspace(30, 150, 100)
    h_grid = np.linspace(36, 96, 100)
    W, H = np.meshgrid(w_grid, h_grid)
    BMI_z = W / ((H * 0.0254)**2)

    fig_map = go.Figure()
    # Background Contour with specific Green Zone definition
    fig_map.add_trace(go.Contour(
        z=BMI_z, x=w_grid, y=h_grid,
        colorscale=[
            [0, 'blue'], [18.5/100, 'blue'],      # Underweight
            [18.5/100, 'green'], [25/100, 'green'], # Normal (Explicit Green Zone)
            [25/100, 'orange'], [30/100, 'orange'], # Overweight
            [30/100, 'red'], [1, 'red']             # Obese
        ],
        showscale=False, contours=dict(showlines=False), opacity=0.4, hoverinfo='skip'
    ))
    
    # Legend Traces
    for cat in categories:
        fig_map.add_trace(go.Scatter(x=[None], y=[None], mode='markers', 
                                    marker=dict(size=12, color=cat['color'], symbol='square'), name=cat['name']))

    # User Marker: Set to WHITE for high visibility
    fig_map.add_trace(go.Scatter(
        x=[weight], y=[total_inches], mode="markers+text",
        text=[f"YOU ({bmi})"], textposition="top center", name="Your Position",
        marker=dict(color='white', size=15, symbol='diamond', line=dict(color='black', width=2))
    ))

    fig_map.update_layout(title="BMI Map", xaxis_title="Weight (kg)", yaxis_title="Height (in)", height=500)
    st.plotly_chart(fig_map, use_container_width=True)

# --- COLUMN 2: DYNAMIC AVATAR ---
with avatar_col:
    h_scale, w_scale = total_inches / 68, (weight / 70) ** 0.5
    fig_avatar = go.Figure()
    avatar_color = current_cat["color"]
    
    # Head
    fig_avatar.add_trace(go.Scatter(x=[0], y=[1.8 * h_scale], mode="markers", 
                                    marker=dict(size=40 * w_scale, color=avatar_color), showlegend=False))
    # Torso
    fig_avatar.add_shape(type="rect", x0=-0.35 * w_scale, y0=0.8 * h_scale, x1=0.35 * w_scale, y1=1.6 * h_scale,
                        fillcolor=avatar_color, line_color=avatar_color)
    # Legs
    for offset in [-0.18, 0.18]:
        fig_avatar.add_shape(type="line", x0=offset * w_scale, y0=0, x1=offset * w_scale, y1=0.8 * h_scale,
                            line=dict(color=avatar_color, width=12 * w_scale))

    fig_avatar.update_layout(
        title="Body Scaling Preview",
        xaxis=dict(range=[-2, 2], visible=False), 
        yaxis=dict(range=[0, 2.5], visible=False), 
        height=500, plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_avatar, use_container_width=True)
