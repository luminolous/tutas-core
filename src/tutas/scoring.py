import pandas as pd
import numpy as np

def load_dummy_tutors() -> pd.DataFrame:
    """Kembalikan DataFrame tutor dengan kolom Nama, Topik, Gaya, Mode."""
    return pd.DataFrame({
        "Nama": ["Tutor1", "Tutor2", "Tutor3", "Tutor4", "Tutor5"],
        "Topik": ["Kalkulus", "Struktur Data", "Statistika", "Struktur Data", "Kalkulus"],
        "Gaya": ["Visual", "Diskusi", "Latihan", "Visual", "Diskusi"],
        "Mode": ["Online", "Offline", "Online", "Chat", "Offline"]
    })

def load_dummy_students() -> pd.DataFrame:
    """Kembalikan DataFrame murid dengan kolom Nama, Topik, Gaya, Mode."""
    return pd.DataFrame({
        "Nama": ["Murid1", "Murid2", "Murid3", "Murid4", "Murid5"],
        "Topik": ["Kalkulus", "Struktur Data", "Statistika", "Kalkulus", "Struktur Data"],
        "Gaya": ["Visual", "Diskusi", "Latihan", "Diskusi", "Visual"],
        "Mode": ["Online", "Offline", "Online", "Chat", "Offline"]
    })

def compute_score_matrix(
    tutors: pd.DataFrame,
    students: pd.DataFrame,
    weights: dict[str,int] = {"Topik":5, "Gaya":3, "Mode":2}
) -> pd.DataFrame:
    """
    Hitung matriks skor kecocokan tutor–murid.
    weights memberi bobot untuk setiap atribut.
    """
    def score_row(t: pd.Series, m: pd.Series) -> int:
        s = 0
        for attr, w in weights.items():
            if t[attr] == m[attr]:
                s += w
        return s

    n_t, n_s = len(tutors), len(students)
    mat = np.zeros((n_t, n_s), dtype=int)
    for i, tut in tutors.iterrows():
        for j, stu in students.iterrows():
            mat[i, j] = score_row(tut, stu)

    df = pd.DataFrame(mat,
                      index=tutors["Nama"].tolist(),
                      columns=students["Nama"].tolist())
    return df

def matriks() -> pd.DataFrame:
    """
    Wrapper seperti dulu: load dummy, compute, print, return DataFrame.
    """
    tutors  = load_dummy_tutors()
    students= load_dummy_students()
    df_score= compute_score_matrix(tutors, students)
    print("\n📊 Matriks Skor Kecocokan Tutor–Murid:\n")
    print(df_score)
    return df_score
