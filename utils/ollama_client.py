import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        
    def list_models(self):
        """List all available models in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                # Extract model names from the response
                models = [model['name'] for model in data.get('models', [])]
                return models
            else:
                return []
        except Exception as e:
            print(f"Error listing Ollama models: {str(e)}")
            return []
    
    def get_completion(self, messages, model):
        """Get completion from Ollama API"""
        try:
            # Convert messages to Ollama format
            prompt = ""
            for message in messages:
                if message["role"] == "user":
                    prompt += f"User: {message['content']}\n"
                elif message["role"] == "assistant":
                    prompt += f"Assistant: {message['content']}\n"
            
            # Add the final prompt for the assistant to respond to
            prompt += "Assistant: "
            
            # Make API request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"
