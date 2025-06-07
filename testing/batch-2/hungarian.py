from scipy.optimize import linear_sum_assignment
from test_matriks import matriks

def hungarian(cost):
    """
    Input:
      cost : matriks bujur-sangkar (n×n), list of lists atau np.ndarray
    Output:
      assignment : list panjang n, di mana assignment[i] = j
                   artinya baris i dipasangkan ke kolom j
    """
    n = len(cost)
    # Potensial baris (u) dan kolom (v), serta arrays bantu p dan way
    u = [0]*(n+1)
    v = [0]*(n+1)
    p = [0]*(n+1)
    way = [0]*(n+1)

    # Untuk tiap baris i
    for i in range(1, n+1):
        p[0] = i
        j0 = 0
        minv = [float('inf')]*(n+1)
        used = [False]*(n+1)

        # Cari augmenting path
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = 0
            for j in range(1, n+1):
                if not used[j]:
                    # reduced cost
                    cur = cost[i0-1][j-1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            # Update potentials
            for j in range(n+1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break

        # Reconstruct augmenting path
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    # Susun hasil akhir
    assignment = [-1]*n
    for j in range(1, n+1):
        if p[j] != 0:
            assignment[p[j]-1] = j-1

    return assignment


df_score = matriks()

score_values = df_score.values
max_score = score_values.max()
cost_matrix = (max_score - score_values).tolist()

# Jalankan manual Hungarian
assignment = hungarian(cost_matrix)

# Cetak hasilnya seperti sebelumnya
tutors = df_score.index.tolist()
murids = df_score.columns.tolist()
total = 0
for i, j in enumerate(assignment):
    s = score_values[i][j]
    print(f"{tutors[i]} → {murids[j]} (skor: {s})")
    total += s
print("Total skor maksimum:", total)
