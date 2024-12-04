import streamlit as st

import greencompute_frontend.formatting as fmt
from greencompute_frontend.helper import llm_response

# Apply different formatting events
logo = "./greencompute_frontend/images/logo4.png"
fmt.add_logo(logo)
fmt.sidebar()
fmt.background()
fmt.title("GreenCompute Chat")
st.write("Welcome to GreenCompute Chat! Feel free to ask questions on best practices for optimizing your data center's energy consumption.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What can we help with?"):
    # User message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(llm_response(prompt))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
