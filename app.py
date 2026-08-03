import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(question):
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response


st.set_page_config(page_title="Bot App")

st.header("🤖 App Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Input:", key="input")

if st.button("Generate Response") and user_input:

    response = get_gemini_response(user_input)

    st.session_state.chat_history.append(("You", user_input))

    st.subheader("Response")

    answer = ""

    for chunk in response:
        if chunk.text:
            answer += chunk.text
            st.write(chunk.text)

    st.session_state.chat_history.append(("Bot", answer))

st.subheader("Chat History")

for role, text in st.session_state.chat_history:
    st.write(f"**{role}:** {text}")