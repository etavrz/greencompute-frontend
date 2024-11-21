import base64

import streamlit as st


def add_logo(logo: str, width: str = "200px"):
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


def sidebar():
    return st.markdown(
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


def background():
    return st.markdown(
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


def title(title: str):
    # Customizing the title with HTML/CSS to make it larger and green
    st.markdown(
        f"<h1 style='color: #4b7170;font-size: 60px;'>{title}</h1>",
        unsafe_allow_html=True,
    )
