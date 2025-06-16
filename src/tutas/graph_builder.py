import networkx as nx
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_similarity_graph(df, THRESHOLD):
    G = nx.Graph()
    def feature_string(row):
        return " ".join([row["Topik"], row["Mode"], row["Gaya"]]).lower()
    df["features"] = df.apply(feature_string, axis=1)

    # TF-IDF + Cosine Similarity
    tfidf = TfidfVectorizer()
    tfidf_mat = tfidf.fit_transform(df["features"])
    sim_mat = cosine_similarity(tfidf_mat)

    # tambahkan edge hanya jika TOPIK sama dan similarity ≥ threshold
    for i, j in combinations(range(len(df)), 2):
        if df.loc[i, "Topik"] != df.loc[j, "Topik"]:
            continue
        w = sim_mat[i, j]
        if w >= THRESHOLD:
            u = df.loc[i, "Nama"]
            v = df.loc[j, "Nama"]
            G.add_edge(u, v, weight=w)

    # memastikan semua node ada
    for name in df["Nama"]:
        if name not in G:
            G.add_node(name)

    print("Daftar node:")
    for n in G.nodes():
        print(" •", n)

    # Edges + bobot
    print("\nDaftar edge (u, v, weight):")
    for u, v, data in G.edges(data=True):
        print(f" • {u}  —  {v}   (w = {data['weight']:.3f})")
    return G