from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.exceptions import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# API key từ WeatherAPI.com
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# Mô hình dữ liệu cho phản hồi thời tiết
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float

@app.get("/weather/{city}", response_model=WeatherResponse)
def get_weather(city: str):
    """Trả về thông tin thời tiết từ WeatherAPI.com."""
    response = requests.get(BASE_URL, params={"key": API_KEY, "q": city})

    data = response.json()
    
    if "error" in data:
        raise HTTPException(status_code=response.status_code, detail=data["error"]["message"])
    
    weather_data = WeatherResponse(
        city=data["location"]["name"],
        temperature=data["current"]["temp_c"],
        description=data["current"]["condition"]["text"],
        humidity=data["current"]["humidity"],
        wind_speed=data["current"]["wind_kph"] / 3.6  # Chuyển từ km/h sang m/s
    )
    return weather_data

# Chạy ứng dụng nếu file được thực thi trực tiếp
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)