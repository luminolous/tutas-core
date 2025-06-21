from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import os

from louvain.louvain import louvain
from graph_builder import build_similarity_graph
from grouping import make_subgroups
from scoring import compute_score_matrix
from hungarian.matching import match_tutors, format_matches

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

INPUT_FILE = os.path.join(DATA_DIR, "input.json")
OUTPUT_1ON1 = os.path.join(DATA_DIR, "output_1on1.json")
OUTPUT_CIRCLE = os.path.join(DATA_DIR, "output_circle.json")

# 🔽 Simpan input baru dan jalankan matching otomatis
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    try:
        with open(INPUT_FILE, "r") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        all_data = []

    all_data.append(data)

    with open(INPUT_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

    # Jalankan matching otomatis
    df = pd.DataFrame(all_data)
    matching_type = data.get("matchingType", "").lower()

    if matching_type == "1-on-1":
        try:
            df_1on1 = df[df["matchingType"] == "1-on-1"]
            tutors = df_1on1[df_1on1["status"].str.lower() == "tutor"]
            murids = df_1on1[df_1on1["status"].str.lower() == "student"]

            if not tutors.empty and not murids.empty:
                df_score = compute_score_matrix(tutors, murids)
                assignment = match_tutors(df_score)
                matches, total = format_matches(df_score, assignment)

                with open(OUTPUT_1ON1, "w") as f:
                    json.dump(matches, f, indent=2)
        except Exception as e:
            print(f"❌ Matching 1-on-1 failed: {e}")

    elif matching_type == "circle":
        try:
            df_circle = df[df["matchingType"] == "Circle"]
            if not df_circle.empty:
                G = build_similarity_graph(df_circle, threshold=0.5)
                partition = louvain(G)
                rows = make_subgroups(df_circle, partition, max_size=4)
                df_result = pd.DataFrame(rows)

                with open(OUTPUT_CIRCLE, "w") as f:
                    json.dump(df_result.to_dict(orient="records"), f, indent=2)
        except Exception as e:
            print(f"❌ Matching Circle failed: {e}")

    return jsonify({"status": "received and matched"})

# 🔁 Endpoint manual 1-on-1
@app.route("/match/1on1", methods=["POST"])
def match_1on1():
    try:
        df = pd.read_json(INPUT_FILE)
        df_1on1 = df[df["matchingType"] == "1-on-1"]
        tutors = df_1on1[df_1on1["status"].str.lower() == "tutor"]
        murids = df_1on1[df_1on1["status"].str.lower() == "student"]

        if tutors.empty or murids.empty:
            return jsonify({"status": "not enough data", "matches": []})

        df_score = compute_score_matrix(tutors, murids)
        assignment = match_tutors(df_score)
        matches, total = format_matches(df_score, assignment)

        with open(OUTPUT_1ON1, "w") as f:
            json.dump(matches, f, indent=2)

        return jsonify({"status": "success", "total_score": total, "matches": matches})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

# 🔁 Endpoint manual circle
@app.route("/match/circle", methods=["POST"])
def match_circle():
    try:
        df = pd.read_json(INPUT_FILE)
        df_circle = df[df["matchingType"] == "Circle"]

        if df_circle.empty:
            return jsonify({"status": "no circle entries"})

        G = build_similarity_graph(df_circle, threshold=0.5)
        partition = louvain(G)
        rows = make_subgroups(df_circle, partition, max_size=4)
        df_result = pd.DataFrame(rows)

        result = df_result.to_dict(orient="records")
        with open(OUTPUT_CIRCLE, "w") as f:
            json.dump(result, f, indent=2)

        return jsonify({"status": "success", "groups": result})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

# 🔍 View data
@app.route("/available", methods=["GET"])
def get_available():
    try:
        with open(OUTPUT_1ON1) as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])

@app.route("/tutas-circle", methods=["GET"])
def get_circle():
    try:
        with open(OUTPUT_CIRCLE) as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
