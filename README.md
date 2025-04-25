# OpenWebUI Clone - Streamlit App

This is a Streamlit application that mimics OpenWebUI, providing a chat interface for both local LLMs via Ollama and OpenAI's ChatGPT models.

## Features

- Support for local LLMs through Ollama
- Support for OpenAI's ChatGPT models
- Clean, responsive chat interface
- Model selection and configuration
- Persistent chat history during session

## Requirements

- Python 3.10+
- Streamlit
- OpenAI Python package
- Requests package
- Ollama running locally (for local LLM support)

## Installation

1. Ensure you have Python 3.10+ installed
2. Install required packages:
   ```
   pip install streamlit openai requests
   ```
3. For local LLM support, install Ollama from [https://ollama.ai/](https://ollama.ai/)

## Usage

1. Start the application:
   ```
   ./start_app.sh
   ```
   or
   ```
   cd streamlit_openwebui
   streamlit run app.py
   ```

2. Access the application in your web browser at:
   - Local URL: http://localhost:8501
   - When deployed: http://8501-inxzw9erkmw60vxrd393d-cdcaa545.manus.computer

## Configuration

### OpenAI (ChatGPT)
- Select "OpenAI" as the model provider
- Enter your OpenAI API key in the settings panel
- Choose from available models (gpt-3.5-turbo, gpt-4, gpt-4-turbo)

### Ollama (Local LLMs)
- Select "Ollama" as the model provider
- Ensure Ollama is running locally (default URL: http://localhost:11434)
- Click "Refresh Models" to see available models
- Select your preferred model from the dropdown

## Project Structure

- `app.py`: Main Streamlit application
- `utils/ollama_client.py`: Client for Ollama API integration
- `utils/openai_client.py`: Client for OpenAI API integration
- `start_app.sh`: Convenience script to start the application

## Notes

- For Ollama to work, you must have it installed and running on your machine
- For ChatGPT to work, you must provide a valid OpenAI API key
- The chat history is stored in the session state and will be cleared when you restart the application or click "Clear Chat"
