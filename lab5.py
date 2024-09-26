import requests
import streamlit as st
import openai
def get_current_weather(location, API_key):
    
    if "," in location:
        location = location.split(",")[0].strip()
    urlbase = "https://api.openweathermap.org/data/2.5/"
    urlweather = f"weather?q={location}&appid={API_key}"
    url = urlbase + urlweather

    response = requests.get(url)
    data = response.json()
    # Extract temperatures & Convert Kelvin to Celsius
    temp = data['main']['temp'] - 273.15
    feels_like = data['main']['feels_like'] - 273.15
    temp_min = data['main']['temp_min'] - 273.15
    temp_max = data['main']['temp_max'] - 273.15
    humidity = data['main']['humidity']

    return {"location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": round(humidity, 2)
    }
if __name__ == "__main__":
    st.title("Weather App")
    API_key = st.secrets["openweathermap"]["API_key"]  
    openai.api_key = st.secrets["API_KEY"]
    # Input from the user for the location
    location = st.text_input("Enter the location:", "Syracuse, NY")
    
    if location:
        weather_info = get_current_weather(location,API_key)

    
    conversation_history = [{"role": "system", "content": """
        You are a helpful assistant. After getting weather info you need to give clothing suggestions according to it.
    """}]

    # Include the relevant documents fetched from ChromaDB
    conversation_history.append({
        "role": "system",
        "content": f"Current weather info:\n{weather_info }"
    })

    
    
    # Step 3: Send the complete prompt to GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )
    assistant_response = response['choices'][0]['message']['content']

    st.write(weather_info)
    st.write(assistant_response)
