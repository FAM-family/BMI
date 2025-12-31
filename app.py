import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="2025 BMI Tracker", layout="wide")
st.title("⚖️ DaCode-r's BMI Visualizer")

# --- SIDEBAR: Native Horizontal Sliders ---
st.sidebar.header("Input Measurements")
# Weight in Kg
weight = st.sidebar.slider("Select Weight (kg)", min_value=30, max_value=150, value=70, step=1)
# Height in total inches
total_inches = st.sidebar.slider("Select Height (inches)", min_value=36, max_value=96, value=68, step=1)

# --- CALCULATIONS ---
# BMI Formula: kg / (meters^2) | 1 inch = 0.0254 meters
height_m = total_inches * 0.0254
bmi = round(weight / (height_m**2), 2)

# Convert total inches to Feet and Inches for display
feet = total_inches // 12
inches = total_inches % 12

# Determine Category for display
if bmi < 18.5:
    status, color = "Underweight", "blue"
elif 18.5 <= bmi < 25:
    status, color = "Normal", "green"
elif 25 <= bmi < 30:
    status, color = "Overweight", "orange"
else:
    status, color = "Obese", "red"

# --- RESULTS SECTION ---
st.subheader("Current Profile")
res1, res2, res3 = st.columns(3)
res1.metric("Height (Ft/In)", f"{feet}' {inches}\"")
res2.metric("Weight (Kg)", f"{weight} kg")
res3.metric("Your BMI", f"{bmi}", delta=status, delta_color="normal")

# --- 2D CHART VISUALIZATION ---
# Create grid for background BMI zones
weights_grid = np.linspace(30, 150, 100)
heights_grid = np.linspace(36, 96, 100)
W, H = np.meshgrid(weights_grid, heights_grid)
BMI_z = W / ((H * 0.0254)**2)

fig = go.Figure()

# 2D Contour for BMI Zones
fig.add_trace(go.Contour(
    z=BMI_z,
    x=weights_grid,
    y=heights_grid,
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

# User Marker (The current calculated BMI point)
fig.add_trace(go.Scatter(
    x=[weight], y=[total_inches],
    mode="markers+text",
    text=[f"BMI: {bmi}"],
    textposition="top center",
    marker=dict(color='black', size=15, symbol='diamond', line=dict(width=2, color='white'))
))

fig.update_layout(
    title="BMI Category Map (Weight vs Height)",
    xaxis_title="Weight (kg)",
    yaxis_title="Height (total inches)",
    height=600,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
