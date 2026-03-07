from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3-flash-preview", 
    contents="Explain how AI works in a few words",
    config=types.GenerateContentConfig(
        system_instruction="Answer in 10-30 words only")
)
print(response.text)