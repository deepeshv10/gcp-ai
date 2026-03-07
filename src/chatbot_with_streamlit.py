# 
# This is a basic Chatbot using streamlit. uses gemini model
# To run the program : streamlit run chatbot_with_streamlit.py
#

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# 1. Setup & Config
load_dotenv()
st.set_page_config(page_title="Chatbot using Gemini", layout="centered")
st.title("Personal Assistant")

# Initialize the Gemini Client
api_key = os.getenv("GEMINI_API_KEY") # Ensure this is in your .env
client = genai.Client(api_key=api_key)

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if prompt := st.chat_input("Type your message..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 5. Generate LLM Response
    with st.chat_message("assistant"):
        try:
            # You can replace this with your specific LLM logic
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=prompt
            )
            full_response = response.text
            st.markdown(full_response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")