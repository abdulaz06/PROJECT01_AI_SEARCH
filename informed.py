import math
import heapq


def haversine(coord1, coord2):

    radius = 3958.8

    lat1 = math.radians(coord1["lat"])
    lon1 = math.radians(coord1["lon"])

    lat2 = math.radians(coord2["lat"])
    lon2 = math.radians(coord2["lon"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return radius * c


def greedy_best_first(map_data, start, goal):

    graph = map_data.get("graph", {})
    locations = map_data.get("locations", {})

    if start not in graph or goal not in graph:
        return {
            "path": None,
            "expanded": [],
            "distance": 0.0
        }

    if start not in locations or goal not in locations:
        return {
            "path": None,
            "expanded": [],
            "distance": 0.0
        }

    goal_coord = locations[goal]

    pq = []

    counter = 0

    h_start = haversine(
        locations[start],
        goal_coord
    )

    heapq.heappush(
        pq,
        (
            h_start,
            counter,
            start,
            [start],
            0.0
        )
    )

    visited = set()
    expanded = []

    while pq:
        _, _, node, path, cost = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)
        expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(cost, 2)
            }

        neighbors = sorted(graph.get(node, {}).items())

        for n_name, n_dist in neighbors:
            if n_name not in visited:
                counter += 1

                h_val = haversine(
                    locations[n_name],
                    goal_coord
                )

                heapq.heappush(
                    pq,
                    (
                        h_val,
                        counter,
                        n_name,
                        path + [n_name],
                        cost + n_dist
                    )
                )

    return {
        "path": None,
        "expanded": expanded,
        "distance": 0.0
    }


def a_star(map_data, start, goal):

    graph = map_data.get("graph", {})
    locations = map_data.get("locations", {})

    if start not in graph or goal not in graph:
        return {
            "path": None,
            "expanded": [],
            "distance": 0.0
        }

    if start not in locations or goal not in locations:
        return {
            "path": None,
            "expanded": [],
            "distance": 0.0
        }

    goal_coord = locations[goal]

    pq = []

    counter = 0

    h_start = haversine(
        locations[start],
        goal_coord
    )

    heapq.heappush(
        pq,
        (
            h_start,
            counter,
            start,
            [start],
            0.0
        )
    )

    visited = set()
    expanded = []

    while pq:
        _, _, node, path, g_cost = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)
        expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(g_cost, 2)
            }

        neighbors = sorted(graph.get(node, {}).items())

        for n_name, n_dist in neighbors:
            if n_name not in visited:
                counter += 1

                g_new = g_cost + n_dist

                h_val = haversine(
                    locations[n_name],
                    goal_coord
                )

                f_new = g_new + h_val

                heapq.heappush(
                    pq,
                    (
                        f_new,
                        counter,
                        n_name,
                        path + [n_name],
                        g_new
                    )
                )

    return {
        "path": None,
        "expanded": expanded,
        "distance": 0.0
    }