import os
import requests
import gradio as gr
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY1")

# Define function to get current weather
def get_current_weather(location, unit='celsius'):
    weather_api_key = os.getenv("WEATHER_API_KEY")
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
    try:
        response = requests.get(base_url, timeout=10)  # Increased timeout for the request
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        weather_description = data['weather'][0]['description']
        return {
            "location": location,
            "temperature": data['main']['temp'],
            "weather": weather_description
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again later."}
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}

# Function definition and initial message handling
def weather_chat(user_message):
    messages = []
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": "You are a weather bot. Answer only in Celsius. If two cities are asked, provide weather for both."})

    # Sending initial message to OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=messages,
            functions=[
                {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The city, e.g. San Francisco"},
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                        },
                        "required": ["location"]
                    }
                }
            ]
        )
    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return "Failed to communicate with the OpenAI API. Please try again later."

    # Handling function calls and fetching weather data
    try:
        function_call = response['choices'][0]['message']['function_call']
        arguments = eval(function_call['arguments'])
        weather_data = get_current_weather(arguments['location'])
        if 'error' in weather_data:
            return weather_data['error']
        messages.append({"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": str(arguments)}})
        messages.append({"role": "function", "name": "get_current_weather", "content": str(weather_data)})

        # Continue conversation with weather data
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error during processing: {e}")
        return "I'm here to provide weather updates. Please ask me questions related to weather."

# Define Gradio interface
iface = gr.Interface(
    fn=weather_chat,
    inputs=gr.Textbox(label="Weather Queries"),
    outputs=gr.Textbox(label="Weather Updates"),
    title="DDS Weather Bot",
    description="Ask me anything about weather!"
)

# Launch the Gradio interface
iface.launch()
