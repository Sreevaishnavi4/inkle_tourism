"""
GeocodingAgent - Converts place names to geographic coordinates.

Uses the Nominatim OpenStreetMap API to geocode location queries.
"""

import httpx

class GeocodingAgent:
    """
    Agent for converting place names to geographic coordinates using Nominatim API.

    Nominatim is an open-source geocoder built on OpenStreetMap data.
    """

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    USER_AGENT = "inkle-assignment/1.0 (tourism@inkle.ai)"
    TIMEOUT = 10

    @staticmethod
    def get_coordinates(place: str) -> dict | None:
        """
        Retrieve geographic coordinates for a given place name.

        Args:
            place: The name of the place to geocode

        Returns:
            A dictionary with keys:
            - lat: Latitude (float)
            - lon: Longitude (float)
            - name: Display name from Nominatim

            Returns None if the place cannot be found or an error occurs.
        """
        if not place or not place.strip():
            return None

        try:
            params = {
                "q": place.strip(),
                "format": "json",
                "limit": 1
            }

            headers = {
                "User-Agent": GeocodingAgent.USER_AGENT
            }

            response = httpx.get(
                GeocodingAgent.NOMINATIM_URL,
                params=params,
                headers=headers,
                timeout=GeocodingAgent.TIMEOUT
            )

            response.raise_for_status()
            results = response.json()

            if results and len(results) > 0:
                first_result = results[0]
                return {
                    "lat": float(first_result["lat"]),
                    "lon": float(first_result["lon"]),
                    "name": first_result.get("display_name", place)
                }

            return None

        except httpx.RequestError:
            return None
        except (KeyError, ValueError):
            return None
