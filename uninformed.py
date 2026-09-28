from collections import deque
import heapq


def bfs(map_data, start, goal):

    graph = map_data.get("graph", {})

    if start not in graph or goal not in graph:
        return {"path": None, "expanded": [], "distance": 0.0}

    if start == goal:
        return {"path": [start], "expanded": [start], "distance": 0.0}

    queue = deque([(start, [start], 0.0)])
    visited = {start}
    expanded = []

    while queue:
        node, path, dist = queue.popleft()
        expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(dist, 2)
            }

        neighbors = sorted(graph.get(node, {}).items())

        for n_name, n_dist in neighbors:
            if n_name not in visited:
                visited.add(n_name)
                queue.append(
                    (n_name, path + [n_name], dist + n_dist)
                )

    return {
        "path": None,
        "expanded": expanded,
        "distance": 0.0
    }


def dfs(map_data, start, goal):

    graph = map_data.get("graph", {})

    if start not in graph or goal not in graph:
        return {"path": None, "expanded": [], "distance": 0.0}

    if start == goal:
        return {"path": [start], "expanded": [start], "distance": 0.0}

    stack = [(start, [start], 0.0)]
    visited = set()
    expanded = []

    while stack:
        node, path, dist = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(dist, 2)
            }

        neighbors = sorted(
            graph.get(node, {}).items(),
            reverse=True
        )

        for n_name, n_dist in neighbors:
            if n_name not in visited:
                stack.append(
                    (n_name, path + [n_name], dist + n_dist)
                )

    return {
        "path": None,
        "expanded": expanded,
        "distance": 0.0
    }


def ucs(map_data, start, goal):

    graph = map_data.get("graph", {})

    if start not in graph or goal not in graph:
        return {"path": None, "expanded": [], "distance": 0.0}

    pq = []

    counter = 0
    heapq.heappush(
        pq,
        (0.0, counter, start, [start])
    )

    visited = set()
    expanded = []

    while pq:
        cost, _, node, path = heapq.heappop(pq)

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

                heapq.heappush(
                    pq,
                    (
                        cost + n_dist,
                        counter,
                        n_name,
                        path + [n_name]
                    )
                )

    return {
        "path": None,
        "expanded": expanded,
        "distance": 0.0
    }


def ids(map_data, start, goal):

    graph = map_data.get("graph", {})

    if start not in graph or goal not in graph:
        return {"path": None, "expanded": [], "distance": 0.0}

    expanded = []

    def dls(node, path, dist, limit, visited_path):
        expanded.append(node)

        if node == goal:
            return {
                "path": path,
                "distance": dist
            }

        if limit <= 0:
            return None

        neighbors = sorted(graph.get(node, {}).items())

        for n_name, n_dist in neighbors:
            if n_name not in visited_path:
                result = dls(
                    n_name,
                    path + [n_name],
                    dist + n_dist,
                    limit - 1,
                    visited_path | {n_name}
                )

                if result is not None:
                    return result

        return None

    for limit in range(len(graph) + 1):
        result = dls(
            start,
            [start],
            0.0,
            limit,
            {start}
        )

        if result is not None:
            result["expanded"] = expanded
            result["distance"] = round(
                result["distance"],
                2
            )
            return result

    return {
        "path": None,
        "expanded": expanded,
        "distance": 0.0
    }