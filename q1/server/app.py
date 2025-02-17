from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import redis
import json
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Adjust log level as needed (INFO, DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Print logs to console
        logging.FileHandler("app.log")  # Also log to a file
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be replaced with ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, ...)
    allow_headers=["*"],  # Allow all headers
)

# API key from WeatherAPI.com
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL_WEATHER = "http://api.weatherapi.com/v1/current.json"
BASE_URL_SUGGEST = "http://api.weatherapi.com/v1/search.json"

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
CACHE_EXPIRATION = 600  # 10 minutes

class WeatherResponse(BaseModel):
    city: str
    country: str  # Added country field
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    date: str  # Added date field

class CitySuggestion(BaseModel):
    name: str
    country: str

@app.get("/weather/{location}", response_model=WeatherResponse)
def get_weather(location: str):
    """Return weather information by city name or coordinates 'lat,lon'."""
    cache_key = f"weather:{location}"

    # Check cache first
    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return WeatherResponse(**json.loads(cached_data))
    except Exception as e:
        logger.error(f"Error accessing cache: {e}")  # Log the error but don't break the API

    # Fetch data from API
    try:
        response = requests.get(BASE_URL_WEATHER, params={"key": API_KEY, "q": location})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch weather data from API.")

    data = response.json()

    if "error" in data or "location" not in data or "current" not in data:
        logger.error(f"Invalid data received from API: {data}")
        raise HTTPException(status_code=500, detail="Invalid data received from API.")

    # Create weather data
    weather_data = WeatherResponse(
        city=data["location"]["name"],
        country=data["location"]["country"],
        temperature=data["current"]["temp_c"],
        description=data["current"]["condition"]["text"],
        humidity=data["current"]["humidity"],
        wind_speed=data["current"]["wind_kph"] / 3.6,  # Convert km/h to m/s
        date=data["location"]["localtime"].split(" ")[0]
    )

    # Save to cache but don't break the API if Redis is not available
    try:
        redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(weather_data.dict()))
    except Exception as e:
        logger.error(f"Error saving data to cache: {e}")

    return weather_data


@app.get("/suggestions/{query}", response_model=list[CitySuggestion])
def get_city_suggestions(query: str):
    """Suggest city names based on the input query."""
    try:
        response = requests.get(BASE_URL_SUGGEST, params={"key": API_KEY, "q": query})
        response.raise_for_status()
        data = response.json()

        if not data:
            logger.warning(f"No city suggestions found for query: {query}")
            raise HTTPException(status_code=404, detail="No suggestions found.")

        return [CitySuggestion(name=city["name"], country=city["country"]) for city in data]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching city suggestions: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch city suggestions.")


@app.get("/forecast/{location}", response_model=list[WeatherResponse])
def get_weather_forecast(location: str, days: int = 3):
    """Return weather forecast for 1, 3, or 7 days."""
    if days not in {1, 3, 7}:  
        raise HTTPException(status_code=400, detail="Forecast days must be 1, 3, or 7.")

    cache_key = f"forecast:{location}:{days}"

    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return [WeatherResponse(**item) for item in json.loads(cached_data)]
    except Exception as e:
        logger.error(f"Error accessing cache: {e}")  # Log the error but don't break the API

    try:
        response = requests.get(
            "http://api.weatherapi.com/v1/forecast.json",
            params={"key": API_KEY, "q": location, "days": days}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching forecast data: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch forecast data from API.")

    data = response.json()

    if "error" in data or "forecast" not in data or "forecastday" not in data["forecast"]:
        logger.error(f"Invalid forecast data received from API: {data}")
        raise HTTPException(status_code=500, detail="Invalid forecast data received from API.")

    forecast_data = [
        WeatherResponse(
            date=day["date"],
            city=data["location"]["name"],
            country=data["location"]["country"],
            temperature=day["day"]["avgtemp_c"],
            description=day["day"]["condition"]["text"],
            humidity=day["day"]["avghumidity"],
            wind_speed=day["day"]["maxwind_kph"] / 3.6  # Convert km/h to m/s
        )
        for day in data["forecast"]["forecastday"]
    ]

    try:
        redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps([item.dict() for item in forecast_data]))
    except Exception as e:
        logger.error(f"Error saving forecast data to cache: {e}")  # Log the error but don't break the API

    return forecast_data
