"""
TourismOrchestrator - Parent agent that coordinates all tourism-related queries.

This orchestrator will manage the workflow between:
- GeocodingAgent (place name → coordinates)
- WeatherAgent (current weather data)
- PlacesAgent (tourist attractions)

Future implementation will include:
- Query parsing and intent detection
- Sequential agent coordination
- Response aggregation and formatting
- Error handling for non-existent places
"""

from ..agents.geocoding_agent import GeocodingAgent
from ..agents.weather_agent import WeatherAgent
from ..agents.places_agent import PlacesAgent

class TourismOrchestrator:
    """
    Main orchestrator for handling tourism queries across multiple specialized agents.

    This class coordinates between geocoding, weather, and places agents to provide
    comprehensive tourism information for user-specified locations.
    """

    @classmethod
    def extract_place(cls, user_query: str) -> str | None:
        """
        Extract a place name from a natural language query.
        Handles cases like:
        - "I'm going to Bangalore, let's plan my trip"
        - "I want to go to Paris"
        - "Going to Goa what is the temperature"
        """

        if not user_query:
            return None

        text = user_query.lower()

        # Ensure "to" is present
        if "to " not in text:
            return None

        # Take everything after the LAST "to "
        place_part = text.split("to ")[-1]

        # Remove everything after first comma ?, !, "and", "what"
        for sep in [",", "?", "!", " and ", " what", " then"]:
            if sep in place_part:
                place_part = place_part.split(sep)[0]
                break

        # Remove extra spaces and punctuation
        place = place_part.strip(" .,!?:;-")

        # Capitalize properly (nominatim is case-insensitive but cleaner)
        if place:
            return place.strip()

        return None

    @classmethod
    def parse_intent(cls, user_query: str) -> tuple[bool, bool]:
        """
        Returns (wants_weather, wants_places) based on simple keyword rules.

        - Weather intent: words like "weather", "temperature", "hot", "cold"
        - Strong places intent: "place", "places", "visit", "see", "trip", "plan my trip"
        - Soft place word: "go" (only counts if no explicit weather-only case)
        """
        query_lower = user_query.lower()

        weather_keywords = ["weather", "temperature", "hot", "cold"]
        strong_places_keywords = ["place", "places", "visit", "see", "trip", "plan my trip"]
        soft_places_keywords = ["go"]

        wants_weather = any(k in query_lower for k in weather_keywords)

        # Strong signal for places (like "places", "visit") 
        wants_places_strong = any(k in query_lower for k in strong_places_keywords)
        wants_places_soft = any(k in query_lower for k in soft_places_keywords)

        # Start with places intent = strong OR soft
        wants_places = wants_places_strong or wants_places_soft

        # ✅ If user clearly asks about weather, but does NOT explicitly mention places,
        #    then treat it as weather-only (ignore "go").
        if wants_weather and not wants_places_strong:
            wants_places = False

        # ✅ If no explicit weather or places intent, default to places (trip planning).
        if not wants_weather and not wants_places:
            wants_places = True

        return wants_weather, wants_places

    @classmethod
    def _get_short_place_name(cls, full_name: str) -> str:
        """
        Extract short place name from full display name.

        Takes the part before the first comma (e.g., "Bengaluru" from "Bengaluru, Bangalore North, ...").

        Args:
            full_name: Full display name from Nominatim

        Returns:
            Short place name
        """
        return full_name.split(",")[0].strip()

    @classmethod
    def handle_query(cls, user_query: str) -> str:
        """
        Process a user's tourism query and coordinate responses from child agents.

        Detects intent (weather, places, or both), geocodes the location, and retrieves
        relevant information from WeatherAgent and PlacesAgent.

        Args:
            user_query: The natural language query from the user

        Returns:
            A formatted string response with tourism information

        Flow:
            1. Extract place name from user_query
            2. Use GeocodingAgent to validate location and get coordinates
            3. Parse intent to determine if user wants weather, places, or both
            4. Call WeatherAgent and/or PlacesAgent based on intent
            5. Format and return combined response
        """
        place = cls.extract_place(user_query)

        if not place:
            return "I couldn't understand which place you want to visit."

        coordinates = GeocodingAgent.get_coordinates(place)

        if coordinates is None:
            return "I don't know this place exists."

        lat = coordinates["lat"]
        lon = coordinates["lon"]
        full_place_name = coordinates["name"]
        short_place_name = cls._get_short_place_name(full_place_name)

        wants_weather, wants_places = cls.parse_intent(user_query)

        responses = []

        if wants_weather:
            weather = WeatherAgent.get_weather(lat, lon)
            if weather is not None:
                temperature = weather["temperature"]
                precip_prob = weather["precip_prob"]
                weather_response = (
                    f"In {short_place_name} it's currently {temperature}°C "
                    f"with a {precip_prob}% chance of rain."
                )
                responses.append(weather_response)
            else:
                weather_response = (
                    f"Weather information for {short_place_name} is temporarily unavailable."
                )
                responses.append(weather_response)

        if wants_places:
            places = PlacesAgent.get_places(lat, lon)
            if places:
                places_list = "\n".join([f"{i + 1}. {place}" for i, place in enumerate(places)])
                places_response = (
                    f"In {short_place_name} these are the places you can go:\n{places_list}"
                )
                responses.append(places_response)
            else:
                places_response = (
                    f"I couldn't find tourist attractions near {short_place_name}."
                )
                responses.append(places_response)

        return " And ".join(responses)


