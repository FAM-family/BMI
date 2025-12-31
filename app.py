import streamlit as st
import plotly.graph_objects as go
import numpy as np
from streamlit_vertical_slider import vertical_slider # requires pip install streamlit-vertical-slider

st.set_page_config(page_title="2025 BMI Visualizer", layout="wide")

st.title("⚖️ Interactive BMI Heatmap")

# --- SIDEBAR: Vertical Sliders ---
st.sidebar.header("Adjust Parameters")
col1, col2 = st.sidebar.columns(2)

with col1:
    st.write("Weight (kg)")
    # Using 3rd party vertical slider for vertical orientation
    weight = vertical_slider(key="weight", min_value=30, max_value=150, default_value=70, step=1, thumb_shape="pill")

with col2:
    st.write("Height (in)")
    total_inches = vertical_slider(key="height", min_value=36, max_value=96, default_value=68, step=1, thumb_shape="pill")

# --- CALCULATIONS ---
# Conversion and BMI Formula: kg / (meters^2)
height_m = total_inches * 0.0254
bmi = round(weight / (height_m**2), 2)

# Height in Feet & Inches
feet = total_inches // 12
inches = total_inches % 12

# --- RESULTS SECTION ---
st.subheader("Your Stats")
res1, res2, res3 = st.columns(3)
res1.metric("Height", f"{feet}' {inches}\"")
res2.metric("Weight", f"{weight} kg")
res3.metric("Calculated BMI", f"{bmi}")

# --- 2D CHART LOGIC ---
# Create a grid of weights and heights for the background zones
weights_range = np.linspace(30, 150, 50)
heights_range = np.linspace(36, 96, 50)
W, H = np.meshgrid(weights_range, heights_range)
BMI_grid = W / ((H * 0.0254)**2)

fig = go.Figure()

# Background BMI Zones
fig.add_trace(go.Contour(
    z=BMI_grid,
    x=weights_range,
    y=heights_range,
    colorscale=[
        [0, 'blue'], [18.5/50, 'blue'],      # Underweight
        [18.5/50, 'green'], [25/50, 'green'], # Normal
        [25/50, 'orange'], [30/50, 'orange'], # Overweight
        [30/50, 'red'], [1, 'red']            # Obese
    ],
    showscale=False,
    contours=dict(start=0, end=50, size=5, showlines=False),
    opacity=0.3,
    hoverinfo='skip'
))

# User Marker
fig.add_trace(go.Scatter(
    x=[weight], y=[total_inches],
    mode="markers+text",
    text=[f"YOU (BMI: {bmi})"],
    textposition="top center",
    marker=dict(color='black', size=15, symbol='diamond-wide', line=dict(width=2, color='white'))
))

fig.update_layout(
    xaxis_title="Weight (kg)",
    yaxis_title="Height (total inches)",
    height=600,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
