import json, os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv('../.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAIが使用する関数の定義
def get_current_weather(location, unit="fahrenheit"):
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps(
            {"location": "San Francisco", "temperature": "72", "unit": unit}
        )
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

# OpenAIが使用可能な関数のリスト
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": { # 関数に渡す引数
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]


client = OpenAI(api_key=OPENAI_API_KEY)

messages = [
    {"role": "user", "content": "Tokyoの天気を教えて"},
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools, # toolsを与える
).to_json()
print(response)

response_message = response.choices[0].message

# 関数名と関数のマッピングを自動で作成
available_functions = {}
for tool in tools:
    function_name = tool["function"]["name"]
    available_functions[function_name] = globals()[function_name]

# 使いたい関数は複数あるかもしれないのでループ
for tool_call in response_message.tool_calls:
    # 関数を実行
    function_name = tool_call["function"]["name"]
    function_args = json.loads(tool_call["function"]["arguments"])
    function_to_call = available_functions[function_name]
    function_response = function_to_call(**function_args)

    print(f"Function {function_name} response: {function_response}")
