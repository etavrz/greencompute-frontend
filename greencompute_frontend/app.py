import streamlit as st
import pandas as pd
import numpy as np
import base64
import pickle

# Paths to the logos
logo1 = "./images/logo1.png"
logo2 = "./images/logo2.png"
logo3 = "./images/logo3.png"

st.set_page_config(layout="wide")


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
                padding-top: 100px;
                background-position: 10px 10px;
                background-size: {width};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Call the add_logo function with the path to your local image
add_logo(logo1, "260px")

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
st.markdown("<h1 style='color: green;'>GreenCompute</h1>", unsafe_allow_html=True)
st.write(
    "<h5 style='color: grey;font-style: italic;'>Estimate carbon emission amount for your data centers and get personalized recommendations</h5>",
    unsafe_allow_html=True,
)
st.image("./images/data_model.png")

# User inputs for memory and CPU
# memory_input = st.number_input("Enter memory (MB)", min_value=0, max_value=55000, step=100)
# cpu_input = st.number_input("Enter CPU usage (%)", min_value=0, max_value=1000, step=50)

# Define the questions by model type
questions = {
    "Server Energy and Carbon": [
        "Do you maintain an inventory of servers in your data center?",
        "About how many servers are located in your data center?",
        "On average, how many CPUs do servers in your data center have?",
        "On average, how much memory does each server contain?",
        "What type of memory do most servers have? (SSD or HDD)",
    ],
    "PUE Model": [
        "Where is your data center located?",
        "What is the typical temperature of air supplied to server racks?",
        "What is the typical temperature of air returning to the cooling coils?",
        "Do you have active, working humidification controls? (yes, no)",
        "Do you have active, working dehumidification controls? (yes, no)",
        "Does the cooling system utilize water-side economization?",
        "Does the cooling system utilize air-side economization?",
        "What type of cooling system do you have? (Air-Cooled DX, Water-Cooled DX, Evaporatively-Cooled DX, or Chilled Water)",
        "What type of chiller is used? (air-cooled or water-cooled)",
        "What is the chilled water leaving temperature?",
        "What type of UPS do you have? (Double Conversion, Double Conversion + Filter, Delta Conversion, Rotary, None)",
        "What is the average load factor of the UPS?",
    ],
}

# Create columns for each model type
col1, col2 = st.columns(2)

# Display questions and gather inputs for "Server Energy and Carbon" model
with col1:
    st.write(
        "<h3 style='color: green;font-style: italic;'>Server Energy and Carbon Data</h3>",
        unsafe_allow_html=True,
    )
    server_inventory = st.radio(questions["Server Energy and Carbon"][0], ["Yes", "No"])
    num_servers = st.number_input(
        questions["Server Energy and Carbon"][1], min_value=0, step=1
    )
    avg_cpus = st.number_input(
        questions["Server Energy and Carbon"][2], min_value=0, step=1
    )
    memory_input = st.number_input(
        questions["Server Energy and Carbon"][3], min_value=0, max_value=55000, step=100
    )
    memory_type = st.selectbox(questions["Server Energy and Carbon"][4], ["SSD", "HDD"])

# Display questions and gather inputs for "PUE Model"
with col2:
    st.write(
        "<h3 style='color: green;font-style: italic;'>PUE Model Input Data</h3>",
        unsafe_allow_html=True,
    )
    location = st.text_input(questions["PUE Model"][0])
    supply_temp = st.number_input(questions["PUE Model"][1], min_value=-50, step=1)
    return_temp = st.number_input(questions["PUE Model"][2], min_value=-50, step=1)
    humidification = st.radio(questions["PUE Model"][3], ["Yes", "No"])
    dehumidification = st.radio(questions["PUE Model"][4], ["Yes", "No"])
    water_economization = st.radio(questions["PUE Model"][5], ["Yes", "No"])
    air_economization = st.radio(questions["PUE Model"][6], ["Yes", "No"])
    cooling_system = st.selectbox(
        questions["PUE Model"][7],
        [
            "Air-Cooled DX",
            "Water-Cooled DX",
            "Evaporatively-Cooled DX",
            "Chilled Water",
        ],
    )
    chiller_type = st.selectbox(
        questions["PUE Model"][8], ["air-cooled", "water-cooled"]
    )
    chilled_water_temp = st.number_input(
        questions["PUE Model"][9], min_value=-50, step=1
    )
    ups_type = st.selectbox(
        questions["PUE Model"][10],
        [
            "Double Conversion",
            "Double Conversion + Filter",
            "Delta Conversion",
            "Rotary",
            "None",
        ],
    )
    avg_load_factor = st.number_input(questions["PUE Model"][11], min_value=0, step=1)

# Add a button to submit the inputs
if st.button("Submit"):
    st.success("Thank you for your submission!")
    # Optionally, display the collected data for confirmation
    st.write("### Submitted Data")
    st.write("**Server Energy and Carbon**")
    st.write(f"Inventory: {server_inventory}")
    st.write(f"Number of Servers: {num_servers}")
    st.write(f"Average CPUs: {avg_cpus}")
    st.write(f"Average Memory (MB): {memory_input}")
    st.write(f"Memory Type: {memory_type}")

    st.write("**PUE Model**")
    st.write(f"Location: {location}")
    st.write(f"Supply Temperature: {supply_temp}°C")
    st.write(f"Return Temperature: {return_temp}°C")
    st.write(f"Humidification Controls: {humidification}")
    st.write(f"Dehumidification Controls: {dehumidification}")
    st.write(f"Water-side Economization: {water_economization}")
    st.write(f"Air-side Economization: {air_economization}")
    st.write(f"Cooling System: {cooling_system}")
    st.write(f"Chiller Type: {chiller_type}")
    st.write(f"Chilled Water Leaving Temperature: {chilled_water_temp}°C")
    st.write(f"UPS Type: {ups_type}")
    st.write(f"Average Load Factor of UPS: {avg_load_factor}")


# Input fields for CPU and memory
# input_cpu = st.text_input("What is the CPU?")
# input_memory = st.text_input("What is the memory?")
# Show the CPU and memory only if input_cpu has a value
# if avg_cpus:
# st.write(f"The input CPU is: {avg_cpus}")
# st.write(f"The input memory is: {memory_input}")


# Add a button to show the file uploader
if st.button("File Upload"):
    # Action to perform when the button is clicked
    st.success("Thank you for your submission!")

    # Display the file uploader
    uploaded_file = st.file_uploader(
        "Choose a file", type=["csv", "txt", "xlsx"], label_visibility="collapsed"
    )

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Display the file name
        st.write(f"**Uploaded file:** {uploaded_file.name}")

        # Read and display the content of the uploaded file
        if uploaded_file.type == "text/csv":
            try:
                df = pd.read_csv(uploaded_file)
                st.write("**DataFrame:**")
                st.write(df)
            except Exception as e:
                st.error(f"Error reading the file: {e}")
                df = pd.read_csv(uploaded_file)
                st.write(df)
        elif uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")
            st.text_area("File content", content, height=300)
        elif (
            uploaded_file.type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            df = pd.read_excel(uploaded_file)
            st.write(df)

    else:
        st.write("Unsuccessful Submission")
else:
    st.write("Click the button above to upload a file.")


# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

st.write(
    "<h3 style='color: green;font-style: italic;'>Estimate Carbon Footprint</h3>",
    unsafe_allow_html=True,
)


# Load the trained XGBoost model from the file
def load_cloud_model():
    with open("xgb_carbon_model.pkl", "rb") as file:
        xgb_model = pickle.load(file)
    return xgb_model


# Load the model once the app is launched
xgb_model = load_cloud_model()

# Collect user input (assuming memory_input and avg_cpus are gathered through input fields)
# memory_input = st.number_input("Enter memory (MB)", min_value=0, max_value=55000, step=100)
# avg_cpus = st.number_input("Enter CPU usage (%)", min_value=0, max_value=100, step=1)

# Predict Carbon Emission
if st.button("Predict Carbon Emission"):
    # Prepare the input data for prediction
    input_data = pd.DataFrame({"memory": [memory_input], "CPU": [avg_cpus]})

    # Predict log-transformed carbon emission
    log_pred_xgb = xgb_model.predict(input_data)

    # Reverse the log transformation to get the actual carbon emission
    carbon_emission_pred_xgb = np.exp(log_pred_xgb)

    # Display the predicted carbon emission
    st.write(
        f"#### Predicted Carbon Emission (by XGBoost): {carbon_emission_pred_xgb[0]:.2f} units"
    )


# Horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

st.write(
    "<h3 style='color: green;font-style: italic;'>Get Your Personalized Recommendations</h3>",
    unsafe_allow_html=True,
)

# Output Recommendation
if st.button("Get Recommendations"):
    # Display the recommendations
    st.write("#### we recommend...")
