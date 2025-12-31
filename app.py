import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Interactive BMI Calculator", page_icon="⚖️")
st.title("⚖️ Interactive BMI Calculator")

# Sidebar for User Inputs using Sliders
st.sidebar.header("User Input")
weight = st.sidebar.slider("Weight (kg)", min_value=10.0, max_value=200.0, value=70.0, step=0.1)
height_cm = st.sidebar.slider("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)

# BMI Calculation logic
height_m = height_cm / 100
bmi = round(weight / (height_m ** 2), 2)

# Determine Category
if bmi < 18.5:
    status, color = "Underweight", "blue"
elif 18.5 <= bmi < 25:
    status, color = "Normal Weight", "green"
elif 25 <= bmi < 30:
    status, color = "Overweight", "orange"
else:
    status, color = "Obese", "red"

# Display Results
st.subheader(f"Your BMI is: **{bmi}**")
st.markdown(f"Category: <span style='color:{color}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)

# Interactive Chart showing BMI Zones
fig = go.Figure()

# Adding Category Zones
fig.add_vrect(x0=0, x1=18.5, fillcolor="blue", opacity=0.2, line_width=0, annotation_text="Underweight")
fig.add_vrect(x0=18.5, x1=25, fillcolor="green", opacity=0.2, line_width=0, annotation_text="Normal")
fig.add_vrect(x0=25, x1=30, fillcolor="orange", opacity=0.2, line_width=0, annotation_text="Overweight")
fig.add_vrect(x0=30, x1=50, fillcolor="red", opacity=0.2, line_width=0, annotation_text="Obese")

# Plot the user's BMI point
fig.add_trace(go.Scatter(
    x=[bmi], y=[0.5],
    mode="markers+text",
    text=[f"YOU ({bmi})"],
    textposition="top center",
    marker=dict(color='black', size=15, symbol='diamond')
))

fig.update_layout(
    title="BMI Category Visualizer",
    xaxis=dict(title="BMI Value", range=[10, 45]),
    yaxis=dict(showticklabels=False, range=[0, 1]),
    height=300,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
