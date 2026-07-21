import os
import time
import streamlit as st
from groq import Groq

# ----------------------------
# Load Environment Variables
# ----------------------------

api_key = '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'

if not api_key:
    st.error("❌ GROQ_API_KEY not found in .env file.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# ----------------------------
# Streamlit Configuration
# ----------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖AI Chatbot")
st.caption("Powered by Tanveer and Hassan")

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:

    st.header("⚙️ Settings")

    model = st.selectbox(
        "Choose Model",
        (
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
            "meta-llama/llama-4-scout-17b-16e-instruct"
        )
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        2.0,
        0.7,
        0.1
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------
# Chat History
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------
# User Input
# ----------------------------
prompt = st.chat_input("Type your message...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        try:

            stream = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True,
            )

            for chunk in stream:

                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0].delta.content
                ):
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"❌ Error: {str(e)}"
            placeholder.error(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
    
