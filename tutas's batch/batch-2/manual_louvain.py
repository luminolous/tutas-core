import pandas as pd
import networkx as nx
from itertools import combinations
from collections import defaultdict, Counter

# ========== PARAMETER ==========
MAX_CIRCLE_SIZE = 5
INPUT_FILE = "data/dummy/dummy_circle_input.csv"
OUTPUT_CIRCLE = "data/output/circle_output_3.csv"
OUTPUT_UNMATCHED = "data/output/unmatched.csv"
THRESHOLD = 0.7

# ——————————————————————————————————————————————————————————————
# FUNGSI-FUNGSI LOUVAIN MANUAL
# ——————————————————————————————————————————————————————————————

def compute_modularity(G, partition, m):
    """
    Hitung modularity berdasarkan formula:
      Q = (1/2m) * Σ_{ij} [ A_ij - (k_i * k_j)/(2m) ] * δ(c_i, c_j)
    di mana:
      - m = total bobot semua edge
      - A_ij = weight antara node i dan j (0 jika tidak terhubung)
      - k_i = derajat (weighted) node i
      - c_i = komunitas node i
      - δ = 1 jika c_i == c_j, 0 otherwise
    """
    Q = 0.0
    # precompute degrees
    degrees = dict(G.degree(weight='weight'))
    for u, v, data in G.edges(data=True):
        w = data.get('weight', 1)
        if partition[u] == partition[v]:
            Q += w - degrees[u] * degrees[v] / (2*m)
    return Q / (2*m)

def one_level(G, partition, m):
    """
    Lakukan phase 1 Louvain: **local moving**.
    - Iterasi node, coba pindahkan ke komunitas tetangga yang memberi gain modularity terbesar.
    """
    improved = True
    # index komunitas ke list node
    community2nodes = defaultdict(set)
    for node, com in partition.items():
        community2nodes[com].add(node)

    # precompute node degrees
    degrees = dict(G.degree(weight='weight'))

    while improved:
        improved = False
        # random order agar tidak bias
        for node in list(G.nodes()):
            node_com = partition[node]
            # total degree incidence node ke komunitas target
            neigh_com2weight = defaultdict(float)
            for nbr, data in G[node].items():
                neigh_com2weight[partition[nbr]] += data.get('weight', 1)

            # hitung loss dari komunitas asal
            tot_com = sum(degrees[n] for n in community2nodes[node_com])
            ki = degrees[node]
            ki_in = neigh_com2weight[node_com]
            best_gain = 0.0
            best_com = node_com

            # remove node sementara dari komunitas asal
            community2nodes[node_com].remove(node)
            # perbandingan dengan memindah ke tiap komunitas tetangga
            for com, w_in in neigh_com2weight.items():
                tot_com_target = sum(degrees[n] for n in community2nodes[com])
                # formula ΔQ dari Blondel et al.
                gain = (w_in - ki * tot_com_target / (2*m)) / (2*m)
                if gain > best_gain:
                    best_gain = gain
                    best_com = com

            # jika komunitas berubah, terapkan
            if best_com != node_com:
                partition[node] = best_com
                community2nodes[best_com].add(node)
                improved = True
            else:
                # kembalikan node ke komunitas asal
                community2nodes[node_com].add(node)

    return partition

def aggregate_graph(G, partition):
    """
    Phase 2 Louvain: **aggregation**.
    - Bentuk graf baru di mana setiap komunitas menjadi satu node,
      dan bobot antara komunitas = jumlah bobot edge antar node di komunitas asal.
    """
    newG = nx.Graph()
    # hitung bobot antar komunitas
    weight_between = defaultdict(float)
    for u, v, data in G.edges(data=True):
        cu, cv = partition[u], partition[v]
        w = data.get('weight', 1)
        if cu == cv:
            weight_between[(cu, cu)] += w
        else:
            weight_between[(cu, cv)] += w
            weight_between[(cv, cu)] += w

    # tambahkan node dan edge ke graf baru
    for (cu, cv), w in weight_between.items():
        newG.add_edge(cu, cv, weight=w)

    return newG

def louvain(G, tol=1e-6):
    # mapping: komunitas sekarang → set node asli di dalamnya
    mapping = {n: {n} for n in G.nodes()}
    # inisialisasi partition pada graf asli
    partition = {n: i for i, n in enumerate(G.nodes())}
    m = G.size(weight='weight')
    cur_mod = compute_modularity(G, partition, m)

    while True:
        # Phase-1: local moving
        partition = one_level(G, partition, m)
        new_mod = compute_modularity(G, partition, m)

        if new_mod - cur_mod > tol:
            cur_mod = new_mod

            # rebuild mapping: setiap komunitas → gabungan semua node asli
            community2nodes = defaultdict(list)
            for node, com in partition.items():
                community2nodes[com].append(node)

            new_mapping = {}
            for com, nodes in community2nodes.items():
                # union dari semua set mapping[node]
                union_set = set()
                for node in nodes:
                    union_set |= mapping[node]
                new_mapping[com] = union_set
            mapping = new_mapping

            # Phase-2: aggregate dan ulangi
            G = aggregate_graph(G, partition)
            partition = {n: i for i, n in enumerate(G.nodes())}
            m = G.size(weight='weight')
        else:
            break

    # Flatten mapping jadi partition akhir untuk semua node asli
    final_part = {}
    for com, orig_nodes in mapping.items():
        for node in orig_nodes:
            final_part[node] = com
    return final_part


# ——————————————————————————————————————————————————————————————
# UTAMA: Load data, bangun similarity graph, jalankan Louvain manual
# ——————————————————————————————————————————————————————————————

# STEP 1: LOAD & FILTER DATA
df = pd.read_csv(INPUT_FILE)
df.fillna("", inplace=True)
df_valid = df[df["Topik"] != ""].reset_index(drop=True)
df_invalid = df[df["Topik"] == ""].reset_index(drop=True)

print("⭑ Total baris input       :", len(df))
print("⭑ Baris valid (Topik ada):", len(df_valid))

# STEP 2: BANGUN GRAF SIMILARITY
G = nx.Graph()
def feature_string(row):
    return " ".join([row["Topik"], row["Mode"], row["Gaya"]]).lower()
df_valid["features"] = df_valid.apply(feature_string, axis=1)

# TF-IDF + Cosine Similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
tfidf = TfidfVectorizer()
tfidf_mat = tfidf.fit_transform(df_valid["features"])
sim_mat = cosine_similarity(tfidf_mat)

# tambahkan edge hanya jika TOPIK sama *dan* similarity ≥ threshold
for i, j in combinations(range(len(df_valid)), 2):
    if df_valid.loc[i, "Topik"] != df_valid.loc[j, "Topik"]:
        continue            # skip jika topiknya berbeda
    w = sim_mat[i, j]
    if w >= THRESHOLD:
        u = df_valid.loc[i, "Nama"]
        v = df_valid.loc[j, "Nama"]
        G.add_edge(u, v, weight=w)

# pastikan semua node ada
for name in df_valid["Nama"]:
    if name not in G:
        G.add_node(name)

print("⭑ Nodes di graf :", G.number_of_nodes())
print("⭑ Edges di graf :", G.number_of_edges())

# STEP 3: JALANKAN LOUVAIN MANUAL
partition = louvain(G)
df_valid["Circle ID"] = df_valid["Nama"].map(partition)

from collections import Counter
print("⭑ Community sizes:", Counter(partition.values()))

# ========== STEP 4: BANGUN SUB-GRUP DENGAN MAX: 1 TUTOR, 4 MURID ==========
circle_groups = df_valid.groupby("Circle ID")
circle_result = []
new_circle_id = 0

for cid, group in circle_groups:
    # Pisahkan tutor & murid
    tutors   = group[group["Status"]=="Tutor"].to_dict("records")
    students = group[group["Status"]=="Murid"].to_dict("records")

    # 1) Untuk setiap tutor, bikin sub-grup: [tutor + up to 4 murid]
    for t in tutors:
        assigned_students = students[:4]     # ambil 4 murid pertama
        students = students[4:]             # sisa murid
        sub = [t] + assigned_students
        circle_result.append((new_circle_id, sub))
        new_circle_id += 1

    # 2) Sisa murid → kelompok murid saja, 4 orang per sub-grup
    while len(students) > 0:
        sub_students = students[:4]
        students = students[4:]
        circle_result.append((new_circle_id, sub_students))
        new_circle_id += 1

    # 3) (Opsional) Jika ada tutor “tersisa” (jarang), masukkan sendiri
    #    — tapi biasanya tutors habis di langkah 1
    for t in tutors[len(tutors):]:
        circle_result.append((new_circle_id, [t]))
        new_circle_id += 1

# Setelah ini, circle_result berisi list of (CircleID, list_of_rows)
# Lanjutkan STEP 5: simpan ke CSV seperti biasa
output_rows = []
for cid, rows in circle_result:
    for row in rows:
        output_rows.append({
            "Nama"       : row["Nama"],
            "Circle ID"  : cid,
            "Tutor/Murid": row["Status"],
            "No WA"      : row["No WA"]
        })

df_output = pd.DataFrame(output_rows)
df_output.to_csv(OUTPUT_CIRCLE, index=False)
print(f"✅ Disimpan: {OUTPUT_CIRCLE}")


