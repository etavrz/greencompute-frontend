import streamlit as st
import base64

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
        color: #4b7170;
        font-size: 18px;  /* Set default font size */
        /* font-weight: bold;   Make the text bold */
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

# Customizing the title with HTML/CSS to make it larger and green
st.markdown("<h1 style='color: #4b7170;font-size: 60px;'>About Us</h1>", unsafe_allow_html=True)


# Define group members
members = [
    {
        "name": "Victor Brew",
        "role": "EDA, Model Development",
        "bio": "Victor is responsible for the exploratory data analysis and predictive modeling components of GreenCompute. He was a Solutions Engineer in the Data & AI segment at IBM. He led the pre-sales efforts, collaborating with clients to understand their software needs around data science and engineering and transforming those into tailored solutions. Currently, he is making a pivot into IT analytics. His passions within data science are around data analytics, engineering and modeling. Outside of his professional career, Victor enjoys athletic pursuits such as rugby and spending time with his family.",
        "image": "./images/victor.png",
        "email": "vbrew@berkeley.edu",
    },
    {
        "name": "Nat Buisson",
        "role": "Project Management, UI/UX",
        "bio": "bio...",
        "image": "./images/nat.jpeg",
        "email": "nbuisson@berkeley.edu",
    },
    {
        "name": "Alex Hubbard",
        "role": "SME, Model Development",
        "bio": "bio...",
        "image": "./images/alex.png",
        "email": "alex.hubbard@berkeley.edu",
    },
    {
        "name": "Elias Tavarez",
        "role": "ML Engineering, GenAI",
        "bio": "Elias is responsible for the infrastructure, deployment, and GenAI components of GreenCompute. He is currently working as a data scientist for BASF, where he has worked on a variety of different projects across the ML spectrum, all within the context of manufacturing. His interests within data science are those around machine learning engineering; more specifically, the creation of infrastructure to deliver ML models to production. Outside of data science, Elias loves to read, play all sorts of sports, and do just about anything with friends and family.",
        "image": "./images/elias.png",
        "email": "etav@berkeley.edu",
    },
    {
        "name": "Ruiyu Zhou",
        "role": "EDA, Model Development, Front-End Design",
        "bio": "Ruiyu is responsible for the exploratory data analysis, predictive modeling, and front-end design and development of GreenCompute. She is currently part of the Index Product Development team at Nasdaq, where she focuses on generating, validating, and pitching innovative index concepts. Her passions in data science span machine learning, time series forecasting, and crafting insightful visualizations. Beyond her professional interests, Ruiyu enjoys long-distance cycling, immersing herself in music, exploring new books, and spending time with her lively 3-year-old cat.",
        "image": "./images/ruiyu.jpeg",
        "email": "rzhou9@berkeley.edu",
    },
]

# Set up the About Us section
st.write("")

# Iterate over each group member and display their details
for member in members:
    # Create a two-column layout: image on the left, bio/role on the right
    col1, col2 = st.columns([1, 5])  # Adjust column width as needed

    with col1:
        
        st.image(member["image"], width=150)  # Display member's image

    with col2:
        st.subheader(member["name"])
        st.write(f"**Role:** {member['role']}")
        st.write(f"**Bio:** {member['bio']}")
        st.write(f"**Email Address:** {member['email']}")

    st.write("---")  # Add a horizontal divider between members
