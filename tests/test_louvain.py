import pandas as pd
import networkx as nx
import pytest

from src.tutas.louvain.louvain import louvain
from src.tutas.graph_builder import build_similarity_graph
from src.tutas.grouping import make_subgroups
from src.tutas.config import THRESHOLD


def test_build_similarity_graph_threshold():
    # Dua topik berbeda, threshold = config
    df = pd.DataFrame([
        {"Nama": "A", "Topik": "X", "Mode": "Online", "Gaya": "Visual"},
        {"Nama": "B", "Topik": "X", "Mode": "Online", "Gaya": "Visual"},
        {"Nama": "C", "Topik": "Y", "Mode": "Offline", "Gaya": "Kinesthetic"},
    ])
    G = build_similarity_graph(df, THRESHOLD)
    assert set(G.nodes) == {"A", "B", "C"}
    assert G.has_edge("A", "B")
    assert not G.has_edge("A", "C")
    assert not G.has_edge("B", "C")


def test_louvain_mendeteksi_dua_komunitas():
    # Dua clique terpisah
    G = nx.Graph()
    group1 = ["n1", "n2", "n3"]
    group2 = ["n4", "n5", "n6"]
    for grp in (group1, group2):
        for u in grp:
            for v in grp:
                if u < v:
                    G.add_edge(u, v)
    partition = louvain(G)
    clusters = {}
    for node, com in partition.items():
        clusters.setdefault(com, []).append(node)
    parts = list(clusters.values())
    assert any(set(group1) == set(p) for p in parts)
    assert any(set(group2) == set(p) for p in parts)


def test_make_subgroups_satu_grup():
    # 1 tutor + 2 murid dalam satu komunitas, menggunakan Nama sebagai key
    df_circle = pd.DataFrame([
        {"Nama":"Tutor1","No WA":"T1","courseName":"C","Topik":"T","Mode":"Online","Gaya":"Visual","Status":"Tutor","preferredDate":"2025-07-01","preferredTime":"09:00"},
        {"Nama":"StuA","No WA":"S1","courseName":"C","Topik":"T","Mode":"Online","Gaya":"Visual","Status":"Murid","preferredDate":"2025-07-02","preferredTime":"10:00"},
        {"Nama":"StuB","No WA":"S2","courseName":"C","Topik":"T","Mode":"Online","Gaya":"Visual","Status":"Murid","preferredDate":"2025-07-03","preferredTime":"11:00"},
    ]).reset_index(drop=True)
    # Partition berbasis Nama (semua di komunitas 0)
    partition = {row["Nama"]: 0 for row in df_circle.to_dict(orient="records")}
    rows = make_subgroups(df_circle, partition, max_size=3)
    # Harus ada 3 baris dengan Circle ID 0
    assert len(rows) == 3
    ids = {r["Circle ID"] for r in rows}
    assert ids == {0}
    tutors = [r for r in rows if r["Tutor/Murid"] == "Tutor"]
    students = [r for r in rows if r["Tutor/Murid"] == "Murid"]
    assert len(tutors) == 1 and tutors[0]["Nama"] == "Tutor1"
    assert {r["Nama"] for r in students} == {"StuA", "StuB"}
