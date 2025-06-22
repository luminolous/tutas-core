# src/tutas/hungarian/matching.py

import numpy as np
import pandas as pd

def build_cost_matrix(score_df: pd.DataFrame) -> list[list[float]]:
    """
    Dari DataFrame skor (tutor × murid), bangun matriks biaya (cost matrix)
    untuk minimisasi Hungarian:
      cost[i][j] = max_score – score[i,j]
    """
    scores = score_df.values
    max_score = scores.max()
    return (max_score - scores).tolist()

def hungarian(cost: list[list[float]]) -> list[int]:
    """
    Implementasi manual Hungarian (Kuhn–Munkres).
    Input:  cost = n×n list of lists
    Output: assignment list, di mana assignment[i]=j artinya baris i → kolom j
    """
    n = len(cost)
    u = [0]*(n+1)
    v = [0]*(n+1)
    p = [0]*(n+1)
    way = [0]*(n+1)

    for i in range(1, n+1):
        p[0] = i
        j0 = 0
        minv = [float('inf')]*(n+1)
        used = [False]*(n+1)

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = 0
            for j in range(1, n+1):
                if not used[j]:
                    cur = cost[i0-1][j-1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(n+1):
                if used[j]:
                    u[p[j]] += delta
                    v[j]      -= delta
                else:
                    minv[j]   -= delta
            j0 = j1
            if p[j0] == 0:
                break

        while True:
            j1      = way[j0]
            p[j0]   = p[j1]
            j0      = j1
            if j0 == 0:
                break

    assignment = [-1]*n
    for j in range(1, n+1):
        if p[j] != 0:
            assignment[p[j]-1] = j-1
    return assignment

def format_matches(score_df, assignment, df_1on1):
    tutors = score_df.index.tolist()
    murids = score_df.columns.tolist()
    scores = score_df.values

    matches = []
    total = 0
    for i, j in enumerate(assignment):
        if j < 0 or j >= len(murids): continue
        t_name = tutors[i]
        s_name = murids[j]
        s = scores[i][j]
        if t_name.startswith("DUMMY") or s_name.startswith("DUMMY"): continue

        # Ambil baris DataFrame original berdasarkan fullName
        t_row = df_1on1[(df_1on1["fullName"] == t_name) & (df_1on1["status"].str.lower()=="tutor")].iloc[0]
        s_row = df_1on1[(df_1on1["fullName"] == s_name) & (df_1on1["status"].str.lower()=="student")].iloc[0]

        matches.append({
            "tutorName"       : t_name,
            "studentName"     : s_name,
            "score"           : int(s),
            "tutorWhatsapp"   : t_row["whatsappNumber"],
            "studentWhatsapp" : s_row["whatsappNumber"],
            "subject"         : t_row["courseName"],
            "subtopic"        : t_row["topicSubtopic"],
            "schedule"        : f'{t_row["preferredDate"]} {t_row["preferredTime"]}',
            "learningMode"    : t_row["learningMode"],
        })
        total += s

    return matches, total

def match_tutors(score_df: pd.DataFrame, verbose: bool = False) -> list[int]:
    cost = build_cost_matrix(score_df)
    assignment = hungarian(cost)
    if verbose:
        matches, total = format_matches(score_df, assignment)
        print("\n🔗 Optimal tutor–murid pairing (Hungarian):")
        for t, m, s in matches:
            print(f"{t} → {m} (skor: {s})")
        print(f"\n✅ Total skor maksimum: {total}")
    return assignment
