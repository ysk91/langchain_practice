import os

from dotenv import load_dotenv
from langsmith import Client

load_dotenv("../.env")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

client = Client(
    api_key=LANGCHAIN_API_KEY,
)
prompt = client.pull_prompt("ysk91/translate")

prompt_value = prompt.invoke(
    {
        "lang": "ja",
        "text": "Hello, how are you?",
    }
)
print(prompt_value)
