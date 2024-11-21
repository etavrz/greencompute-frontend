import streamlit as st

import greencompute_frontend.formatting as fmt

# Apply different formatting events
logo = "./greencompute_frontend/images/logo4.png"
fmt.add_logo(logo)
fmt.sidebar()
fmt.background()
fmt.title("About Us")

# Define group members
members = [
    {
        "name": "Victor Brew",
        "role": "EDA, Model Development",
        "bio": "bio...",
        "image": "./greencompute_frontend/images/victor.png",
        "email": "vbrew@berkeley.edu",
    },
    {
        "name": "Nat Buisson",
        "role": "Project Management, UI/UX",
        "bio": "bio...",
        "image": "./greencompute_frontend/images/nat.jpeg",
        "email": "nbuisson@berkeley.edu",
    },
    {
        "name": "Alex Hubbard",
        "role": "SME, Model Development",
        "bio": "bio...",
        "image": "./greencompute_frontend/images/alex.png",
        "email": "alex.hubbard@berkeley.edu",
    },
    {
        "name": "Elias Tavarez",
        "role": "ML Engineering, GenAI",
        "bio": "bio...",
        "image": "./greencompute_frontend/images/elias.png",
        "email": "etav@berkeley.edu",
    },
    {
        "name": "Ruiyu Zhou",
        "role": "EDA, Model Development",
        "bio": "bio...",
        "image": "./greencompute_frontend/images/ruiyu.jpeg",
        "email": "rzhou9@berkeley.edu",
    },
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
