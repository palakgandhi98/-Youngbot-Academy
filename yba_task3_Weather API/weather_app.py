import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# Initialize API settings
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/"  # Changed from 3.0 to 2.5

def get_weather(city):
    """Get current weather for a city"""
    try:
        url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

def get_forecast(city):
    """Get 5-day forecast for a city"""
    try:
        url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

# Add custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .forecast-box {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# App title
st.markdown("<h1 style='text-align: center;'>🌤️ Weather Dashboard</h1>", unsafe_allow_html=True)

# City input
city = st.text_input("Enter City Name", "London")

if city:
    # Get current weather
    weather_data = get_weather(city)
    
    if weather_data:
        # Current weather section
        st.markdown("### Current Weather")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<p class='big-font'>{weather_data['name']}, {weather_data['sys']['country']}</p>", unsafe_allow_html=True)
            st.markdown(f"Temperature: **{round(weather_data['main']['temp'], 1)}°C**")
            st.markdown(f"Feels like: **{round(weather_data['main']['feels_like'], 1)}°C**")
        
        with col2:
            st.markdown(f"Humidity: **{weather_data['main']['humidity']}%**")
            st.markdown(f"Wind Speed: **{weather_data['wind']['speed']} m/s**")
            st.markdown(f"Weather: **{weather_data['weather'][0]['description'].capitalize()}**")
        
        # Get and display forecast
        forecast_data = get_forecast(city)
        if forecast_data:
            st.markdown("### 5-Day Forecast")
            cols = st.columns(5)
            
            for idx, item in enumerate(forecast_data['list'][::8]):  # Get one forecast per day
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                temp = round(item['main']['temp'], 1)
                desc = item['weather'][0]['description'].capitalize()
                
                with cols[idx]:
                    st.markdown(f"""
                    <div class='forecast-box'>
                        <p><strong>{date}</strong></p>
                        <p>{temp}°C</p>
                        <p>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("Error fetching weather data. Please check the city name and try again.")

# Add footer
st.markdown("---")
st.markdown("Built with Streamlit and OpenWeatherMap API")