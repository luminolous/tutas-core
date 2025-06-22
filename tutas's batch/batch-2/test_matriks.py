import pandas as pd
import numpy as np

# === Data Dummy Tutor ===
tutor_data = pd.DataFrame({
    "Nama": ["Tutor1", "Tutor2", "Tutor3", "Tutor4", "Tutor5"],
    "Topik": ["Kalkulus", "Struktur Data", "Statistika", "Struktur Data", "Kalkulus"],
    "Gaya": ["Visual", "Diskusi", "Latihan", "Visual", "Diskusi"],
    "Mode": ["Online", "Offline", "Online", "Chat", "Offline"]
})

# === Data Dummy Murid ===
murid_data = pd.DataFrame({
    "Nama": ["Murid1", "Murid2", "Murid3", "Murid4", "Murid5"],
    "Topik": ["Kalkulus", "Struktur Data", "Statistika", "Kalkulus", "Struktur Data"],
    "Gaya": ["Visual", "Diskusi", "Latihan", "Diskusi", "Visual"],
    "Mode": ["Online", "Offline", "Online", "Chat", "Offline"]
})

# === Fungsi Skor Kecocokan ===
def matriks():
    def score(tutor, murid):
        s = 0
        if tutor["Topik"] == murid["Topik"]:
            s += 5
        if tutor["Gaya"] == murid["Gaya"]:
            s += 3
        if tutor["Mode"] == murid["Mode"]:
            s += 2
        return s

    # === Buat Matriks Skor ===
    score_matrix = np.zeros((len(tutor_data), len(murid_data)), dtype=int)
    for i, t in tutor_data.iterrows():
        for j, m in murid_data.iterrows():
            score_matrix[i, j] = score(t, m)

    # === Tampilkan Matriks Skor ===
    df_score = pd.DataFrame(score_matrix, index=tutor_data["Nama"], columns=murid_data["Nama"])
    print("\n📊 Matriks Skor Kecocokan Tutor–Murid:\n")
    print(df_score)
    return df_score
