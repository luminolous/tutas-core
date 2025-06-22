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
        "preferredDate": 1,
        "preferredTime": 1  # baru ditambah
    }
) -> pd.DataFrame:
    """Hitung matriks skor antara tutor dan murid, lalu pad agar persegi."""

    def score_row(t: pd.Series, s: pd.Series) -> int:
        total = 0
        for attr, w in weights.items():
            # Tangani atribut tanggal & waktu dengan fleksibilitas
            if attr in ["preferredDate", "preferredTime"]:
                flex_t = str(t.get("flexibleSchedule", "")).lower() == "yes"
                flex_s = str(s.get("flexibleSchedule", "")).lower() == "yes"
                if flex_t or flex_s:
                    total += w
                elif t.get(attr) == s.get(attr):
                    total += w
            else:
                if t.get(attr) == s.get(attr):
                    total += w
        return total

    num_tutors, num_students = len(tutors), len(students)
    mat = np.zeros((num_tutors, num_students), dtype=int)

    for i in range(num_tutors):
        t = tutors.iloc[i]
        for j in range(num_students):
            s = students.iloc[j]
            mat[i, j] = score_row(t, s)

    tutor_names = tutors["fullName"].tolist() if "fullName" in tutors.columns else [f"Tutor{i}" for i in range(num_tutors)]
    student_names = students["fullName"].tolist() if "fullName" in students.columns else [f"Student{j}" for j in range(num_students)]

    # Padding agar matriks jadi persegi
    diff = abs(num_tutors - num_students)
    if num_tutors < num_students:
        dummy_rows = np.zeros((diff, num_students), dtype=int)
        mat = np.vstack([mat, dummy_rows])
        tutor_names += [f"DUMMY_TUTOR_{i+1}" for i in range(diff)]
    elif num_students < num_tutors:
        dummy_cols = np.zeros((num_tutors, diff), dtype=int)
        mat = np.hstack([mat, dummy_cols])
        student_names += [f"DUMMY_STUDENT_{j+1}" for j in range(diff)]

    return pd.DataFrame(mat, index=tutor_names, columns=student_names)
