import pandas as pd
import numpy as np

def compute_score_matrix(
    tutors: pd.DataFrame,
    students: pd.DataFrame,
    weights: dict[str, int] = {
        "courseName": 4,
        "topicSubtopic": 5,
        "learningStyle": 3,
        "learningMode": 2,
        "preferredDate": 1
    }
) -> pd.DataFrame:
    """
    Hitung matriks skor tutor–murid berdasarkan atribut (5 fitur).
    Matriks otomatis dipad ke bentuk persegi jika jumlah tutor ≠ murid.
    """

    def score_row(t: pd.Series, s: pd.Series) -> int:
        return sum(
            w for attr, w in weights.items()
            if t.get(attr, "").strip().lower() == s.get(attr, "").strip().lower()
        )

    rows = len(tutors)
    cols = len(students)
    mat = np.zeros((rows, cols), dtype=int)

    for i, t in tutors.iterrows():
        for j, s in students.iterrows():
            mat[i, j] = score_row(t, s)

    # Nama asli
    tutor_names = tutors["fullName"].tolist() if "fullName" in tutors.columns else list(tutors.index)
    student_names = students["fullName"].tolist() if "fullName" in students.columns else list(students.index)

    # Buat square matrix jika jumlah tutor ≠ jumlah murid
    size = max(rows, cols)
    square_mat = np.zeros((size, size), dtype=int)
    square_mat[:rows, :cols] = mat

    # Tambahkan dummy names
    while len(tutor_names) < size:
        tutor_names.append(f"DUMMY_TUTOR_{len(tutor_names) + 1}")
    while len(student_names) < size:
        student_names.append(f"DUMMY_STUDENT_{len(student_names) + 1}")

    return pd.DataFrame(square_mat, index=tutor_names, columns=student_names)
