import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Change the background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d9e4dd;  /* Light gray-green */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Customizing the title with HTML/CSS to make it larger and green
st.markdown("<h1 style='color: green;'>GreenCompute</h1>", unsafe_allow_html=True)

# Input fields for CPU and memory
input_cpu = st.text_input("What is the CPU?")
input_memory = st.text_input("What is the memory?")

# Show the CPU and memory only if input_cpu has a value
if input_cpu:
    st.write(f"The input CPU is: {input_cpu}")
    st.write(f"The input memory is: {input_memory}")

st.write("<h2 style='color: green;font-style: italic;'>Estimated Carbon Footprint</h2>", unsafe_allow_html=True)
st.write("#### Cloud Carbon Footprint ___")
st.write("#### IT Electricity Usage ___")
    
df = pd.read_csv("./Cloud Carbon Footprint - Embodied Emissions.csv")

# Rename columns
df.columns = ['series', 'vm', 'CPU', 'memory', 'carbon_emission', 'carbon_emission2']
#df['carbon_emission'] = np.log(df['carbon_emission'])

# Create two columns (left and right)
col1, col2 = st.columns(2)

# Scatter plot for Column A vs Column B
with col1:
    st.write("##### Carbon Emission vs. # of CPUs")
    scatter_plot = (
        alt.Chart(df)
        .mark_circle(color='orange')  # Set the color to green
        .encode(
            x='CPU',
            y='carbon_emission',
            tooltip=['CPU','carbon_emission']  # Optional: show values on hover
        )
        .properties(width=400, height=300)  # Set plot size
    )
    
    st.altair_chart(scatter_plot, use_container_width=True)

# Scatter plot for Column C vs Column B
with col2:
    st.write("##### Carbon Emission vs. Memory")
    scatter_plot = (
        alt.Chart(df)
        .mark_circle(color='blue')  # Set the color to green
        .encode(
            x='memory',
            y='carbon_emission',
            tooltip=['memory', 'carbon_emission']  # Optional: show values on hover
        )
        .properties(width=400, height=300)  # Set plot size
    )
    
    st.altair_chart(scatter_plot, use_container_width=True)

