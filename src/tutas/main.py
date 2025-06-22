from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import os
import re

from louvain.louvain import louvain
from graph_builder import build_similarity_graph
from grouping import make_subgroups
from scoring import compute_score_matrix
from hungarian.matching import match_tutors, format_matches
from config import THRESHOLD

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

INPUT_FILE = os.path.join(DATA_DIR, "input.json")
OUTPUT_1ON1 = os.path.join(DATA_DIR, "output_1on1.json")
OUTPUT_CIRCLE = os.path.join(DATA_DIR, "output_circle.json")

def run_circle_matching(df, max_size=4):
    # Filter entri circle/tutas circle
    df_circle = df[
        df["matchingType"]
          .str
          .lower()
          .isin(["tutas circle", "circle"])
    ]

    # Rename kolom agar graph_builder & make_subgroups bisa jalan
    df_circle = df_circle.rename(columns={
        "fullName":       "Nama",
        "whatsappNumber": "No WA",
        "topicSubtopic":  "Topik",
        "learningMode":   "Mode",
        "learningStyle":  "Gaya",
        "status":         "Status"
    })

    # Map status student→Murid
    df_circle["Status"] = (
        df_circle["Status"]
          .str.strip()
          .str.lower()
          .map({"student": "Murid", "tutor": "Tutor"})
          .fillna(df_circle["Status"])
    )

    # Kalau kosong, langsung return []
    if df_circle.empty:
        return []

    # Reset index supaya .iloc[ ] aman, lalu bangun graph & partisi
    df_circle = df_circle.reset_index(drop=True)
    G = build_similarity_graph(df_circle, THRESHOLD)
    partition = louvain(G)

    # Flat rows dari grouping.py
    rows = make_subgroups(df_circle, partition, max_size=max_size)

    # DEBUG: lihat dulu baris-baris murid/tutor yang dihasilkan
    print("DEBUG rows:", rows)

    # Transform flat rows → struktur StudyGroup
    groups_map = {}
    for r in rows:
        cid = r["Circle ID"]
        person = {
            "name":     r["Nama"],
            "whatsapp": re.sub(r"\D", "", r["No WA"])
        }

        if cid not in groups_map:
            groups_map[cid] = {
                "id":           str(cid),
                "courseName":   None,
                "subtopic":     None,
                "schedule":     None,
                "learningMode": None,
                "maxStudents":  max_size,
                "tutor":        None,
                "students":     []
            }

        # ambil metadata dari baris tutor
        if r["Tutor/Murid"].lower() == "tutor":
            tutor_row = df_circle[df_circle["Nama"] == r["Nama"]].iloc[0]
            groups_map[cid].update({
                "courseName":   tutor_row["courseName"],
                "subtopic":     tutor_row["Topik"],
                "schedule":     f"{tutor_row['preferredDate']} {tutor_row['preferredTime']}",
                "learningMode": tutor_row["Mode"]
            })
            groups_map[cid]["tutor"] = person
        else:
            groups_map[cid]["students"].append(person)

    study_groups = list(groups_map.values())

    # Hanya ambil grup yang tutor-nya tidak null
    study_groups = [g for g in study_groups if g["tutor"] is not None]

    with open(OUTPUT_CIRCLE, "w") as f:
        json.dump({ "study_groups": study_groups }, f, indent=2)
    return study_groups


# Simpan input baru dan jalankan matching otomatis
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
            df_1on1 = df[df["matchingType"].str.lower() == "1-on-1"]
            tutors = df_1on1[df_1on1["status"].str.lower() == "tutor"]
            murids = df_1on1[df_1on1["status"].str.lower() == "student"]

            if tutors.empty or murids.empty:
                return jsonify({"status":"not enough data","matches":[]}), 200

            df_score  = compute_score_matrix(tutors, murids)
            assignment = match_tutors(df_score)
            matches, total = format_matches(df_score, assignment, df_1on1)

            with open(OUTPUT_1ON1, "w") as f:
                json.dump(matches, f, indent=2)

            return jsonify({"status":"1-on-1 matched","matched_pairs":matches}), 200

        except Exception as e:
            app.logger.error("1-on-1 matching failed", exc_info=e)
            return jsonify({"status":"error","error":str(e)}), 500

    elif matching_type in ("tutas circle", "circle"):
        try:
            rows = run_circle_matching(df)
        except Exception:
            import traceback; traceback.print_exc()
            return jsonify({"status":"error","error":"circle matching failed"}), 500

    return jsonify({"status": "received and matched"})

# Endpoint manual 1-on-1
@app.route("/match/1on1", methods=["POST"])
def match_1on1():
    try:
        df = pd.read_json(INPUT_FILE)
        df_1on1 = df[df["matchingType"].str.lower() == "1-on-1"]
        tutors = df_1on1[df_1on1["status"].str.lower() == "tutor"]
        murids = df_1on1[df_1on1["status"].str.lower() == "student"]

        if tutors.empty or murids.empty:
            return jsonify({"status": "not enough data", "matches": []})

        df_score = compute_score_matrix(tutors, murids)
        assignment = match_tutors(df_score)
        matches, total = format_matches(df_score, assignment, df_1on1)

        with open(OUTPUT_1ON1, "w") as f:
            json.dump(matches, f, indent=2)

        return jsonify({"status":"success", "total_score": total, "matched_pairs": matches})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

# Endpoint manual circle
@app.route("/match/circle", methods=["POST"])
def match_circle():
    try:
        df = pd.read_json(INPUT_FILE)
        rows = run_circle_matching(df)
        return jsonify({"status":"success","groups": rows})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

# View data
@app.route("/available", methods=["GET"])
def get_available():
    try:
        raw = json.load(open(OUTPUT_1ON1))
        return jsonify({"matched_pairs": raw})
    except:
        return jsonify({"matched_pairs": []})

@app.route("/tutas-circle", methods=["GET"])
def get_circle():
    try:
        payload = json.load(open(OUTPUT_CIRCLE))
        return jsonify(payload)
    except:
        return jsonify({ "study_groups": [] })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
