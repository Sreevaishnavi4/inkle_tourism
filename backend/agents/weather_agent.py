"""
WeatherAgent - Retrieves current weather data for a given location.

Uses the Open-Meteo API to fetch real-time weather information.
"""

import httpx

class WeatherAgent:
    """
    Agent for retrieving current weather conditions using Open-Meteo API.

    Open-Meteo provides free, historical, and real-time weather data without authentication.
    """

    OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
    TIMEOUT = 10

    @staticmethod
    def get_weather(lat: float, lon: float) -> dict | None:
        """
        Retrieve current weather conditions for given coordinates.

        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate

        Returns:
            A dictionary with keys:
            - temperature: Current temperature in Celsius (float)
            - precip_prob: Precipitation probability as percentage (float)

            Returns None if the API call fails or data is unavailable.
        """
        if lat is None or lon is None:
            return None

        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,precipitation_probability"
            }

            response = httpx.get(
                WeatherAgent.OPEN_METEO_URL,
                params=params,
                timeout=WeatherAgent.TIMEOUT
            )

            response.raise_for_status()
            data = response.json()

            if "current" not in data:
                return None

            current = data["current"]

            temperature = current.get("temperature_2m")
            precip_prob = current.get("precipitation_probability")

            if temperature is None or precip_prob is None:
                return None

            return {
                "temperature": float(temperature),
                "precip_prob": float(precip_prob)
            }

        except httpx.RequestError:
            return None
        except (KeyError, ValueError, TypeError):
            return None
