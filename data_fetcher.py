import json
import time
import math
import requests


REGION_NAME = "Illinois, USA"

CITIES = [
    "Chicago, IL",
    "Aurora, IL",
    "Naperville, IL",
    "Joliet, IL",
    "Rockford, IL",
    "Springfield, IL",
    "Peoria, IL",
    "Elgin, IL",
    "Waukegan, IL",
    "Champaign, IL",
    "Bloomington, IL",
    "Decatur, IL",
    "Evanston, IL",
    "Schaumburg, IL",
    "Arlington Heights, IL",
    "Bolingbrook, IL",
    "Palatine, IL",
    "Skokie, IL",
    "Des Plaines, IL",
    "Orland Park, IL",
    "Kankakee, IL",
    "DeKalb, IL"
]


ROAD_CONNECTIONS = [
    ("Chicago, IL", "Evanston, IL"),
    ("Chicago, IL", "Skokie, IL"),
    ("Chicago, IL", "Des Plaines, IL"),
    ("Chicago, IL", "Naperville, IL"),
    ("Chicago, IL", "Joliet, IL"),
    ("Chicago, IL", "Orland Park, IL"),

    ("Evanston, IL", "Skokie, IL"),
    ("Evanston, IL", "Waukegan, IL"),
    ("Skokie, IL", "Des Plaines, IL"),

    ("Des Plaines, IL", "Arlington Heights, IL"),
    ("Arlington Heights, IL", "Palatine, IL"),
    ("Arlington Heights, IL", "Waukegan, IL"),
    ("Palatine, IL", "Schaumburg, IL"),

    ("Schaumburg, IL", "Elgin, IL"),
    ("Schaumburg, IL", "Naperville, IL"),

    ("Elgin, IL", "DeKalb, IL"),
    ("Elgin, IL", "Rockford, IL"),
    ("DeKalb, IL", "Rockford, IL"),
    ("DeKalb, IL", "Aurora, IL"),

    ("Naperville, IL", "Aurora, IL"),
    ("Naperville, IL", "Bolingbrook, IL"),
    ("Aurora, IL", "Joliet, IL"),

    ("Bolingbrook, IL", "Joliet, IL"),
    ("Joliet, IL", "Orland Park, IL"),
    ("Joliet, IL", "Kankakee, IL"),
    ("Joliet, IL", "Bloomington, IL"),

    ("Kankakee, IL", "Champaign, IL"),

    ("Rockford, IL", "Peoria, IL"),
    ("Peoria, IL", "Bloomington, IL"),
    ("Peoria, IL", "Springfield, IL"),

    ("Bloomington, IL", "Champaign, IL"),
    ("Bloomington, IL", "Decatur, IL"),
    ("Bloomington, IL", "Springfield, IL"),

    ("Springfield, IL", "Decatur, IL"),
    ("Decatur, IL", "Champaign, IL")
]


USER_AGENT = "CS411-Search-Visualizer/1.0"


def haversine_distance(coord1, coord2):

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    radius = 3958.8

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = lat2 - lat1
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(radius * c, 2)


def fetch_coordinates(city):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            if len(data) > 0:
                return {
                    "lat": float(data[0]["lat"]),
                    "lon": float(data[0]["lon"])
                }

    except Exception as e:
        print("Error getting coordinates for", city, ":", e)

    return None


def fetch_road_distance(coord1, coord2):

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}"
    )

    params = {
        "overview": "false"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            if data.get("code") == "Ok" and len(data.get("routes", [])) > 0:
                distance_meters = data["routes"][0]["distance"]

                distance_miles = distance_meters * 0.000621371

                return round(distance_miles, 2)

    except Exception as e:
        print("Error getting road distance:", e)

    # Fall back to straight-line distance if OSRM fails
    return haversine_distance(coord1, coord2)


def build_graph():
    print("Building graph for", REGION_NAME)

    locations = {}

    # Get coordinates for every city
    for i, city in enumerate(CITIES, 1):
        print(f"[{i}/{len(CITIES)}] Getting coordinates for {city}")

        coords = fetch_coordinates(city)

        if coords is not None:
            locations[city] = coords
        else:
            print("Could not find:", city)

        # Avoid sending requests too quickly
        time.sleep(1)


    # Create empty adjacency list
    graph = {}

    for city in locations:
        graph[city] = {}


    print("\nGetting road distances...")

    total_edges = 0

    for city1, city2 in ROAD_CONNECTIONS:

        if city1 not in locations or city2 not in locations:
            print("Skipping:", city1, city2)
            continue

        coord1 = (
            locations[city1]["lat"],
            locations[city1]["lon"]
        )

        coord2 = (
            locations[city2]["lat"],
            locations[city2]["lon"]
        )

        distance = fetch_road_distance(coord1, coord2)

        # Undirected graph
        graph[city1][city2] = distance
        graph[city2][city1] = distance

        total_edges += 1

        print(
            city1,
            "<->",
            city2,
            ":",
            distance,
            "miles"
        )

        time.sleep(0.2)


    map_data = {
        "region": REGION_NAME,
        "total_cities": len(locations),
        "total_edges": total_edges,
        "locations": locations,
        "graph": graph
    }


    with open("map_data.json", "w") as file:
        json.dump(map_data, file, indent=2)


    print("\nDone!")
    print("Cities:", len(locations))
    print("Edges:", total_edges)
    print("Saved graph to map_data.json")


if __name__ == "__main__":
    build_graph()