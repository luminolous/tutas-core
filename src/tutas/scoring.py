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
    """Hitung matriks skor antara tutor dan murid, lalu pad agar persegi."""

    def score_row(t: pd.Series, s: pd.Series) -> int:
        return sum(
            w for attr, w in weights.items()
            if t.get(attr) == s.get(attr)
        )

    num_tutors, num_students = len(tutors), len(students)
    mat = np.zeros((num_tutors, num_students), dtype=int)

    for i in range(len(tutors)):
        t = tutors.iloc[i]
        for j in range(len(students)):
            s = students.iloc[j]
            mat[i, j] = score_row(t, s)


    tutor_names = tutors["fullName"].tolist() if "fullName" in tutors.columns else [f"Tutor{i}" for i in range(num_tutors)]
    student_names = students["fullName"].tolist() if "fullName" in students.columns else [f"Student{j}" for j in range(num_students)]

    # Padding agar square
    diff = abs(num_tutors - num_students)
    if num_tutors < num_students:
        # Tambah dummy tutor
        dummy_rows = np.zeros((diff, num_students), dtype=int)
        mat = np.vstack([mat, dummy_rows])
        tutor_names += [f"DUMMY_TUTOR_{i+1}" for i in range(diff)]
    elif num_students < num_tutors:
        # Tambah dummy murid
        dummy_cols = np.zeros((num_tutors, diff), dtype=int)
        mat = np.hstack([mat, dummy_cols])
        student_names += [f"DUMMY_STUDENT_{j+1}" for j in range(diff)]

    return pd.DataFrame(mat, index=tutor_names, columns=student_names)
