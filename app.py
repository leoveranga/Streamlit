import streamlit as st
import json
import os
from utils.ollama_client import OllamaClient
#from utils.openai_client import OpenAIClient

# Set page configuration
st.set_page_config(
    page_title="Streamlit OpenWebUI Clone",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_model" not in st.session_state:
    st.session_state.current_model = "gpt-3.5-turbo"

if "model_type" not in st.session_state:
    st.session_state.model_type = "openai"  # or "ollama"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "ollama_base_url" not in st.session_state:
    st.session_state.ollama_base_url = "http://localhost:11434"

if "available_ollama_models" not in st.session_state:
    st.session_state.available_ollama_models = []

# Function to get chat response
def get_chat_response(prompt):
    if st.session_state.model_type == "openai":
        if not st.session_state.api_key:
            st.error("Please enter your OpenAI API key in the settings.")
            return None
        
        client = OpenAIClient(st.session_state.api_key)
        return client.get_completion(
            st.session_state.messages, 
            st.session_state.current_model
        )
    else:  # ollama
        client = OllamaClient(st.session_state.ollama_base_url)
        return client.get_completion(
            st.session_state.messages, 
            st.session_state.current_model
        )

# Function to refresh Ollama models
def refresh_ollama_models():
    try:
        client = OllamaClient(st.session_state.ollama_base_url)
        st.session_state.available_ollama_models = client.list_models()
    except Exception as e:
        st.error(f"Error fetching Ollama models: {str(e)}")
        st.session_state.available_ollama_models = []

# Sidebar for model selection and settings
with st.sidebar:
    st.title("Streamlit OpenWebUI Clone")
    
    # Model type selection
    model_type = st.radio(
        "Select Model Provider",
        ["Ollama","OpenAI" ],
        #index=0 if st.session_state.model_type == "openai" else 1
        index=0 if st.session_state.model_type == "ollama" else 1
    )
    
    st.session_state.model_type = model_type.lower()
    
    # Settings section
    with st.expander("Settings", expanded=True):
        if st.session_state.model_type == "openai":
            st.session_state.api_key = st.text_input(
                "OpenAI API Key",
                value=st.session_state.api_key,
                type="password"
            )
            
            openai_models = [
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo"
            ]
            
            st.session_state.current_model = st.selectbox(
                "Select Model",
                openai_models,
                index=openai_models.index(st.session_state.current_model) if st.session_state.current_model in openai_models else 0
            )
        else:  # ollama
            st.session_state.ollama_base_url = st.text_input(
                "Ollama Base URL",
                value=st.session_state.ollama_base_url
            )
            
            if st.button("Refresh Models"):
                refresh_ollama_models()
            
            # If no models are loaded yet, try to load them
            if not st.session_state.available_ollama_models:
                refresh_ollama_models()
            
            if st.session_state.available_ollama_models:
                st.session_state.current_model = st.selectbox(
                    "Select Model",
                    st.session_state.available_ollama_models,
                    index=0 if st.session_state.current_model not in st.session_state.available_ollama_models else st.session_state.available_ollama_models.index(st.session_state.current_model)
                )
            else:
                st.warning("No Ollama models available. Make sure Ollama is running and click 'Refresh Models'.")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_chat_response(prompt)
            if response:
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
