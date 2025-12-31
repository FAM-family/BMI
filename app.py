import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="2025 BMI Health Tracker", layout="wide")
st.title("⚖️ BMI Visualizer & Healthy Weight Calculator")

# --- SIDEBAR: Inputs ---
st.sidebar.header("Input Measurements")
weight = st.sidebar.slider("Your Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.5)
total_inches = st.sidebar.slider("Your Height (inches)", min_value=36, max_value=96, value=68, step=1)

# --- CALCULATIONS ---
height_m = total_inches * 0.0254
bmi = round(weight / (height_m**2), 2)
feet, inches = total_inches // 12, total_inches % 12

# Calculate Normal Weight Range for the user's specific height
# Formula: Weight = BMI * (Height^2)
min_healthy_weight = round(18.5 * (height_m**2), 1)
max_healthy_weight = round(25.0 * (height_m**2), 1)

categories = [
    {"name": "Underweight", "color": "blue", "range": (0, 18.5)},
    {"name": "Normal", "color": "green", "range": (18.5, 25)},
    {"name": "Overweight", "color": "orange", "range": (25, 30)},
    {"name": "Obese", "color": "red", "range": (30, 100)}
]
current_cat = next((c for c in categories if c["range"][0] <= bmi < c["range"][1]), categories[-1])

# --- RESULTS SECTION ---
st.subheader("Your Health Metrics")
col_res1, col_res2, col_res3 = st.columns([1, 1, 2])

with col_res1:
    st.metric("Current Height", f"{feet}' {inches}\"")
    st.metric("Current Weight", f"{weight} kg")

with col_res2:
    st.metric("Your BMI", f"{bmi}", delta=current_cat["name"], delta_color="normal")

with col_res3:
    st.info(f"""
    **Healthy Targets for Your Height:**
    *   **Normal BMI Range:** 18.5 — 25.0
    *   **Normal Weight Range:** {min_healthy_weight} kg — {max_healthy_weight} kg
    """)

st.divider()

# --- VISUALIZATION SECTION ---
plot_col, avatar_col = st.columns([2, 1])

with plot_col:
    # Generate background grid
    w_grid = np.linspace(30, 150, 100)
    h_grid = np.linspace(36, 96, 100)
    W, H = np.meshgrid(w_grid, h_grid)
    BMI_z = W / ((H * 0.0254)**2)

    # Force discrete color blocks (Fixes Green Normal Zone)
    d_colors = [
        [0, 'blue'], [18.5/50, 'blue'],
        [18.5/50, 'green'], [25/50, 'green'],
        [25/50, 'orange'], [30/50, 'orange'],
        [30/50, 'red'], [1, 'red']
    ]

    fig_map = go.Figure()
    fig_map.add_trace(go.Contour(
        z=BMI_z, x=w_grid, y=h_grid, zmin=0, zmax=50,
        colorscale=d_colors, showscale=False,
        contours=dict(showlines=False, coloring='heatmap'),
        opacity=0.4, hoverinfo='skip'
    ))
    
    # Legend
    for cat in categories:
        fig_map.add_trace(go.Scatter(x=[None], y=[None], mode='markers', 
                                    marker=dict(size=12, color=cat['color'], symbol='square'), name=cat['name']))

    # WHITE DIAMOND marker for high contrast
    fig_map.add_trace(go.Scatter(
        x=[weight], y=[total_inches], mode="markers+text",
        text=[f"YOU ({bmi})"], textposition="top center", name="Your Position",
        marker=dict(color='white', size=16, symbol='diamond', line=dict(color='black', width=2))
    ))

    fig_map.update_layout(title="BMI Map (Weight vs Height)", xaxis_title="Weight (kg)", yaxis_title="Height (in)", height=500)
    st.plotly_chart(fig_map, use_container_width=True, theme=None)

with avatar_col:
    h_scale, w_scale = total_inches / 68, (weight / 70) ** 0.5
    fig_avatar = go.Figure()
    avatar_color = current_cat["color"]
    
    # Body Visualization
    fig_avatar.add_trace(go.Scatter(x=[0], y=[1.8 * h_scale], mode="markers", 
                                    marker=dict(size=45 * w_scale, color=avatar_color), showlegend=False)) 
    fig_avatar.add_shape(type="rect", x0=-0.4 * w_scale, y0=0.8 * h_scale, x1=0.4 * w_scale, y1=1.6 * h_scale,
                        fillcolor=avatar_color, line_color=avatar_color) 
    for x_pos in [-0.2, 0.2]:
        fig_avatar.add_shape(type="line", x0=x_pos * w_scale, y0=0, x1=x_pos * w_scale, y1=0.8 * h_scale,
                            line=dict(color=avatar_color, width=15 * w_scale)) 

    fig_avatar.update_layout(title="Body Preview", xaxis=dict(range=[-2, 2], visible=False), 
                            yaxis=dict(range=[0, 2.5], visible=False), height=500, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_avatar, use_container_width=True, theme=None)
