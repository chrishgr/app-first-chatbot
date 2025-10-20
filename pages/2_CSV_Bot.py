import streamlit as st
import google.generativeai as genai
import pandas as pd

st.sidebar.title("Settings")

with st.sidebar:
    model_name = st.selectbox(
        "Select you model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"],
        key="gemini_model"
    )
    gemini_api_key = st.text_input("Gemini API key", key="gemini_api_key", type="password")

st.title("Chat with your csv data")
st.caption("something more text")

uploaded_file = st.file_uploader("Upload your CSV here", type=("csv"))

if not gemini_api_key:
    st.info("Please add your Google API key to continue")
    st.stop()

genai.configure(api_key=gemini_api_key)
model= genai.GenerativeModel(model_name)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.df = ""


if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    csv_preview = st.session_state.df.head(50).to_string(index= False)

    if not any(msg["role"]=="assistant" for msg in st.session_state.messages):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "CSV uploaded! You can now ask me questions about it"
        })

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask me something about the CSV file"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    chat_prompt = f""" 
                    You are a data analyst. Use the following CSV data to answer my Question:
                    CSV data: {csv_preview},
                    Question: {prompt}
                   """
    
    chat = model.start_chat(history=[])
    response = chat.send_message(chat_prompt)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)

    