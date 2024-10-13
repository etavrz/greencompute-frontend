import streamlit as st
import pandas as pd
import altair as alt
import base64

# Paths to the logos
logo1 = "./images/logo1.png"
logo2 = "./images/logo2.png"
logo3 = "./images/logo3.png"


def add_logo(logo, width):
    # Read the image and convert it to Base64
    with open(logo, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    # Inject CSS with Base64-encoded image into the sidebar
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url("data:image/png;base64,{data}");
                background-repeat: no-repeat;
                padding-top: 180px;
                background-position: 20px 20px;
                background-size: {width};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Call the add_logo function with the path to your local image
add_logo(logo1, "260px")
add_logo(logo3, "260px")


df = pd.read_csv("./Cloud Carbon Footprint - Embodied Emissions.csv")

# Rename columns
df.columns = ["series", "vm", "CPU", "memory", "carbon_emission", "carbon_emission2"]

# Change the background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d9e4dd;  /* Light gray-green */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Customizing the title with HTML/CSS to make it larger and green
st.markdown("<h1 style='color: green;'>Background</h1>", unsafe_allow_html=True)

# Overview
st.write(
    "##### Data centers are critical infrastructure that significantly contribute to global carbon emissions. Operators lack effective tools to track, manage, and optimize their carbon footprint."
)

# Create two columns (left and right)
col1, col2 = st.columns(2)

# Scatter plot for Column A vs Column B
with col1:
    st.write("##### Carbon Emission vs. # of CPUs")
    scatter_plot = (
        alt.Chart(df)
        .mark_circle(color="orange")  # Set the color to green
        .encode(
            x="CPU",
            y="carbon_emission",
            tooltip=["CPU", "carbon_emission"],  # Optional: show values on hover
        )
        .properties(width=400, height=300)  # Set plot size
    )

    st.altair_chart(scatter_plot, use_container_width=True)

# Scatter plot for Column C vs Column B
with col2:
    st.write("##### Carbon Emission vs. Memory")
    scatter_plot = (
        alt.Chart(df)
        .mark_circle(color="blue")  # Set the color to green
        .encode(
            x="memory",
            y="carbon_emission",
            tooltip=["memory", "carbon_emission"],  # Optional: show values on hover
        )
        .properties(width=400, height=300)  # Set plot size
    )

    st.altair_chart(scatter_plot, use_container_width=True)
