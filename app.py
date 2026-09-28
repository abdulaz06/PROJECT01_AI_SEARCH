import os
import json

from flask import Flask, render_template, jsonify, request

from uninformed import bfs, dfs, ucs, ids
from informed import greedy_best_first, a_star


app = Flask(__name__)

MAP_DATA_FILE = "map_data.json"


def load_map_data():

    if os.path.exists(MAP_DATA_FILE):
        try:
            with open(MAP_DATA_FILE, "r") as file:
                return json.load(file)

        except Exception as e:
            print("Error loading map data:", e)

    return {
        "region": "Illinois, USA",
        "total_cities": 0,
        "total_edges": 0,
        "locations": {},
        "graph": {}
    }


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():

    data = load_map_data()

    return jsonify(data)


@app.route("/api/search", methods=["POST"])
def search():

    data = load_map_data()

    payload = request.get_json() or {}

    start = payload.get("start", "")
    goal = payload.get("goal", "")
    algorithm = payload.get("algorithm", "")

    graph = data.get("graph", {})

    if start not in graph or goal not in graph:
        return jsonify({
            "path": [],
            "cost": 0,
            "nodes_expanded": 0,
            "message": "Invalid start or destination city."
        }), 400

    if algorithm == "bfs":
        result = bfs(data, start, goal)

    elif algorithm == "dfs":
        result = dfs(data, start, goal)

    elif algorithm == "ucs":
        result = ucs(data, start, goal)

    elif algorithm == "ids":
        result = ids(data, start, goal)

    elif algorithm == "greedy":
        result = greedy_best_first(data, start, goal)

    elif algorithm == "astar":
        result = a_star(data, start, goal)

    else:
        return jsonify({
            "path": [],
            "cost": 0,
            "nodes_expanded": 0,
            "message": "Invalid search algorithm."
        }), 400

    if result["path"] is None:
        return jsonify({
            "path": [],
            "cost": 0,
            "nodes_expanded": len(result["expanded"]),
            "message": "No path found."
        })

    return jsonify({
        "path": result["path"],
        "cost": result["distance"],
        "nodes_expanded": len(result["expanded"])
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )