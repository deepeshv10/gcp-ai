from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

chat = client.chats.create(model="gemini-2.5-flash-lite")

while True:
    message = input("> ")
    if message == "exit":
        break


    response = chat.send_message(message)
    print(response.text)