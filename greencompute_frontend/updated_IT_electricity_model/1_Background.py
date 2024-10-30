import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import base64
import streamlit.components.v1 as components


# Paths to the logos
logo = "./images/logo4.png"

st.set_page_config(page_title="Compute", layout="wide")

###########################
# Add LOGO
###########################
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
                padding-top: 150px;
                background-position: 10px 10px;
                background-size: {width};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Call the add_logo function with the path to your local image
add_logo(logo, "200px")


df = pd.read_csv("./Cloud Carbon Footprint - Embodied Emissions.csv")

# Rename columns
df.columns = ['series', 'vm', 'CPU', 'memory', 'carbon_emission', 'carbon_emission2']

st.markdown(
    """
    <style>
    /* Style for the sidebar content */
    [data-testid="stSidebarContent"] {
        background-color: white; /*#bac9b9; Sidebar background color */
    }
    /* Set color for all text inside the sidebar */
    [data-testid="stSidebar"] * {
        color: #3b8bc2 !important;  /* Text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Change the background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d2e7ae;  /* #c0dc8f Light gray-green */
    }
    .custom-label{
        color: #3b8bc2;
        font-size: 18px;  /* Set the font size for text input, number input, and text area */
        padding: 10px;    /* Optional: adjust padding for better appearance */
    }
    p, li, span{
        color: #3b8bc2;
        font-size: 18px;  /* Set default font size */
        /* font-weight: bold;   Make the text bold */
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)
# Customizing the title with HTML/CSS to make it larger and green
st.markdown("<h1 style='color: #4b7170;font-size: 60px;'>Background</h1>", unsafe_allow_html=True)

# Overview
st.write("##### Data centers are critical infrastructure that significantly contribute to global carbon emissions. Operators lack effective tools to track, manage, and optimize their carbon footprint.")

################################
# Data Visualization
################################

# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Embodied Carbon</h3>",
    unsafe_allow_html=True,
)    

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
    
# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Power Usage Effectiveness</h3>",
    unsafe_allow_html=True,
)  

# Define the URL to the Tableau public visualization
tableau_url = "https://public.tableau.com/views/PUE_State/Dashboard1"

# Embed the Tableau dashboard using an iframe
components.html(
    f"""
    <iframe src="{tableau_url}?:embed=y&:display_count=yes&:showVizHome=no"
            width="1000" height="827" style="border: none;"></iframe>
    """,
    height=830,
)


# Define the URL to the Tableau public visualization
tableau_url = "https://public.tableau.com/views/Num_Data_centers/Dashboard1"

# Set desired width and height
viz_width = 1200  # Change to your preferred width
viz_height = 820  # Change to your preferred height

# Embed the Tableau dashboard using an iframe
components.html(
    f"""
    <iframe src="{tableau_url}?:embed=y&:display_count=no&:showVizHome=no&:toolbar=no"
            width="{viz_width}" height="{viz_height}" style="border: none;"></iframe>
    """,
    height=viz_height + 10,
)

################################
# Data Model
################################

# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Data Model</h3>",
    unsafe_allow_html=True,
)    
st.image("./images/data_model.png")


################################
# Model Iteration and Accuracy
################################

# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Model Performance Metrics</h3>",
    unsafe_allow_html=True,
)  

# Sample data
data = {
    'Model Type': ['Linear Regression', 'Decision Tree', 'Random Forest', 'XGBoost'],
    'MSE': [0.23, 0.10, 0.08, 0.06],
    'RMSE': [0.47, 0.31, 0.29, 0.25],
    'R-squared': [0.53, 0.80, 0.83, 0.87],
}

# Create a DataFrame
df = pd.DataFrame(data)
st.dataframe(df)  # or use st.table(df) for a static table

################################
# Citation
################################


# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Citation</h3>",
    unsafe_allow_html=True,
)  
