
import networkx as nx
from collections import defaultdict
import pandas as pd

# === Data preferensi pengguna ===
data_user = {
    "user01": {"gaya": {"Visual & konsep"}, "waktu": {"Senin malam", "Jumat pagi"}, "mode": {"Online – Video Call"}, "matkul": {"Kalkulus"}, "topik": {"Integral Parsial"}},
    "user02": {"gaya": {"Langsung latihan soal"}, "waktu": {"Senin malam"}, "mode": {"Offline (sekitar ITS)"}, "matkul": {"Kalkulus"}, "topik": {"Integral Parsial"}},
    "user03": {"gaya": {"Visual & konsep", "Diskusi dua arah"}, "waktu": {"Jumat pagi"}, "mode": {"Online – Video Call"}, "matkul": {"Struktur Data"}, "topik": {"Pointer di C++"}},
    "user04": {"gaya": {"Diskusi dua arah"}, "waktu": {"Senin malam", "Rabu sore"}, "mode": {"Chat Diskusi (WA/Telegram)"}, "matkul": {"Struktur Data"}, "topik": {"Pointer di C++"}},
    "user05": {"gaya": {"Langsung latihan soal"}, "waktu": {"Jumat pagi"}, "mode": {"Offline (sekitar ITS)"}, "matkul": {"Statistika"}, "topik": {"Distribusi Binomial"}},
}

# === Fungsi Kemiripan ===
def similarity(u1, u2):
    score = 0
    if u1["matkul"] == u2["matkul"]:
        score += 0.4
    if u1["topik"] == u2["topik"]:
        score += 0.4
    gaya_sim = len(u1["gaya"] & u2["gaya"]) / len(u1["gaya"] | u2["gaya"])
    waktu_sim = len(u1["waktu"] & u2["waktu"]) / len(u1["waktu"] | u2["waktu"])
    mode_sim = len(u1["mode"] & u2["mode"]) / len(u1["mode"] | u2["mode"])
    score += 0.1 * gaya_sim + 0.05 * waktu_sim + 0.05 * mode_sim
    return score

# === Buat Graph ===
G = nx.Graph()
for u in data_user:
    G.add_node(u)
user_list = list(data_user.keys())
for i in range(len(user_list)):
    for j in range(i + 1, len(user_list)):
        sim = similarity(data_user[user_list[i]], data_user[user_list[j]])
        if sim > 0:
            G.add_edge(user_list[i], user_list[j], weight=sim)

# === Fungsi Modularitas & Optimasi ===
def calculate_modularity(G, partition):
    m = sum(d['weight'] for _, _, d in G.edges(data=True))
    degrees = dict(G.degree(weight='weight'))
    Q = 0
    for community in set(partition.values()):
        nodes = [n for n in G.nodes() if partition[n] == community]
        for i in nodes:
            for j in nodes:
                A_ij = G[i][j]['weight'] if G.has_edge(i, j) else 0
                Q += A_ij - (degrees[i] * degrees[j]) / (2 * m)
    return Q / (2 * m)

def modularity_gain(G, node, target_community, partition, m, degrees):
    k_i = degrees[node]
    k_i_in = sum(G[node][n]['weight'] for n in G[node] if partition[n] == target_community)
    sum_tot = sum(degrees[n] for n in G.nodes() if partition[n] == target_community)
    sum_in = sum(G[u][v]['weight'] for u, v in G.edges() if partition[u] == partition[v] == target_community) / 2
    delta_Q = ((sum_in + k_i_in) / (2 * m) - ((sum_tot + k_i) / (2 * m))**2) - (sum_in / (2 * m) - (sum_tot / (2 * m))**2)
    return delta_Q

def optimize_partition(G, partition):
    m = sum(d['weight'] for _, _, d in G.edges(data=True))
    degrees = dict(G.degree(weight='weight'))
    improved = True
    while improved:
        improved = False
        for node in G.nodes():
            best_community = partition[node]
            best_increase = 0
            neighbor_comms = {partition[n] for n in G.neighbors(node)}
            for comm in neighbor_comms:
                delta_q = modularity_gain(G, node, comm, partition, m, degrees)
                if delta_q > best_increase:
                    best_increase = delta_q
                    best_community = comm
            if best_community != partition[node]:
                partition[node] = best_community
                improved = True
    return partition

# === Agregasi dan Louvain ===
def aggregate_graph(G, partition):
    newG = nx.Graph()
    weights = defaultdict(float)
    for u, v, data in G.edges(data=True):
        cu, cv = partition[u], partition[v]
        if cu == cv:
            weights[(cu, cu)] += data['weight']
        else:
            key = tuple(sorted((cu, cv)))
            weights[key] += data['weight']
    for (u, v), w in weights.items():
        newG.add_edge(u, v, weight=w)
    return newG

# Versi revisi fungsi louvain_manual dengan pengecekan dan log tambahanimport pandas as pd

def louvain_manual_debug(G):
    if G.number_of_edges() == 0:
        print("⚠️ Graf tidak memiliki edge. Tidak ada kemiripan antar user.")
        return {}

    current_G = G.copy()
    partition = {node: i for i, node in enumerate(G.nodes())}
    name_map = {i: [node] for i, node in enumerate(G.nodes())}

    while True:
        optimized = optimize_partition(current_G, partition.copy())
        if optimized == partition:
            break

        new_map = defaultdict(list)
        for node, cid in optimized.items():
            if node in name_map:
                for original in name_map[node]:
                    new_map[cid].append(original)

        if not new_map:
            print("⚠️ Pemetaan komunitas kosong setelah agregasi.")
            break

        current_G = aggregate_graph(current_G, optimized)
        partition = {node: node for node in current_G.nodes()}
        name_map = new_map

    result = {}
    for cid, members in name_map.items():
        for m in members:
            result[m] = cid

    if not result:
        print("⚠️ Tidak ada hasil partisi yang terbentuk.")
    else:
        print(f"\n✅ Komunitas berhasil terbentuk untuk {len(result)} user.")
        print("Hasil akhir partisi:")

        # Tampilkan hasil dalam bentuk tabel
        df = pd.DataFrame([(u, c) for u, c in result.items()], columns=["User", "Circle"])
        print(df.to_string(index=False))

    return result

# Cek isi graf sebelum proses Louvain
print("📊 Edge yang terbentuk:")
for u, v, d in G.edges(data=True):
    print(f"{u} – {v} → weight: {d['weight']:.2f}")

# Jalankan versi debug
final_partition = louvain_manual_debug(G)
