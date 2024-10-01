import requests
import streamlit as st
import json
import openai

# Setup OpenAI client with API key from Streamlit secrets
openai.api_key = st.secrets["API_KEY"]
    

# Define the "tools" structure that includes the function definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location.",
                    },
                },
                "required": ["location", "format"],
            },
        }
    }
]

# Function to get current weather data
def get_current_weather(location, format):

    if "," in location:
        location = location.split(",")[0].strip()

    # OpenWeather API endpoint
    urlbase = "https://api.openweathermap.org/data/2.5/"
    urlweather = f"weather?q={location}&appid={st.secrets['API_key']}"
    url = urlbase + urlweather

    response = requests.get(url)
    data = response.json()

    # Extract temperature values in Kelvin
    temp_kelvin = data['main']['temp']
    feels_like_kelvin = data['main']['feels_like']
    temp_min_kelvin = data['main']['temp_min']
    temp_max_kelvin = data['main']['temp_max']
    humidity = data['main']['humidity']

    # Convert temperatures based on the unit argument
    if format == 'celsius':
        temp = temp_kelvin - 273.15
        feels_like = feels_like_kelvin - 273.15
        temp_min = temp_min_kelvin - 273.15
        temp_max = temp_max_kelvin - 273.15
    elif format == 'fahrenheit':
        temp = (temp_kelvin - 273.15) * 9/5 + 32
        feels_like = (feels_like_kelvin - 273.15) * 9/5 + 32
        temp_min = (temp_min_kelvin - 273.15) * 9/5 + 32
        temp_max = (temp_max_kelvin - 273.15) * 9/5 + 32
    else:
        raise ValueError("Invalid unit. Please choose either 'celsius' or 'fahrenheit'.")

    # Return the weather information in the desired unit
    return {
        "location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": round(humidity, 2),
        "unit": format
    }

# Function to get clothing suggestions from OpenAI based on temperature
def get_clothing_suggestions(temp, unit):
    prompt = f"The current temperature is {temp} degrees {unit}. Please suggest suitable clothing options for this weather."
    
    response = openai.ChatCompletion.create(
        engine="chatgpt-4o-mini",
        prompt=prompt,
       
    )
    
    suggestions = response.choices[0].text.strip()
    return suggestions

# Streamlit interface to enter the location and display weather results
st.title("Weather Information and Clothing Suggestions")

# Input for location and unit preference
location = st.text_input("Enter a city name:")
format_option = st.selectbox("Choose temperature unit:", ['celsius', 'fahrenheit'])

# Use the tools structure for function invocation logic
if st.button("Get Weather and Clothing Suggestions"):
    if location:
        # Simulating the use of the tools definition and invoking the weather function directly
        function_name = tools[0]['function']['name']
        
        if function_name == 'get_current_weather':
            try:
                weather_data = get_current_weather(location, format_option)
                
                # Display the weather data
                st.write(f"Weather in {weather_data['location']}:")
                st.write(f"Temperature: {weather_data['temperature']} °{format_option.capitalize()}")
                st.write(f"Feels like: {weather_data['feels_like']} °{format_option.capitalize()}")
                st.write(f"Min Temperature: {weather_data['temp_min']} °{format_option.capitalize()}")
                st.write(f"Max Temperature: {weather_data['temp_max']} °{format_option.capitalize()}")
                st.write(f"Humidity: {weather_data['humidity']}%")

                # Get clothing suggestions based on the temperature
                suggestions = get_clothing_suggestions(weather_data['temperature'], format_option.capitalize())
                st.write("Clothing Suggestions:")
                st.write(suggestions)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a valid location.")
