import datetime
import json
import pickle
import time

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import streamlit as st
from loguru import logger
from millify import millify

import greencompute_frontend.formatting as fmt
from greencompute_frontend.constants import STATES

# Apply different formatting events
logo = "./greencompute_frontend/images/logo4.png"
fmt.add_logo(logo)
fmt.sidebar()
fmt.background()
fmt.title("GreenCompute")


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
    st.image("./greencompute_frontend/images/data_model_simple.png", width=800)
    st.write("Formula: Total Carbon Emission = PUE * Server Electricity Consumption + Embodied Carbon")


# Initialize the session state for displaying the typing effect
if "show_text_once" not in st.session_state:
    st.session_state.show_text_once = True

# Placeholder for typing effect and counting effect on the same line
text_placeholder = st.empty()

# Display the text with a typing effect if it's the first page load/refresh
if st.session_state.show_text_once:
    # Typing effect for the text
    text = "Enter your data center's Server Electricity Consumption, Embodied Carbon, and Power Usage Efficiency (PUE) details to generate a carbon emissions prediction."
    text_placeholder.markdown(f"<h4 style='color: #3b8bc2;'>{text}</h4>", unsafe_allow_html=True)

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
    if economization == "Air-side Economization" and chiller_type == "Air-cooled chiller":
        return "Airside economizer + (air-cooled chiller)"
    elif economization == "Air-side Economization" and chiller_type == "Direct expansion system":
        return "Airside economizer + (direct expansion system)"
    elif economization == "Air-side Economization" and chiller_type == "Water-cooled chiller":
        return "Airside economizer + (water-cooled chiller)"
    elif chiller_type == "Direct expansion system":
        return "Direct expansion system"
    elif chiller_type == "Water-cooled chiller" and economization == "Water-side Economization":
        return "Waterside economizer + (water-cooled chiller)"
    else:
        return chiller_type


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
    num_servers = st.number_input(questions["Server Energy and Carbon"][0], min_value=1, step=1)
    avg_cpus = st.number_input(questions["Server Energy and Carbon"][1], min_value=1, step=1)
    memory_input = st.number_input(questions["Server Energy and Carbon"][2], min_value=1, step=100)
    num_cores = st.number_input(questions["Server Energy and Carbon"][3], min_value=1, step=50)

# Add a vertical separator line
with separator:
    st.markdown(
        "<style>div.separator { height: 40vh; border-left: 1px solid #4b7170; margin-left: auto; margin-right: auto; }</style>" "<div class='separator'></div>",
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
    location = st.selectbox(questions["PUE Model"][0], STATES)
    chiller_type = st.selectbox(
        questions["PUE Model"][2],
        ["Air-cooled chiller", "Direct expansion system", "Water-cooled chiller"],
    )


###########################
# Predictions
###########################

# Create a DataFrame for dummy variables
input_data_pue = pd.DataFrame(columns=chiller_economizer + STATES)

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
        carbon_emission_pred_xgb = np.exp(response["prediction"])

    except Exception as e:
        logger.error(f"API request failed: {e}. Using local model instead.")

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

    input_data2 = pd.DataFrame({"Memory (GB)": [memory_input], "# Cores": [num_cores], "# Chips": [avg_cpus]})

    ######################
    # Step1: IT Electricity
    ######################

    ##### may need to Change ######
    try:
        response_server = requests.post(
            "http://localhost:8000/ml/it-electricity",
            json={
                "memory": memory_input,
                "cores": num_cores,
                "cpu": avg_cpus,
            },
        ).json()
        server_pred_rf = response_server["prediction"]

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
            "http://localhost:8000/ml/active-idle",
            json={
                "memory": memory_input,
                "cores": num_cores,
                "cpu": avg_cpus,
            },
        ).json()
        idle_pred_rf = response_idle["prediction"]

    except Exception as e:
        logger.error(f"API request failed: {e}. Using local model instead.")

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
    # Updated to multiply by number of servers here
    annual_total_energy = annual_average_power * 8760 * 1.05 * 1.20 * num_servers / 1000

    ###################################################
    # Predict PUE
    ###################################################

    # Prepare raw input data as required by the pipeline (without manual encoding)
    input_data3 = pd.DataFrame({"Cooling System": [chiller_type], "state_name": [location]})

    json_data = input_data3.to_dict(orient="records")[0]
    logger.debug(json_data)

    # Attempt prediction via API, fallback to local model if API fails
    try:
        response_pue = requests.post(
            "http://localhost:8000/ml/pue",
            json=json_data,
        ).json()
        pue_pred = response_pue["prediction"]

    except Exception as e:
        logger.error(f"API request failed: {e}. Using local model instead.")

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
    # Placeholder value of 0.86 lbCO2/kWh
    total_carbon_emission = annual_total_energy * 0.86 * 0.455 + carbon_emission_pred_xgb

    # Placeholder for typing effect and counting effect on the same line
    combined_placeholder = st.empty()

    # Typing effect for the text
    text = "The carbon footprint of your data center is "
    typed_text = ""
    for char in text:
        typed_text += char
        combined_placeholder.markdown(f"<h3 style='color: #3b8bc2;'>{typed_text}</h3>", unsafe_allow_html=True)
        time.sleep(0.01)  # Adjust for typing speed

    # Counting effect for the total emission value
    final_value = round(total_carbon_emission, 2)
    current_value = 0.0
    increment = final_value / 100  # Adjust speed of the counter

    while current_value < final_value:
        current_value = min(current_value + increment, final_value)
        combined_placeholder.markdown(
            f"<h3 style='color: #3b8bc2;'>{typed_text}{current_value:.2f} kgCO₂ per year</h3>",
            unsafe_allow_html=True,
        )
        time.sleep(0.01)  # Adjust for counting speed

    # Add a horizontal line separator
    empty_line_placeholder = st.empty()
    empty_line_placeholder.markdown("<p style='margin-top: 20px;'></p>", unsafe_allow_html=True)

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
        cmap = mcolors.LinearSegmentedColormap.from_list("emission_cmap", ["green", "orange", "red"])

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(10, 0.82))

        # Replace with your desired color
        background_color = "#d2e7ae"
        fig.patch.set_facecolor(background_color)

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
            fontsize=16,
        )
        ax.text(
            max_emission,
            0.1,
            f"Hyperscale DC\n({max_emission} kgCO₂)",
            ha="center",
            color="red",
            fontsize=16,
        )

        # Label the prediction line
        ax.text(
            total_carbon_emission,
            -0.12,
            f"{total_carbon_emission:.2f} kgCO₂",
            ha="center",
            color="#3b8bc2",
            fontsize=18,
            weight="bold",
        )

        # Hide the y-axis and spines for a cleaner look
        ax.axis("off")

        # Display the figure in Streamlit
        st.pyplot(fig)

        # Add a horizontal line separator
        st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

        ####################
        # Prediction reulsts
        ####################

        cols = st.columns(3)

        with cols[0]:
            st.markdown(
                f"""
                <div style="font-size: 18px; color: #4b7170; font-style: italic;font-weight: bold;">
                    Predicted Embodied Carbon:<br>
                    <span style="font-size: 28px; color: #3b8bc2;font-weight: bold;">
                        {millify(carbon_emission_pred_xgb, 2)} (kgCO₂)
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with cols[1]:
            st.markdown(
                f"""
                <div style="font-size: 18px; color: #4b7170; font-style: italic;font-weight: bold;">
                    Predicted Annual Total Energy:<br>
                    <span style="font-size: 28px; color: #3b8bc2;font-weight: bold;">
                        {millify(annual_total_energy, 2)} (kWh)
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with cols[2]:
            st.markdown(
                f"""
                <div style="font-size: 18px; color: #4b7170; font-style: italic;font-weight: bold;">
                    Predicted PUE:<br>
                    <span style="font-size: 28px; color: #3b8bc2;font-weight: bold;">
                        {millify(pue_pred, precision=2)}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Add a vertical separator line
    with separator:
        st.markdown(
            "<style>div.separator { height: 28vh; border-left: 1px solid #4b7170; margin-left: auto; margin-right: auto; }</style>" "<div class='separator'></div>",
            unsafe_allow_html=True,
        )

    # Column 2: Environmental equivalents
    with col2:
        # Calculate interpretation: miles driven equivalent
        miles_per_kg_co2 = 2.5  # Approximate miles driven per metric ton of CO₂
        equivalent_miles = total_carbon_emission * miles_per_kg_co2

        # Calculate interpretation: household power equivalent
        daily_household_kg_co2 = 18  # Approximate daily CO₂ footprint for a typical household in kg
        equivalent_household_days = total_carbon_emission / daily_household_kg_co2

        # Calculate interpretation: tree sequestration equivalent
        annual_tree_sequestration_kg_co2 = 22  # Approximate CO₂ absorbed by a tree per year in kg
        equivalent_trees = total_carbon_emission / annual_tree_sequestration_kg_co2

        # Display the interpretation
        st.write(
            "<h4 style='color: #4b7170;'>🌍 Equivalent Carbon Emissions 🌍</h4>",
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

    # Output
    output_data = {
        "Number of Servers": num_servers,
        "Average CPUs": avg_cpus,
        "Average Memory (GB)": memory_input,
        "Number of Cores": num_cores,
        "Cooling System": chiller_type,
        "Location": location,
        "Air-side Economization": economization,
        "Total Emission (kgCO₂)": round(total_carbon_emission, 2),
        "Predicted Embodied Carbon": round(carbon_emission_pred_xgb, 2),
        "Predicted Annual Total Energy": round(annual_total_energy, 2),
        "Predicted PUE": round(pue_pred, 2),
        "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Convert values that are of numpy 32 to floats and keep the rest as is
    output_data = {k: v.item() if isinstance(v, np.float32) else v for k, v in output_data.items()}

    json_string = json.dumps(output_data, indent=4)
    st.download_button(
        label="Save Results",
        file_name=f"greencompute_results_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json",
        mime="application/json",
        data=json_string,
    )
