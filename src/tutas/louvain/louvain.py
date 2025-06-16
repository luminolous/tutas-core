from collections import defaultdict
import networkx as nx

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
    Lakukan phase 1 Louvain: local moving.
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
                # formula ΔQ dari Blondel et al., 2008
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
    Phase 2 Louvain: aggregation.
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
