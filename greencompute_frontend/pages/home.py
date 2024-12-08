import pandas as pd
import streamlit as st

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
        font-size: 18px;  /* Set default font size */
        /* font-weight: bold;   Make the text bold */
    }

    </style>
    """,
    unsafe_allow_html=True,
)
# Customizing the title with HTML/CSS to make it larger and green
st.markdown("<h1 style='color: #4b7170;font-size: 60px;'>GreenCompute</h1>", unsafe_allow_html=True)

# Overview
st.write("#### Data centers are critical infrastructure that significantly contribute to global carbon emissions. Operators lack effective tools to track, manage, and optimize their carbon footprint.")
st.markdown("<hr>", unsafe_allow_html=True)

columns = st.columns([0.4, 0.6])
with columns[0]:
    st.image(logo, width=400)
with columns[1]:
    st.markdown(
        "## *GreenCompute addresses this gap by offering a user-friendly, data-driven platform to estimate carbon emissions and provide actionable recommendations to optimize energy efficiency and minimize emissions.*"
    )
################################
# Summary
################################
# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "<h2 style='color: #4b7170;font-style: italic;'>About GreenCompute</h2>",
    unsafe_allow_html=True,
)

st.markdown(
    """
GreenCompute is dedicated to addressing the critical environmental challenge of carbon emissions in data centers. Data centers, essential to our digital infrastructure, consume massive amounts of electricity to power servers and cooling systems. These facilities contribute to carbon emissions that are classified into three categories:

- **Scope 1** : Direct emissions from on-site fuel combustion, such as backup generators.
- **Scope 2** : Indirect emissions from purchased electricity, often the largest contributor for data centers.
- **Scope 3** : Indirect emissions from the entire supply chain, including embodied carbon in hardware manufacturing and emissions from logistics.

Our platform provides a comprehensive solution to measure these emissions, empowering data center operators and customers with actionable insights. We do this via two AI powered features: carbon emissions estimates and energy efficiency recommendations. Click on the links below to try them out!

""",
    unsafe_allow_html=True,
)

columns = st.columns(2)

with columns[0]:
    with st.container(border=True):
        st.markdown(
            """
            #### Carbon Emission Estimates
            Leveraging our trained ML models, we estimate annual carbon emissions by aggregating predictions for IT electricity consumption, embodied carbon, and Power Usage Effectiveness (PUE). Inputs such as memory, CPUs, location, and other factors are used to refine these predictions.
            """
        )
        st.page_link("pages/compute.py", label="**Click here to compute your estimate**", icon="💻")
with columns[1]:
    with st.container(border=True):
        st.markdown(
            """
            #### Energy Efficiency Recommendations
            Our LLM-powered chatbot delivers expert guidance based on recommendations from the [Center of Expertise for Energey Efficiency and Data Centers](https://datacenters.lbl.gov/) to optimize energy use and reduce emissions, helping companies improve their data center operations.
            """
        )
        st.page_link("pages/chat.py", label="**Click here to get expert recommendations**", icon="🤖")
