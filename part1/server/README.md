# Server Project

## Overview

This project is part of the SOA labs homework (hw03). It contains the server-side implementation for question 1.

## Prerequisites

- Python 3.x
- Redis
- weatherapi.com

## Installation

1. Navigate to the project directory:
  ```sh
  cd hw03/q1/server
  ```
1. Install the dependencies:
  ```sh
  pip install -r requirements.txt
  ```

## Usage
1. Start Redis
  ```sh
  sudo systemctl start redis.service
  ```

2. Start the server:
  ```sh
  uvicorn app:app --reload
  ```
1. The server will be running at `http://localhost:8000`.

## Techniques applied in the project

1. **FastAPI**: A fast web framework that supports async and auto-generates API documentation (Swagger).
2. **Pydantic**: Data validation and transformation with `BaseModel` to define API models.
3. **Redis**: Used as a cache to store weather API results, reducing server load with a 10-minute expiration time.
4. **dotenv**: Manages environment variables, securing API keys in a `.env` file.
5. **CORS Middleware**: Allows API access from different domains.
6. **API Requests**: Sends requests to WeatherAPI to fetch weather data.
7. **Error Handling**: Handles errors when unable to connect to APIs or Redis, ensuring the API doesn't crash.
8. **Logging**: Logs errors encountered during API or Redis connection issues.
9. **RESTful API**: Designs the API in a RESTful architecture, using HTTP GET methods.
