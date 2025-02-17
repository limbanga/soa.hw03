"use client";
import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, MapPin, Search, LocateFixed } from "lucide-react";

interface WeatherData {
  city: string;
  country: string;
  temperature: number;
  description: string;
  humidity: number;
  wind_speed: number;
  date: string;
}

interface CitySuggestion {
  name: string;
  country: string;
}

const CACHE_EXPIRATION = 10 * 60 * 1000; // 10 minutes
const API_BASE_URL = "http://localhost:8000"; // FastAPI URL
const DEBOUNCE_DELAY = 500; // Debounce delay (ms)

export default function WeatherApp() {
  const [city, setCity] = useState<string>("");
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [suggestions, setSuggestions] = useState<CitySuggestion[]>([]);
  const [debounceQuery, setDebounceQuery] = useState<string>("");
  const [forecast, setForecast] = useState<WeatherData[]>([]);

  const getCache = (key: string) => {
    const cachedData = localStorage.getItem(key);
    if (!cachedData) return null;
    const { data, timestamp } = JSON.parse(cachedData);
    if (Date.now() - timestamp > CACHE_EXPIRATION) {
      localStorage.removeItem(key);
      return null;
    }
    return data;
  };

  const setCache = (key: string, data: any) => {
    localStorage.setItem(key, JSON.stringify({ data, timestamp: Date.now() }));
  };

  const fetchWeather = async (location: string) => {
    if (!location) return;
    setLoading(true);
    setError("");

    const cachedWeather = getCache(`weather_${location}`);
    if (cachedWeather) {
      setWeather(cachedWeather);
      setLoading(false);
      return;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/weather/${location}`);
      if (!res.ok) throw new Error("Error fetching weather data.");
      const data: WeatherData = await res.json();
      setWeather(data);
      setCache(`weather_${location}`, data);
      setSuggestions([]);
    } catch (err) {
      setError("Unable to fetch weather information.");
      setWeather(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchForecast = async (location: string) => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE_URL}/forecast/${location}?days=7`);
      if (!res.ok) throw new Error("Error fetching forecast data.");
      const data: WeatherData[] = await res.json();
      setForecast(data);
    } catch (err) {
      setError("Unable to fetch forecast data.");
      setForecast([]);
    } finally {
      setLoading(false);
    }
  };

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      setError("Geolocation not supported by the browser.");
      return;
    }
    setLoading(true);
    setError("");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        fetchWeather(`${latitude},${longitude}`);
      },
      () => {
        setError("Unable to fetch location. Please check GPS permissions.");
        setLoading(false);
      }
    );
  };

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebounceQuery(city);
    }, DEBOUNCE_DELAY);

    return () => clearTimeout(handler);
  }, [city]);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (!debounceQuery) {
        setSuggestions([]);
        return;
      }

      try {
        const res = await fetch(`${API_BASE_URL}/suggestions/${debounceQuery}`);
        const data: CitySuggestion[] = await res.json();
        setSuggestions(data);
      } catch (err) {
        console.error("Unable to fetch suggestions", err);
      }
    };

    fetchSuggestions();
  }, [debounceQuery]);

  // Helper function to format date to English
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" });
  };

  return (
    <div className="flex flex-col items-center p-6 space-y-4 min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold">Weather Forecast</h1>
      <div className="relative w-full max-w-md">
        <Input
          placeholder="Enter city name..."
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        {suggestions.length > 0 && (
          <ul className="absolute bg-white border w-full mt-1 shadow-md rounded-lg">
            {suggestions.map((sugg, index) => (
              <li
                key={index}
                className="p-2 hover:bg-gray-200 cursor-pointer"
                onClick={() => {
                  setSuggestions([]);
                  fetchWeather(sugg.name);
                  fetchForecast(sugg.name); // Automatically fetch 7-day forecast when a city is selected
                }}
              >
                {sugg.name}, {sugg.country}
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="flex space-x-2">
        <Button onClick={() => { fetchWeather(city); fetchForecast(city); }} disabled={!city || loading}>
          {loading ? <Loader2 className="animate-spin" /> : <Search />}
          <span className="ml-2">Search</span>
        </Button>
        <Button variant="secondary" onClick={getCurrentLocation} disabled={loading}>
          {loading ? <Loader2 className="animate-spin" /> : <LocateFixed />}
          <span className="ml-2">Get Location</span>
        </Button>
      </div>

      {error && <p className="text-red-500">{error}</p>}

      {weather && (
        <Card className="w-full max-w-md">
          <CardContent className="p-6 text-center">
            <h2 className="text-xl font-semibold flex items-center justify-center">
              <MapPin className="mr-2" /> {weather.city}, {weather.country}
            </h2>
            <p className="text-lg">{weather.description}</p>
            <p className="text-4xl font-bold">{weather.temperature}°C</p>
            <p>Humidity: {weather.humidity}%</p>
            <p>Wind: {weather.wind_speed.toFixed(2)} m/s</p>
          </CardContent>
        </Card>
      )}

      {forecast.length > 0 && (
        <div className="mt-6 flex flex-wrap justify-center gap-4">
          <h2 className="text-xl font-semibold w-full text-center">7-Day Weather Forecast</h2>
          {forecast.map((day, index) => (
            <Card key={index} className="w-64">
              <CardContent className="p-4 text-center">
                <h3 className="text-lg font-semibold">{formatDate(day.date)}</h3>
                <p className="text-md">{day.description}</p>
                <p className="text-3xl font-bold">{day.temperature}°C</p>
                <p>Humidity: {day.humidity}%</p>
                <p>Wind: {day.wind_speed.toFixed(2)} m/s</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
