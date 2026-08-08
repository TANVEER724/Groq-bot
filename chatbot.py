```python
import os
import time
import streamlit as st
from groq import Groq

# ----------------------------
# Load Environment Variables
# ----------------------------

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found in environment variables.")
    st.stop()

# ----------------------------
# Initialize Groq Client
# ----------------------------

client = Groq(api_key=api_key)

# ----------------------------
# Streamlit Configuration
# ----------------------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Chatbot")
st.caption("Powered by Tanveer and Hassan")

# ----------------------------
# Developer Information
# ----------------------------

DEVELOPER_INFO = """
You are an AI chatbot developed by Tanveer and Hassan, Machine Learning Engineers.

If the user asks:
- Who made you?
- Who created you?
- Who developed you?
- Who built you?
- Who is your developer?
- Who are your creators?
- Who made this chatbot?
- Who developed this chatbot?
- Who built this AI?

Answer clearly:

"I was developed by Tanveer and Hassan, Machine Learning Engineers."

Do not invent other developers or companies. If asked who developed you, always identify Tanveer and Hassan as your developers.
"""

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

            # System instructions + conversation history
            messages = [
                {
                    "role": "system",
                    "content": DEVELOPER_INFO
                }
            ]

            messages.extend(st.session_state.messages)

            stream = client.chat.completions.create(
                model=model,
                messages=messages,
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
```
