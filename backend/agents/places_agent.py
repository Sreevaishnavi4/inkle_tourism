"""
PlacesAgent - Retrieves nearby tourist attractions and points of interest.

Uses the Overpass API to query OpenStreetMap data for attractions, parks, and historic sites.
"""

import httpx

class PlacesAgent:
    """
    Agent for retrieving nearby tourist attractions using Overpass API.

    Queries OpenStreetMap for attractions, leisure areas, and historic sites.
    """

    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    TIMEOUT = 25
    SEARCH_RADIUS = 8000

    @staticmethod
    def get_places(lat: float, lon: float, limit: int = 5) -> list[str]:
        """
        Retrieve nearby tourist attractions for given coordinates.

        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            limit: Maximum number of places to return (default 5)

        Returns:
            A list of place names (strings), max length = limit.
            Returns an empty list if no places found or API fails.
        """
        if lat is None or lon is None:
            return []

        overpass_query = f"""[out:json][timeout:25];
(
  node["tourism"="attraction"](around:{PlacesAgent.SEARCH_RADIUS},{lat},{lon});
  node["leisure"="park"](around:{PlacesAgent.SEARCH_RADIUS},{lat},{lon});
  node["historic"](around:{PlacesAgent.SEARCH_RADIUS},{lat},{lon});
);
out body;"""

        try:
            response = httpx.post(
                PlacesAgent.OVERPASS_URL,
                data=overpass_query,
                timeout=PlacesAgent.TIMEOUT
            )

            response.raise_for_status()
            data = response.json()

            if "elements" not in data:
                return []

            places = []
            seen_names = set()

            for element in data["elements"]:
                if "tags" not in element:
                    continue

                tags = element["tags"]
                name = tags.get("name")

                if name and name not in seen_names:
                    places.append(name)
                    seen_names.add(name)

                    if len(places) >= limit:
                        break

            return places

        except httpx.RequestError:
            return []
        except (KeyError, ValueError, TypeError):
            return []
