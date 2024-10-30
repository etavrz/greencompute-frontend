import streamlit as st
import pandas as pd
import numpy as np
import base64
import requests
import pickle


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
        "Formula: Total Carbon Emission = PUE * Server Electricity Consumption + Cloud Carbon Emission"
    )

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


def determine_combination(chiller_type, air_economization, water_economization):
    if air_economization == "Yes" and chiller_type == "Air-cooled chiller":
        return "Airside economizer + (air-cooled chiller)"
    elif air_economization == "Yes" and chiller_type == "Direct expansion system":
        return "Airside economizer + (direct expansion system)"
    elif air_economization == "Yes" and chiller_type == "Water-cooled chiller":
        return "Airside economizer + (water-cooled chiller)"
    elif chiller_type == "Direct expansion system":
        return "Direct expansion system"
    elif chiller_type == "Water-cooled chiller" and water_economization == "Yes":
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
        "How many chips does each server have?",
        "What many cores does each server have?",
    ],
    "PUE Model": [
        "Where is your data center located?",
        "Does the cooling system utilize water-side economization?",
        "Does the cooling system utilize air-side economization?",
        "What type of chiller is used?",
    ],
}

# Display questions and gather inputs for "Server Energy and Carbon" model
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Server Energy and Carbon Data</h3>",
    unsafe_allow_html=True,
)

# Use three columns for inputs in the Server Energy and Carbon section
server_col1, server_col2, server_col3 = st.columns(3)

with server_col1:
    num_servers = st.number_input(
        questions["Server Energy and Carbon"][0], min_value=0, step=1
    )
    avg_cpus = st.number_input(
        questions["Server Energy and Carbon"][1], min_value=0, step=1
    )

with server_col2:
    memory_input = st.number_input(
        questions["Server Energy and Carbon"][2], min_value=0, step=100
    )
    num_chips = st.number_input(
        questions["Server Energy and Carbon"][3], min_value=0, step=50
    )

with server_col3:
    num_cores = st.number_input(
        questions["Server Energy and Carbon"][4], min_value=0, step=50
    )

# Add a horizontal line separator
st.markdown("<hr>", unsafe_allow_html=True)

# Display questions and gather inputs for "PUE Model"
st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>PUE Model Input Data</h3>",
    unsafe_allow_html=True,
)

# Use three columns for inputs in the PUE Model section
pue_col1, pue_col2, pue_col3 = st.columns(3)

with pue_col1:
    water_economization = st.radio(questions["PUE Model"][1], ["Yes", "No"])
    air_economization = st.radio(questions["PUE Model"][2], ["Yes", "No"])

with pue_col2:
    location = st.selectbox(questions["PUE Model"][0], states)

with pue_col3:
    chiller_type = st.selectbox(
        questions["PUE Model"][3],
        ["Air-cooled chiller", "Direct expansion system", "Water-cooled chiller"],
    )


# Add a button to submit the inputs
if st.button("Submit"):
    st.success("Thank you for your submission!")

    # Optionally, display the collected data for confirmation
    st.write("### Submitted Data")
    st.write("**Server Energy and Carbon**")
    st.write(f"Number of Servers: {num_servers}")
    st.write(f"Average CPUs: {avg_cpus}")
    st.write(f"Average Memory (MB): {memory_input}")

    st.write("**PUE Model**")
    st.write(f"Location: {location}")
    st.write(f"Water-side Economization: {water_economization}")
    st.write(f"Air-side Economization: {air_economization}")
    st.write(f"Chiller Type: {chiller_type}")

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
        {"Memory (GB)": [memory_input], "# Cores": [num_cores], "# Chips": [num_chips]}
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
                "# Chips": num_chips,
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
                "# Chips": num_chips,
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

    chiller_economizer_input = determine_combination(
        chiller_type, air_economization, water_economization
    )
    input_data3 = pd.DataFrame(columns=chiller_economizer + states)

    # Create a row of zeros
    input_data3.loc[0] = 0

    # Set the appropriate dummy variables to 1 based on user input
    input_data3.loc[0, chiller_economizer_input] = 1
    input_data3.loc[0, location] = 1

    json_data = input_data3.to_dict(orient="records")[0]

    ##### may need to Change ######
    try:
        response_pue = requests.post(
            "http://localhost:8000/ml/carbon-emissions",
            json=json_data,
        ).json()
        pue_pred = response_pue["PUE"]

    except requests.exceptions.RequestException:
        # Load the trained xgb model from the file
        def load_cloud_model():
            with open("xgb_pue_model.pkl", "rb") as file:
                pue_model = pickle.load(file)
            return pue_model

        # Load the model once the app is launched
        pue_model = load_cloud_model()
        pue_pred = pue_model.predict(input_data3)[0]

    ###################################################
    # Output
    ###################################################

    total_carbon_emission = (
        pue_pred * server_pred_rf * num_servers + carbon_emission_pred_xgb
    )
    st.write(
        f"<h4 style='color: #3b8bc2;'>The carbon footprint of your data center is {total_carbon_emission:.2f} kgCO2 </h4>",
        unsafe_allow_html=True,
    )

    # Create three columns to display the predicted outputs
    col1, col2, col3 = st.columns(3)

    # Column 1: Predicted Cloud Carbon Emission
    with col1:
        st.write(
            f"Predicted Cloud Carbon Emission: {carbon_emission_pred_xgb:.2f} kgCO2"
        )

    # Column 2: Predicted IT Server Electricity Consumption
    with col2:
        st.write(
            f"Predicted Annual Total Energy per Server: {server_pred_rf:.2f} Watts"
        )

    # Column 3: Predicted PUE
    with col3:
        st.write(f"Predicted PUE: {pue_pred:.2f}")


###################################################
# Recommendation
###################################################

# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

st.write(
    "<h3 style='color: #4b7170;font-style: italic;'>Get Your Personalized Recommendations</h3>",
    unsafe_allow_html=True,
)

# Output Recommendation
if st.button("Get Recommendations"):
    # Display the recommendations
    st.write("#### we recommend...")

    # Horizontal line
    st.markdown("<hr>", unsafe_allow_html=True)

    st.write(
        "<h3 style='color: #4b7170;font-style: italic;'>Additional Questions</h3>",
        unsafe_allow_html=True,
    )
    questions2 = [
        "Do you maintain an inventory of servers in your data center?",
        "What type of memory do most servers have? (SSD or HDD)",
        "What is the typical temperature of air supplied to server racks?",
        "What is the typical return air temperature to cooling coils?",
        "Do you have active, working humidification controls?",
        "Do you have active, working dehumidification controls?",
        "What type of cooling system do you have? (Air-Cooled DX, Water-Cooled DX, Evaporatively-Cooled DX, or Chilled Water)",
        "What is the chilled water leaving temperature?",
        "What type of UPS do you have? (Double Conversion, Double Conversion + Filter, Delta Conversion, Rotary, None)",
        "What is the average load factor of the UPS?",
    ]

    server_inv = st.radio(questions2[0], ["Yes", "No"])
    memory_type = st.selectbox(questions2[1], ["SSD", "HDD"])
    supply_temp = st.number_input(questions2[2], min_value=-50, step=1)
    return_temp = st.number_input(questions2[3], min_value=-50, step=1)
    cooling_system = st.selectbox(
        questions2[4],
        [
            "Air-Cooled DX",
            "Water-Cooled DX",
            "Evaporatively-Cooled DX",
            "Chilled Water",
        ],
    )
    humidification = st.radio(questions2[5], ["Yes", "No"])
    dehumidification = st.radio(questions2[6], ["Yes", "No"])
    chilled_water_temp = st.number_input(questions2[7], min_value=-50, step=1)
    avg_load_factor = st.number_input(questions2[8], min_value=0, step=1)
    ups_type = st.selectbox(
        questions2[9],
        [
            "Double Conversion",
            "Double Conversion + Filter",
            "Delta Conversion",
            "Rotary",
            "None",
        ],
    )
