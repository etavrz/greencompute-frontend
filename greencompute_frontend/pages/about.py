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
        "bio": "Victor is responsible for the exploratory data analysis and predictive modeling components of GreenCompute. He was a Solutions Engineer in the Data & AI segment at IBM. He led the pre-sales efforts, collaborating with clients to understand their software needs around data science and engineering and transforming those into tailored solutions. Currently, he is making a pivot into IT analytics. His passions within data science are around data analytics, engineering and modeling. Outside of his professional career, Victor enjoys athletic pursuits such as rugby and spending time with his family.",
        "image": "./greencompute_frontend/images/victor.png",
        "email": "vbrew@berkeley.edu",
    },
    {
        "name": "Nat Buisson",
        "role": "Project Management, UI/UX",
        "bio": "Nat is responsible for the Project Management of GreenCompute. She is a Master of Information and Data Science (MIDS) student at UC Berkeley with a background as a chemical engineer and over a decade of experience in the chemical manufacturing industry. Her career has focused on optimizing complex industrial processes, leading cross-functional teams, and delivering data-driven solutions to improve operational efficiency and sustainability.",
        "image": "./greencompute_frontend/images/nat.jpeg",
        "email": "nbuisson@berkeley.edu",
    },
    {
        "name": "Alex Hubbard",
        "role": "SME, Model Development",
        "bio": "Alex is the subject matter expert for GreenCompute, is responsible for data discovery, and helped to create the predictive models used in the tool. He is currently a technology researcher at Lawrence Berkeley National Laboratory, where he performs energy analysis of industrial processes and data centers. Alex is passionate about data-driven approaches to energy savings, specifically in data centers and industrial processes. Outside of data science, Alex is a long-time rock climber and runner, and enjoys doing anything in the outdoors.",
        "image": "./greencompute_frontend/images/alex.png",
        "email": "alex.hubbard@berkeley.edu",
    },
    {
        "name": "Elias Tavarez",
        "role": "ML Engineering, GenAI, Architecture",
        "bio": "Elias is responsible for the infrastructure, deployment, and GenAI components of GreenCompute. He is currently working as a data scientist for BASF, where he has worked on a variety of different projects across the ML spectrum, all within the context of manufacturing. His interests within data science are those around machine learning engineering; more specifically, the creation of infrastructure to deliver ML models to production. Outside of data science, Elias loves to read, play all sorts of sports, and do just about anything with friends and family.",
        "image": "./greencompute_frontend/images/elias.png",
        "email": "etav@berkeley.edu",
    },
    {
        "name": "Ruiyu Zhou",
        "role": "EDA, Model Development, Front-End Design",
        "bio": "Ruiyu is responsible for the exploratory data analysis, predictive modeling, and front-end design and development of GreenCompute. She is currently part of the Index Product Development team at Nasdaq, where she focuses on generating, validating, and pitching innovative index concepts. Her passions in data science span machine learning, time series forecasting, and crafting insightful visualizations. Beyond her professional interests, Ruiyu enjoys long-distance cycling, immersing herself in music, exploring new books, and spending time with her lively 3-year-old cat.",
        "image": "./greencompute_frontend/images/ruiyu.jpeg",
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
