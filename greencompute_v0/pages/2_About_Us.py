import streamlit as st
import pandas as pd
import numpy as np
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
st.markdown("<h1 style='color: green;'>About Us</h1>", unsafe_allow_html=True)


# Define group members
members = [
    {
        "name": "Victor Brew",
        "role": "EDA, Model Development",
        "bio": "bio...",
        "image": "./profile_images/victor.png", 
        "email":"vbrew@berkeley.edu"
    },
    {
        "name": "Nat Buisson",
        "role": "Project Management, UI/UX",
        "bio": "bio...",
        "image": "./profile_images/nat.jpeg",
        "email":"nbuisson@berkeley.edu"
    },
    {
        "name": "Alex Hubbard",
        "role": "SME, Model Development",
        "bio": "bio...",
        "image": "./profile_images/alex.png",
        "email":"alex.hubbard@berkeley.edu"
    },
    {
        "name": "Elias Tavarez",
        "role": "ML Engineering, GenAI",
        "bio": "bio...",
        "image": "./profile_images/elias.png",
        "email":"etav@berkeley.edu"
    },
    {
        "name": "Ruiyu Zhou",
        "role": "EDA, Model Development",
        "bio": "bio...",
        "image": "./profile_images/ruiyu.jpeg",
        "email":"rzhou9@berkeley.edu"
    }
]

# Set up the About Us section
st.write("")

# Iterate over each group member and display their details
for member in members:
    # Create a two-column layout: image on the left, bio/role on the right
    col1, col2 = st.columns([1, 2])  # Adjust column width as needed
    
    with col1:
        st.image(member["image"], width=150)  # Display member's image
    
    with col2:
        st.subheader(member["name"])
        st.write(f"**Role:** {member['role']}")
        st.write(f"**Bio:** {member['bio']}")
        st.write(f"**Email Address:** {member['email']}")
    
    st.write("---")  # Add a horizontal divider between members