import streamlit as st
import pandas as pd
import numpy as np
import base64
import requests
import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time
from millify import millify


# Paths to the logos
logo = "./images/logo4.png"


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

#############################
# Change the background color
#############################

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
st.markdown(
    "<h1 style='color: #4b7170;font-size: 60px;'>GreenCompute</h1>",
    unsafe_allow_html=True,
)
st.write(
    "<h4 style='color: #4b7170;font-style: italic;font-size: 24px;'>Estimate carbon emission amount for your data centers and get personalized recommendations</h4>",
    unsafe_allow_html=True,
)

###########################
# Add Simplified Data Model
###########################

# Initialize session state variable if it doesn't exist
if "show_image" not in st.session_state:
    st.session_state.show_image = False

# Create a button
if st.button("How we make our predictions"):
    # Toggle the visibility state
    st.session_state.show_image = not st.session_state.show_image

# Display the image based on the state
if st.session_state.show_image:
    st.image("./images/data_model_simple.png", width=800)
    st.write(
        "Formula: Total Carbon Emission = PUE * Server Electricity Consumption + Embodied Carbon"
    )


# Initialize the session state for displaying the typing effect
if "show_text_once" not in st.session_state:
    st.session_state.show_text_once = True

# Placeholder for typing effect and counting effect on the same line
text_placeholder = st.empty()

# Display the text with a typing effect if it's the first page load/refresh
if st.session_state.show_text_once:
    # Typing effect for the text
    text = "Enter your data center's Server Electricity Consumption, Embodied Carbon, and Power Usage Efficiency (PUE) details to generate a carbon emissions prediction."
    typed_text = ""
    for char in text:
        typed_text += char
        text_placeholder.markdown(
            f"<h4 style='color: #3b8bc2;'>{typed_text}</h4>", unsafe_allow_html=True
        )
        time.sleep(0.01)  # Adjust for typing speed

    # Set the session state to prevent showing it again
    st.session_state.show_text_once = False
else:
    # Display static text after the first load/refresh
    text_placeholder.markdown(
        "<h4 style='color: #3b8bc2;'>Enter your data center's Server Electricity Consumption, Embodied Carbon, and Power Usage Efficiency (PUE) details to generate a carbon emissions prediction.</h4>",
        unsafe_allow_html=True,
    )

###########################
# Preparation for modeling
###########################

# Define possible categories for dummies
chiller_economizer = [
    "Air-cooled chiller",
    "Airside economizer + (air-cooled chiller)",
    "Airside economizer + (direct expansion system)",
    "Airside economizer + (water-cooled chiller)",
    "Direct expansion system",
    "Water-cooled chiller",
    "Waterside economizer + (water-cooled chiller)",
]


def determine_combination(chiller_type, economization):
    if (
        economization == "Air-side Economization"
        and chiller_type == "Air-cooled chiller"
    ):
        return "Airside economizer + (air-cooled chiller)"
    elif (
        economization == "Air-side Economization"
        and chiller_type == "Direct expansion system"
    ):
        return "Airside economizer + (direct expansion system)"
    elif (
        economization == "Air-side Economization"
        and chiller_type == "Water-cooled chiller"
    ):
        return "Airside economizer + (water-cooled chiller)"
    elif chiller_type == "Direct expansion system":
        return "Direct expansion system"
    elif (
        chiller_type == "Water-cooled chiller"
        and economization == "Water-side Economization"
    ):
        return "Waterside economizer + (water-cooled chiller)"
    else:
        return chiller_type


states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]


###########################
# Add User Inputs
###########################

# Define the questions by model type #?# not working
st.markdown(
    """
    <style>
    .prompt-text {
        color:#3b8bc2;  /* Set text color */
        font-size: 18px;  /* Set font size */
        /*  font-weight: bold;  Make text bold */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Questions
questions = {
    "Server Energy and Carbon": [
        "About how many servers are located in your data center?",
        "On average, how many CPUs do servers in your data center have?",
        "On average, how much memory does each server contain?",
        "What many cores does each server have?",
    ],
    "PUE Model": [
        "Where is your data center located?",
        "What type of cooling system is used utilize water-side economization?",
        "Does the cooling system utilize air-side economization?",
        "What type of chiller is used?",
    ],
}

# Add a horizontal line separator
st.markdown("<hr>", unsafe_allow_html=True)

# Use three columns for inputs in the Server Energy and Carbon section
server_col1, separator, server_col2 = st.columns([2.2, 0.1, 2.2])

with server_col1:
    # Display questions and gather inputs for "Server Energy and Carbon" model
    st.write(
        "<h3 style='color: #4b7170;font-style: italic;'>Server Electricity and Embodied Carbon Input</h3>",
        unsafe_allow_html=True,
    )

    # Question list
    num_servers = st.number_input(
        questions["Server Energy and Carbon"][0], min_value=1, step=1
    )
    avg_cpus = st.number_input(
        questions["Server Energy and Carbon"][1], min_value=1, step=1
    )
    memory_input = st.number_input(
        questions["Server Energy and Carbon"][2], min_value=1, step=100
    )
    num_cores = st.number_input(
        questions["Server Energy and Carbon"][3], min_value=1, step=50
    )

# Add a vertical separator line
with separator:
    st.markdown(
        "<style>div.separator { height: 40vh; border-left: 1px solid #4b7170; margin-left: auto; margin-right: auto; }</style>"
        "<div class='separator'></div>",
        unsafe_allow_html=True,
    )


with server_col2:
    # Display questions and gather inputs for "PUE Model"
    st.write(
        "<h3 style='color: #4b7170;font-style: italic;'>Power Usage Efficiency Input</h3>",
        unsafe_allow_html=True,
    )

    economization = st.selectbox(
        questions["PUE Model"][1],
        ["Water-side Economization", "Air-side Economization"],
    )
    location = st.selectbox(questions["PUE Model"][0], states)
    chiller_type = st.selectbox(
        questions["PUE Model"][2],
        ["Air-cooled chiller", "Direct expansion system", "Water-cooled chiller"],
    )


###########################
# Predictions
###########################

# Create a DataFrame for dummy variables
input_data_pue = pd.DataFrame(columns=chiller_economizer + states)

# Create a row of zeros
input_data_pue.loc[0] = 0

# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Estimate Carbon Footprint</h3>",
    unsafe_allow_html=True,
)

# Predict Cloud Carbon Emission
if st.button("Calculate Carbon Emission"):
    ###################################################
    # Predict log-transformed carbon emission
    ###################################################

    # Prepare the input data for prediction
    input_data = pd.DataFrame({"memory": [memory_input], "CPU": [avg_cpus]})

    try:
        response = requests.post(
            "http://localhost:8000/ml/carbon-emissions",
            json={"memory": memory_input, "cpu": avg_cpus},
        ).json()

        # Reverse the log transformation to get the actual carbon emission
        carbon_emission_pred_xgb = np.exp(response["carbon"])

    except requests.exceptions.RequestException:
        # Load the trained XGBoost model from the file
        def load_cloud_model():
            with open("xgb_carbon_model.pkl", "rb") as file:
                xgb_model = pickle.load(file)
            return xgb_model

        # Load the model once the app is launched
        xgb_model = load_cloud_model()
        carbon_emission_pred_xgb = np.exp(xgb_model.predict(input_data)[0])

    ###################################################
    # Prepare the input data for electricity prediction
    ###################################################

    input_data2 = pd.DataFrame(
        {"Memory (GB)": [memory_input], "# Cores": [num_cores], "# Chips": [avg_cpus]}
    )

    ######################
    # Step1: IT Electricity
    ######################

    ##### may need to Change ######
    try:
        response_server = requests.post(
            "http://localhost:8000/ml/carbon-emissions",
            json={
                "Memory (GB)": memory_input,
                "# Cores": num_cores,
                "# Chips": avg_cpus,
            },
        ).json()
        server_pred_rf = response_server["Average watts @ 50% of target load"]

    except requests.exceptions.RequestException:
        # Load the trained random forest model from the file
        def load_electricity_model():
            with open("gbr_it_electricity_model.pkl", "rb") as file:
                gbr_electricity_model = pickle.load(file)
            return gbr_electricity_model

        # Load the model once the app is launched
        gbr_electricity_model = load_electricity_model()
        server_pred_rf = gbr_electricity_model.predict(input_data2)[0]

    ######################
    # Step2: Active Idle
    ######################

    ##### may need to Change ######
    try:
        response_idle = requests.post(
            "http://localhost:8000/ml/carbon-emissions",
            json={
                "Memory (GB)": memory_input,
                "# Cores": num_cores,
                "# Chips": avg_cpus,
            },
        ).json()
        idle_pred_rf = response_idle["Average watts @ active idle"]

    except requests.exceptions.RequestException:
        # Load the trained random forest model from the file
        def load_idle_model():
            with open("rf_activeidle_model.pkl", "rb") as file:
                rf_activeidle_model = pickle.load(file)
            return rf_activeidle_model

        # Load the model once the app is launched
        rf_activeidle_model = load_idle_model()
        idle_pred_rf = rf_activeidle_model.predict(input_data2)[0]

    ######################
    # Step2: Annual Power
    ######################

    # calculate annual average power
    annual_average_power = 0.3 * server_pred_rf + 0.7 * idle_pred_rf

    # Annual Total Energy
    annual_total_energy = annual_average_power * 8760 * 1.05 * 1.20

    ###################################################
    # Predict PUE
    ###################################################

    # Prepare raw input data as required by the pipeline (without manual encoding)
    input_data3 = pd.DataFrame(
        {"Cooling System": [chiller_type], "state_name": [location]}
    )

    json_data = input_data3.to_dict(orient="records")[0]

    # Attempt prediction via API, fallback to local model if API fails
    try:
        response_pue = requests.post(
            "http://localhost:8000/ml/carbon-emissions",
            json=json_data,
        ).json()
        pue_pred = response_pue["PUE"]

    except requests.exceptions.RequestException:
        # Load the trained pipeline model from the file
        def load_cloud_model():
            with open("xgb_pue_sklearn.pkl", "rb") as file:
                pue_model = pickle.load(file)
            return pue_model

        # Load and use the pipeline model to make a prediction
        pue_model = load_cloud_model()
        pue_pred = pue_model.predict(input_data3)[0]

    print(f"Predicted PUE: {pue_pred}")

    ###################################################
    # Output
    ###################################################

    # Calculate the total carbon emission
    total_carbon_emission = (
        pue_pred * server_pred_rf * num_servers + carbon_emission_pred_xgb
    )

    # Placeholder for typing effect and counting effect on the same line
    combined_placeholder = st.empty()

    # Typing effect for the text
    text = "The carbon footprint of your data center is "
    typed_text = ""
    for char in text:
        typed_text += char
        combined_placeholder.markdown(
            f"<h4 style='color: #3b8bc2;'>{typed_text}</h4>", unsafe_allow_html=True
        )
        time.sleep(0.01)  # Adjust for typing speed

    # Counting effect for the total emission value
    final_value = round(total_carbon_emission, 2)
    current_value = 0.0
    increment = final_value / 100  # Adjust speed of the counter

    while current_value < final_value:
        current_value = min(current_value + increment, final_value)
        combined_placeholder.markdown(
            f"<h4 style='color: #3b8bc2;'>{typed_text}{current_value:.2f} kgCO₂</h4>",
            unsafe_allow_html=True,
        )
        time.sleep(0.02)  # Adjust for counting speed

    # Use three columns for inputs in the Server Energy and Carbon section
    col1, separator, col2 = st.columns([2.2, 0.1, 2.2])

    # Column 1: Predicted Cloud Carbon Emission & visualization
    with col1:
        #################
        # Visualizations
        #################

        # Assume some ranges for data center emissions (in metric tons of CO2 per year)
        min_emission = 1000  # Lower end for a small data center
        max_emission = 1000000  # Upper end for a large hyperscale data center

        # Create a gradient color map from green to orange
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "emission_cmap", ["green", "orange", "red"]
        )

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(10, 0.82))

        # Generate data points for the spectrum (x-axis)
        x = np.linspace(min_emission, max_emission, 500)
        y = np.zeros_like(x)

        # Plot the gradient spectrum as a colored line
        for i in range(len(x) - 1):
            ax.plot(x[i : i + 2], y[i : i + 2], color=cmap(i / len(x)), linewidth=28)

        # Add a vertical line for the predicted emission
        ax.axvline(
            total_carbon_emission,
            color="#3b8bc2",
            linestyle="-",
            linewidth=4,
            label=f"Prediction: {total_carbon_emission} kgCO₂",
        )

        # Add labels at both ends of the spectrum
        ax.text(
            min_emission,
            0.1,
            f"Small DC\n({min_emission} kgCO₂)",
            ha="center",
            color="green",
            fontsize=15,
        )
        ax.text(
            max_emission,
            0.1,
            f"Hyperscale DC\n({max_emission} kgCO₂)",
            ha="center",
            color="red",
            fontsize=15,
        )

        # Label the prediction line
        ax.text(
            total_carbon_emission,
            -0.12,
            f"{total_carbon_emission:.2f} kgCO₂",
            ha="center",
            color="#3b8bc2",
            fontsize=15,
        )

        # Hide the y-axis and spines for a cleaner look
        ax.axis("off")

        # Display the figure in Streamlit
        st.pyplot(fig)

        # Add a horizontal line separator
        st.markdown("<hr>", unsafe_allow_html=True)

        # Prediction reulsts
        cols = st.columns(3)

        cols[0].metric(
            "Predicted Cloud Carbon Emission kgCO2",
            millify(carbon_emission_pred_xgb, precision=2),
        )
        cols[1].metric("Predicted Annual Total Energy per Server Watts", server_pred_rf)
        cols[2].metric("Predicted PUE:", millify(pue_pred, precision=2))

    # Add a vertical separator line
    with separator:
        st.markdown(
            "<style>div.separator { height: 28vh; border-left: 1px solid #4b7170; margin-left: auto; margin-right: auto; }</style>"
            "<div class='separator'></div>",
            unsafe_allow_html=True,
        )

    # Column 2: Environmental equivalents
    with col2:
        # Calculate interpretation: miles driven equivalent
        miles_per_kg_co2 = 2.5  # Approximate miles driven per metric ton of CO₂
        equivalent_miles = total_carbon_emission * miles_per_kg_co2

        # Calculate interpretation: household power equivalent
        daily_household_kg_co2 = (
            18  # Approximate daily CO₂ footprint for a typical household in kg
        )
        equivalent_household_days = total_carbon_emission / daily_household_kg_co2

        # Calculate interpretation: tree sequestration equivalent
        annual_tree_sequestration_kg_co2 = (
            22  # Approximate CO₂ absorbed by a tree per year in kg
        )
        equivalent_trees = total_carbon_emission / annual_tree_sequestration_kg_co2

        # Display the interpretation
        st.write(
            "<h4 style='color: #3b8bc2;'>🌍 Equivalent Carbon Emissions 🌍</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
        Your predicted emission of **{total_carbon_emission:.2f}** kgCO₂ is approximately equal to:

        •  🚗 Driving a typical car for **{equivalent_miles:,.0f} miles** \\
        •  🏡 Powering an average household for **{equivalent_household_days:,.0f} days**\\
        •  🌲 Sequestering carbon equivalent to **{equivalent_trees:,.0f} trees** over a year


        These estimates provide a tangible sense of the environmental impact of your data center's carbon emissions.
        """,
            unsafe_allow_html=True,
        )


###################################################
# Recommendation
###################################################

# Horizontal line
# st.markdown("<hr>", unsafe_allow_html=True)

# st.write(
# "<h3 style='color: #4b7170;font-style: italic;'>Get Your Personalized Recommendations</h3>",
# unsafe_allow_html=True,)

# Output Recommendation
# if st.button("Get Recommendations"):
# Display the recommendations
# st.write("#### we recommend...")

# Horizontal line
# st.markdown("<hr>", unsafe_allow_html=True)
