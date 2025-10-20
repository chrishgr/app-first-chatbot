# Step 1: install google SDK
# Step 2: Import google SDK
# Step 3: Write a message on the screen
# Step 4: Added Navbar
# 


import streamlit as st
import google.generativeai as genai

#st.logo("./app/test_logo.png")


st.sidebar.title("Settings")

with st.sidebar:
    model = st.selectbox(
        "Select you model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"],
        key="gemini_model"
    )
    gemini_api_key = st.text_input("Gemini API key", key="gemini_api_key", type="password")

st.title("eih bot")
st.caption("something more text")

# api_key = "AIzaSyA-W6f3UlDPT-3-u5P5s5j8oEa7OuHqs6Y"
# model_name  = "gemini-2.5-flash"

# genai.configure(api_key=api_key)
# model=genai.GenerativeModel(model_name)

#st.session_state.clear()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not gemini_api_key:
        st.info("Please add your Google API key")
        st.stop()

    genai.configure(api_key=gemini_api_key)
    model=genai.GenerativeModel(model)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)