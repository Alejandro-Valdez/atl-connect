import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"


def search_realtime_resources(query: str, lat: float = None, lng: float = None) -> list:
    """Fetch real-time Atlanta community resources via Serper.dev."""
    location_hint = ""
    if lat and lng:
        location_hint = f" near coordinates {lat},{lng} Atlanta Georgia"
    else:
        location_hint = " in Atlanta Georgia"

    search_query = f"{query}{location_hint} community resources help"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "q": search_query,
        "gl": "us",
        "hl": "en",
        "location": "Atlanta, Georgia, United States",
        "num": 6,
    }

    try:
        resp = requests.post(SERPER_URL, headers=headers, json=payload, timeout=6)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("organic", [])[:6]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            })

        # Also pull "places" if Serper returns a local pack
        for place in data.get("places", [])[:4]:
            results.append({
                "title": place.get("title", ""),
                "address": place.get("address", ""),
                "phone": place.get("phoneNumber", ""),
                "rating": place.get("rating", ""),
                "link": place.get("website", ""),
                "snippet": place.get("description", ""),
            })

        return results
    except Exception as e:
        print(f"Serper search error: {e}")
        return []
