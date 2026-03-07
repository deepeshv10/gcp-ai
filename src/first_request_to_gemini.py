from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash-lite", 
    contents="Tell a joke",
    config=types.GenerateContentConfig(
        system_instruction="Answer in 10-30 words only",
        temperature=0.8)
)


print(response.text)