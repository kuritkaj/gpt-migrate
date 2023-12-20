import os
import openai
from utils import parse_code_string
from litellm import completion

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")

class AI:
    def __init__(self, model="gpt-4-32k", model_provider="openai", modelrouter="openrouter", temperature=0.1, max_tokens=10000):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model_provider = model_provider
        self.model_name = model
        self.modelrouter = modelrouter
    
    def write_code(self, prompt):
        message=[{"role": "user", "content": str(prompt)}]
        if self.modelrouter == "openrouter":
            response = openai.ChatCompletion.create(
                model=f"{self.model_provider}/{self.model_name}",
                messages=message,
                stream=False,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                headers={
                    "HTTP-Referer": "https://gpt-migrate.com",
                    "X-Title": "GPT-Migrate",
                },
            )
        else:
            response = completion(
                messages=message,
                stream=False,
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
        if response["choices"][0]["message"]["content"].startswith("INSTRUCTIONS:"):
            return ("INSTRUCTIONS:","",response["choices"][0]["message"]["content"][14:])
        else:
            return parse_code_string(response["choices"][0]["message"]["content"])

    def run(self, prompt):
        message=[{"role": "user", "content": str(prompt)}]
        if self.modelrouter == "openrouter":
            response = openai.ChatCompletion.create(
                model=f"{self.model_provider}/{self.model_name}",
                messages=message,
                stream=False,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                headers={
                    "HTTP-Referer": "https://gpt-migrate.com",
                    "X-Title": "GPT-Migrate",
                },
            )
            return response["choices"][0]["message"]["content"]
        else:
            response = completion(
                messages=message,
                stream=True,
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            chat = ""
            for chunk in response:
                delta = chunk["choices"][0]["delta"]
                msg = delta.get("content", "")
                chat += msg
            return chat
        
    