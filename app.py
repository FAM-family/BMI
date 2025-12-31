import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="2025 Gender-Aware BMI Visualizer", layout="wide")
st.title("DaCode-r Health Analyser!")

# --- SIDEBAR: Inputs ---
st.sidebar.header("Input Measurements")
gender = st.sidebar.radio("Select Gender", ["Male", "Female"])
weight = st.sidebar.slider("Weight (kg)", min_value=30, max_value=150, value=70, step=1)
total_inches = st.sidebar.slider("Height (inches)", min_value=36, max_value=96, value=68, step=1)

# --- CALCULATIONS ---
height_m = total_inches * 0.0254
bmi = round(weight / (height_m**2), 2)
feet, inches = total_inches // 12, total_inches % 12

# Gender-specific thresholds based on NHANES research
# Standard is 25, but some research suggests 27.3 for women and 27.8 for men
overweight_threshold = 27.8 if gender == "Male" else 27.3

# Categories
categories = [
    {"name": "Underweight", "color": "blue", "range": (0, 18.5)},
    {"name": "Normal", "color": "green", "range": (18.5, overweight_threshold)},
    {"name": "Overweight", "color": "orange", "range": (overweight_threshold, 30)},
    {"name": "Obese", "color": "red", "range": (30, 100)}
]
current_cat = next((c for c in categories if c["range"] <= bmi < c["range"]), categories[-1])

# --- DISPLAY METRICS ---
st.subheader(f"Current Profile: {gender}")
res1, res2, res3 = st.columns(3)
res1.metric("Height", f"{feet}' {inches}\"")
res2.metric("Weight", f"{weight} kg")
res3.metric("BMI", f"{bmi}", delta=current_cat["name"], delta_color="normal")

plot_col, avatar_col = st.columns()

# --- COLUMN 1: BMI CATEGORY MAP ---
with plot_col:
    w_grid = np.linspace(30, 150, 100)
    h_grid = np.linspace(36, 96, 100)
    W, H = np.meshgrid(w_grid, h_grid)
    BMI_z = W / ((H * 0.0254)**2)

    fig_map = go.Figure()
    fig_map.add_trace(go.Contour(
        z=BMI_z, x=w_grid, y=h_grid,
        colorscale=[
            [0, 'blue'], [18.5/100, 'blue'],
            [18.5/100, 'green'], [overweight_threshold/100, 'green'], 
            [overweight_threshold/100, 'orange'], [30/100, 'orange'],
            [30/100, 'red'], [1, 'red']
        ],
        showscale=False, contours=dict(showlines=False), opacity=0.4, hoverinfo='skip'
    ))
    
    for cat in categories:
        fig_map.add_trace(go.Scatter(x=[None], y=[None], mode='markers', 
                                    marker=dict(size=12, color=cat['color'], symbol='square'), name=cat['name']))

    # Marker updated to white for visibility
    fig_map.add_trace(go.Scatter(x=[weight], y=[total_inches], mode="markers+text",
                                text=[f"YOU"], textposition="top center", name="Your Position",
                                marker=dict(color='white', size=15, symbol='diamond', line=dict(color='black', width=2))))

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

    fig_avatar.update_layout(title="Body Preview", xaxis=dict(range=[-2, 2], visible=False), 
                            yaxis=dict(range=[0, 2.5], visible=False), height=500, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_avatar, use_container_width=True)
