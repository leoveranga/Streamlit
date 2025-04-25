import openai

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def get_completion(self, messages, model):
        """Get completion from OpenAI API"""
        try:
            # Format messages for OpenAI API
            formatted_messages = []
            for message in messages:
                formatted_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
            
            # Make API request to OpenAI
            response = self.client.chat.completions.create(
                model=model,
                messages=formatted_messages
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
