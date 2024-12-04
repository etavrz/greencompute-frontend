import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import greencompute_frontend.formatting as fmt

# Paths to the logos
logo = "./greencompute_frontend/images/logo4.png"
fmt.add_logo(logo)

df = pd.read_csv("./greencompute_frontend/data/cloud_embodied_emissions.csv")

# Rename columns
df.columns = ["series", "vm", "CPU", "memory", "carbon_emission", "carbon_emission2"]

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
    unsafe_allow_html=True,
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
# Summary
################################
# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>About GreenCompute</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    """
GreenCompute is dedicated to addressing the critical environmental challenge of carbon emissions in data centers. Data centers, essential to our digital infrastructure, consume massive amounts of electricity to power servers and cooling systems. These facilities contribute to carbon emissions that are classified into three categories:

•  Scope 1: Direct emissions from on-site fuel combustion, such as backup generators.\\
•  Scope 2: Indirect emissions from purchased electricity, often the largest contributor for data centers.\\
•  Scope 3: Indirect emissions from the entire supply chain, including embodied carbon in hardware manufacturing and emissions from logistics.\\

Our platform provides a comprehensive solution to measure and reduce these emissions, empowering data center operators and customers with actionable insights:

Carbon Emission Prediction – Leveraging three advanced sub-models, we predict annual carbon emissions by aggregating outputs for IT electricity consumption, embodied carbon, and Power Usage Effectiveness (PUE). Inputs such as memory, CPUs, location, and other factors are used to refine these predictions.
Energy Efficiency Recommendations – Our LLM-powered chatbot delivers tailored guidance to optimize energy use and reduce emissions, helping companies improve efficiency and sustainability.

By providing clear visibility into carbon emissions and actionable pathways for reduction, GreenCompute supports businesses in meeting sustainability goals while addressing the significant environmental impact of data centers.
 """,
    unsafe_allow_html=True,
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
st.image("./greencompute_frontend/images/data_model.png")

################################
# Data Visualization
################################
# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Exploratory Data Analysis</h3>",
    unsafe_allow_html=True,
)

### Embodied Carbon ###
st.write(
    "<h4 style='color: #4b7170;font-style: italic;'>1. Embodied Carbon</h4>",
    unsafe_allow_html=True,
)

with st.expander("Click to see the visualization..."):
    # Create two columns (left and right)
    col1, col2 = st.columns(2)

    # Scatter plot for Column A vs Column B
    with col1:
        st.write(
            "<h5 style='color: #3b8bc2;font-style: italic;'>Carbon Emission vs. # of CPUs</h5>",
            unsafe_allow_html=True,
        )
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
        st.write(
            "<h5 style='color: #3b8bc2;font-style: italic;'> Carbon Emission vs. Memory</h5>",
            unsafe_allow_html=True,
        )
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

### IT ###
st.write(
    "<h4 style='color: #4b7170;font-style: italic;'>2. IT Electricity Consumption</h4>",
    unsafe_allow_html=True,
)

with st.expander("Click to see the visualization..."):
    st.image("./greencompute_frontend/images/IT.png", width=600)

### PUE ###
st.write(
    "<h4 style='color: #4b7170;font-style: italic;'>2. Power Usage Effectiveness</h4>",
    unsafe_allow_html=True,
)

with st.expander("Click to see the visualization..."):
    # Define the URL to the Tableau public visualization
    tableau_url = "https://public.tableau.com/views/PUE_State/Dashboard1"

    # Embed the Tableau dashboard using an iframe
    components.html(
        f"""
        <iframe src="{tableau_url}?:embed=y&:display_count=yes&:showVizHome=no"
        width="900" height="727" style="border: none;"></iframe>
        """,
        height=730,
    )


#     # Define the URL to the Tableau public visualization
#     tableau_url = "https://public.tableau.com/views/Num_Data_centers/Dashboard1"

#     # Set desired width and height
#     viz_width = 1200  # Change to your preferred width
#     viz_height = 820  # Change to your preferred height

#     # Embed the Tableau dashboard using an iframe
#     components.html(
#         f"""
#         <iframe src="{tableau_url}?:embed=y&:display_count=no&:showVizHome=no&:toolbar=no"
#             width="{viz_width}" height="{viz_height}" style="border: none;"></iframe>
#         """,
#         height=viz_height + 10,
#     )


################################
# Model Iteration and Accuracy
################################

# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Model Performance Metrics</h3>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1.5, 1])

# Embodied carbon data
with col1:
    st.write(
        "<h4 style='color: #3b8bc2;font-style: italic;'>1. Embodied Carbon</h4>",
        unsafe_allow_html=True,
    )
    data1 = {"Model Type": ["Linear Regression", "Decision Tree", "Random Forest", "XGBoost"], "MSE": [0.23, 0.10, 0.08, 0.06], "R-squared": [0.53, 0.80, 0.83, 0.87]}
    # Create a DataFrame
    df1 = pd.DataFrame(data1)
    df1.set_index("Model Type", inplace=True)
    st.dataframe(df1)

# Embodied carbon data
with col2:
    st.write(
        "<h4 style='color: #3b8bc2;font-style: italic;'>2. IT Electricity & Idle Power</h4>",
        unsafe_allow_html=True,
    )
    data2 = {
        "Output": ["IT Electricity", "IT Electricity", "IT Electricity", "Active Idle Power", "Active Idle Power", "Active Idle Power"],
        "Model Type": ["Random Forest", "Gradient Boosting Regressor", "Neural Network", "Random Forest", "Gradient Boosting Regressor", "K-NN"],
        "MSE": [14409.11, 8339.51, 18455.5, 3794.67, 5573.91, 21496.27],
        "R-squared": [0.96, 0.97, 0.94, 0.92, 0.89, 0.57],
    }
    # Create a DataFrame
    df2 = pd.DataFrame(data2)
    df2.set_index("Output", inplace=True)
    st.dataframe(df2)

# Embodied carbon data
with col3:
    st.write(
        "<h4 style='color: #3b8bc2;font-style: italic;'>3. PUE</h4>",
        unsafe_allow_html=True,
    )
    data3 = {"Model Type": ["Linear Regression", "Decision Tree", "Random Forest", "XGBoost"], "MSE": [0.026, 0.025, 0.025, 0.025], "R-squared": [0.633, 0.644, 0.644, 0.644]}
    # Create a DataFrame
    df3 = pd.DataFrame(data3)
    df3.set_index("Model Type", inplace=True)
    st.dataframe(df3)

################################
# Citation
################################


# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Citation</h3>",
    unsafe_allow_html=True,
)
