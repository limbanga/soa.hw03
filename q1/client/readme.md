# Client Project

## Overview
This project is part of the SOA labs homework assignment (hw03). It is located in the `client` directory and is designed to demonstrate the implementation of a client application.

## Prerequisites
- Node.js
- npm (Node Package Manager)

## Installation
2. Navigate to the project directory:
  ```sh
  cd hw03/q1/client
  ```
3. Install the dependencies:
  ```sh
  npm install
  ```

## Usage
To start the client application, run:
```sh
npm run dev
```

## Features
- Search for Weather: Enter the city name in the search bar to get weather details.
- City Suggestions: While typing the city name, suggestions will appear below the search bar.
- Current Location: Click the "Get Location" button to fetch weather data based on your current geolocation.
- 7-Day Forecast: After searching for a city, the app shows a 7-day weather forecast with temperature, humidity, and wind speed.

## Optimization techniques
Debouncing: Delays API calls while typing to prevent excessive requests and improve performance.

Caching: Stores weather data in localStorage with an expiration timestamp to avoid redundant API calls.

Lazy Loading: Fetches weather data only when the user requests it, reducing unnecessary load.

Error Handling: Displays clear error messages to inform the user when something goes wrong (e.g., failed API call).
