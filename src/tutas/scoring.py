import pandas as pd
import numpy as np

def load_dummy_tutors() -> pd.DataFrame:
    """Kembalikan DataFrame tutor dengan 4 atribut: Topik, Gaya, Mode, Waktu."""
    return pd.DataFrame({
        "Nama": ["Tutor1", "Tutor2", "Tutor3", "Tutor4", "Tutor5"],
        "Topik": ["Kalkulus", "Struktur Data", "Statistika", "Struktur Data", "Kalkulus"],
        "Gaya": ["Visual", "Diskusi", "Latihan", "Visual", "Diskusi"],
        "Mode": ["Online", "Offline", "Online", "Chat", "Offline"],
        "Waktu": ["Senin", "Senin", "Selasa", "Rabu", "Kamis"]
    })

def load_dummy_students() -> pd.DataFrame:
    """Kembalikan DataFrame murid dengan 4 atribut: Topik, Gaya, Mode, Waktu."""
    return pd.DataFrame({
        "Nama": ["Murid1", "Murid2", "Murid3", "Murid4", "Murid5"],
        "Topik": ["Kalkulus", "Struktur Data", "Statistika", "Kalkulus", "Struktur Data"],
        "Gaya": ["Visual", "Diskusi", "Latihan", "Diskusi", "Visual"],
        "Mode": ["Online", "Offline", "Online", "Chat", "Offline"],
        "Waktu": ["Senin", "Senin", "Selasa", "Rabu", "Kamis"]
    })

def compute_score_matrix(
    tutors: pd.DataFrame,
    students: pd.DataFrame,
    weights: dict[str, int] = {"Topik": 5, "Gaya": 3, "Mode": 2, "Waktu": 1}
) -> pd.DataFrame:
    """Hitung matriks skor kecocokan tutor–murid berdasarkan 4 parameter."""
    def score_row(t: pd.Series, m: pd.Series) -> int:
        return sum(
            w for attr, w in weights.items() if t[attr] == m[attr]
        )

    mat = np.zeros((len(tutors), len(students)), dtype=int)
    for i, t in tutors.iterrows():
        for j, m in students.iterrows():
            mat[i, j] = score_row(t, m)

    return pd.DataFrame(mat, index=tutors["Nama"], columns=students["Nama"])

def matriks() -> pd.DataFrame:
    """Wrapper: load dummy data, compute score, print matrix."""
    tutors = load_dummy_tutors()
    students = load_dummy_students()
    score_df = compute_score_matrix(tutors, students)
    print("\n📊 Matriks Skor Kecocokan Tutor–Murid:\n")
    print(score_df)
    return score_df
