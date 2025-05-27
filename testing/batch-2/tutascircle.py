import networkx as nx
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt

#Data preferensi pengguna dari form
data_user = {
    "user01": {
        "gaya": {"Visual & konsep"},
        "waktu": {"Senin malam", "Jumat pagi"},
        "mode": {"Online – Video Call"},
        "matkul": {"Kalkulus"},
        "topik": {"Integral Parsial"}
    },
    "user02": {
        "gaya": {"Langsung latihan soal"},
        "waktu": {"Senin malam"},
        "mode": {"Offline (sekitar ITS)"},
        "matkul": {"Kalkulus"},
        "topik": {"Integral Parsial"}
    },
    "user03": {
        "gaya": {"Visual & konsep", "Diskusi dua arah"},
        "waktu": {"Jumat pagi"},
        "mode": {"Online – Video Call"},
        "matkul": {"Struktur Data"},
        "topik": {"Pointer di C++"}
    },
    "user04": {
        "gaya": {"Diskusi dua arah"},
        "waktu": {"Senin malam", "Rabu sore"},
        "mode": {"Chat Diskusi (WA/Telegram)"},
        "matkul": {"Struktur Data"},
        "topik": {"Pointer di C++"}
    },
    "user05": {
        "gaya": {"Langsung latihan soal"},
        "waktu": {"Jumat pagi"},
        "mode": {"Offline (sekitar ITS)"},
        "matkul": {"Statistika"},
        "topik": {"Distribusi Binomial"}
    },
}

#Fungsi kemiripan antar user berdasarkan semua parameter
def similarity(u1, u2):
    if u1["matkul"] != u2["matkul"] or u1["topik"] != u2["topik"]:
        return 0  # tidak bisa satu circle jika matkul atau topik beda

    gaya_sim = len(u1["gaya"] & u2["gaya"]) / len(u1["gaya"] | u2["gaya"])
    waktu_sim = len(u1["waktu"] & u2["waktu"]) / len(u1["waktu"] | u2["waktu"])
    mode_sim = len(u1["mode"] & u2["mode"]) / len(u1["mode"] | u2["mode"])

    return 0.5 * gaya_sim + 0.3 * waktu_sim + 0.2 * mode_sim

#Membuat graf tak berarah antar user
G = nx.Graph()
for user in data_user:
    G.add_node(user)

user_list = list(data_user.keys())
for i in range(len(user_list)):
    for j in range(i + 1, len(user_list)):
        u1 = user_list[i]
        u2 = user_list[j]
        sim = similarity(data_user[u1], data_user[u2])
        if sim > 0:
            G.add_edge(u1, u2, weight=sim)

#Jalankan Louvain untuk deteksi komunitas
partition = community_louvain.best_partition(G)

#Cetak hasil komunitas
print("\nHasil Pembentukan Tutas Circle:")
for user, komunitas in partition.items():
    print(f"{user} tergabung dalam Circle {komunitas}")

#Visualisasi
pos = nx.spring_layout(G, seed=42)
colors = [partition[n] for n in G.nodes()]
plt.figure(figsize=(10, 6))
nx.draw_networkx(G, pos, with_labels=True, node_color=colors, cmap=plt.cm.Set3, node_size=1000)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}, font_size=8)
plt.title("Visualisasi Tutas Circle (Algoritma Louvain)")
plt.axis("off")
plt.show()
