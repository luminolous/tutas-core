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
    """Hitung matriks skor kecocokan tutor–murid berdasarkan atribut dan pad jadi square."""

    def score_row(t: pd.Series, s: pd.Series) -> int:
        return sum(
            w for attr, w in weights.items() if t.get(attr) == s.get(attr)
        )

    mat = np.zeros((len(tutors), len(students)), dtype=int)
    for i, t in tutors.iterrows():
        for j, s in students.iterrows():
            mat[i, j] = score_row(t, s)

    # Ambil nama
    tutor_names = tutors["fullName"].tolist()
    student_names = students["fullName"].tolist()

    # Pad supaya square
    n = max(len(tutor_names), len(student_names))
    while len(tutor_names) < n:
        tutor_names.append(f"DUMMY_TUTOR_{len(tutor_names)+1}")
    while len(student_names) < n:
        student_names.append(f"DUMMY_MURID_{len(student_names)+1}")

    padded_mat = np.zeros((n, n), dtype=int)
    padded_mat[:len(tutors), :len(students)] = mat

    return pd.DataFrame(padded_mat, index=tutor_names, columns=student_names)
