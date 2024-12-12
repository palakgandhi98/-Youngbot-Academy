# 🌤️ Weather Dashboard

A simple weather dashboard built using [Streamlit](https://streamlit.io/) and the [OpenWeatherMap API](https://openweathermap.org/). This app allows users to enter a city name and get the current weather as well as a 5-day weather forecast.

![Weather_app](https://github.com/user-attachments/assets/776751cf-fb72-4fb2-baba-93de51943a80)

--- 

- [🎓 Student Database Management System](#-banking-system)
  - [Features](#features)
  - [Requirements](#Requirements)
  - [Directory Structure](#Directory)
  - [Setup](#Setup)
  - [How it Works](#How)
  - [Acknowledgements](#Acknowledgements)
  - [Code Logic](#Code)
  - [Full Code Logic Summary](#Full)
  - [Contributing](#Contributing)
  - [Stay Connected](#Stay)
  - [License](#License)
  - 

---
## Features

- Displays the **current weather** of the entered city, including temperature, humidity, wind speed, and a weather description.
- Shows a **5-day weather forecast**, including the temperature and weather description for each day.
- Responsive layout with clear and concise information about the weather.
---

## Requirements

- `Python` 3.6+
- `Streamlit`
- `Requests`
- `python-dotenv`
---


## Directory Structure:
    
```bash
project/
│
├── .env             # Contains database credentials
├── database.py      # Database-related logic
├── main.py          # Streamlit app for visualization

```

---
## Setup

1. Clone the repository:
    
    ```bash
    git clone https://github.com/your-username/weather-dashboard.git
    cd weather-dashboard
    ```

2. Install the required dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your OpenWeatherMap API key:
    
    ```bash
    OPENWEATHER_API_KEY=your_api_key_here
    ```

4. Running the Application

    ```bash
    streamlit run weather_app.py
    ```
---

## How it Works

The app uses the OpenWeatherMap API to fetch the current weather and a 5-day forecast for the city entered by the user. The weather data is displayed in an easy-to-read format with:

- Current temperature, humidity, wind speed, and weather description.
- 5-day forecast showing the temperature and weather description for each day.
---

## Acknowledgements

- `Streamlit` for the simple and fast way to build web apps.
- `OpenWeatherMap` API for providing weather data.
- `python-dotenv` for loading environment variables.
---

## Code Logic

1. **Imports and Dependencies**

```python
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
```

2. **Loading Environment Variables**

```python
# Load environment variables
load_dotenv()

# Initialize API settings
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/"  # Changed from 3.0 to 2.5
```

- `load_dotenv()`: This loads the environment variables from the .env file.
- `API_KEY`: Accesses the OpenWeatherMap API key from the environment variable.
- `BASE_URL`: The base URL for the OpenWeatherMap API. The version 2.5 is used here (rather than 3.0).

3. **API Call Functions**

    `get_weather()`: Fetches current weather data

```python
def get_weather(city):
    """Get current weather for a city"""
    try:
        url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Returns the JSON response
    except requests.exceptions.RequestException as e:
        return None  # If an error occurs, return None
```

- `get_weather()`: This function builds the API URL with the city name, the API key, and the unit (metric for Celsius). It makes a GET request using `requests.get()`.
- If the request is successful, the function returns the JSON data of the current weather.
- If an error occurs (e.g., an invalid city name or API failure), it catches the exception and returns `None`.

`get_forecast()`: Fetches 5-day weather forecast data

```python
def get_forecast(city):
    """Get 5-day forecast for a city"""
    try:
        url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # Returns the JSON response
    except requests.exceptions.RequestException as e:
        return None  # If an error occurs, return None
```

- `get_forecast()`: Similar to `get_weather()`, this function fetches the 5-day weather forecast data for a city.
- It constructs the URL for the forecast API endpoint and returns the forecast data in JSON format if successful.

4. **Streamlit Page Setup and Custom CSS**

```python
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
```

- Custom CSS: Adds styling to the app. The .big-font class makes the city name and country larger and bold, while .forecast-box is used for styling the forecast data boxes (adding padding, border radius, and margin).

5. **Streamlit User Interface**

    App Title and City Input

```python
# App title
st.markdown("<h1 style='text-align: center;'>🌤️ Weather Dashboard</h1>", unsafe_allow_html=True)

# City input
city = st.text_input("Enter City Name", "London")
```

- App title: The title is centered and displayed using Streamlit's st.markdown().
- City input: The user is prompted to enter the city name using a text_input() field. By default, the city is set to "London".

Fetching and Displaying Current Weather

```python
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

```

- **City validation**: If a city is provided by the user, the app calls get_weather(city) to fetch the current weather data.
- **The app then displays**:
    - **City Name**: weather_data['name'] and country code weather_data['sys']['country'].
    - **Temperature**: weather_data['main']['temp'] (rounded to one decimal).
    - **Feels Like Temperatur**e: weather_data['main']['feels_like'] (rounded to one decimal).
    - **Humidity**: weather_data['main']['humidity'].
    - **Wind Speed**: weather_data['wind']['speed'].
    - **Weather Description**: weather_data['weather'][0]['description'].

Fetching and Displaying ``5-Day Forecast``

```python
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
```

- **Forecast data**: The function get_forecast(city) is called to fetch the 5-day forecast data.
- The forecast_data['list'][::8] slices the forecast data, taking one entry per day (since the API returns data every 3 hours, this ensures one entry per day).

- The forecast for each day is displayed with:
    - `Date`: The timestamp is converted to a human-readable date using datetime.fromtimestamp().
    - `Temperature`: The temperature for the day is shown (rounded to one decimal).
    - `Weather Description`: The weather description (e.g., "clear sky", "light rain") is displayed and capitalized.

6.  **Error Handling**

```python
else:
    st.error("Error fetching weather data. Please check the city name and try again.")
```

- If an error occurs while fetching weather data (e.g., invalid city), an error message is shown using `st.error()`.
  
7. **Footer**

```python
st.markdown("---")
st.markdown("Built with Streamlit and OpenWeatherMap API")
```
---

## Full Code Logic Summary:
- **App Setup**: The app is configured with Streamlit's settings and custom CSS for styling.
- **User Input**: The user enters a city name (default is "London").
- **API Requests**: The app fetches the current weather and 5-day forecast for the entered city using OpenWeatherMap's API.
- **Display**: The current weather and forecast are displayed in a clean layout with appropriate formatting.
- **Error Handling**: If there are issues with the API call (e.g., invalid city), an error message is shown.
- **Footer**: The footer shows credits for the technologies used.

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests.

## Stay Connected:
 * [![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff)](https://www.github.com/palakgandhi98)
 * [![LinkedIn](https://img.shields.io/badge/Linkedin-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/palakgandhi98)

Let's build something amazing together!


## License
This project is licensed under the MIT License.
