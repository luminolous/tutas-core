import pandas as pd
from src.tutas.scoring import compute_score_matrix
from src.tutas.hungarian.matching import match_tutors, format_matches_unitest

# 🧪 Test: Matching 1-on-1 dengan preferensi waktu dan fleksibilitas
def test_matching_1on1_with_time_flexibility():
    # 🔹 Data dummy 2 tutor
    tutors = pd.DataFrame([
        {
            "fullName": "Bob Wijaya",
            "courseName": "Physics",
            "topicSubtopic": "Mechanics",
            "learningStyle": "Kinesthetic Learning",
            "learningMode": "Offline near ITS",
            "preferredDate": "2025-07-02",
            "preferredTime": "14:00",
            "flexibleSchedule": "No",
        },
        {
            "fullName": "Tutor B",
            "courseName": "Math",
            "topicSubtopic": "Algebra",
            "learningStyle": "Visual Learning",
            "learningMode": "Online",
            "preferredDate": "2025-07-03",
            "preferredTime": "10:00",
            "flexibleSchedule": "Yes",
        }
    ])

    # 🔹 Data dummy 2 murid
    students = pd.DataFrame([
        {
            "fullName": "Ali",
            "courseName": "Physics",
            "topicSubtopic": "Mechanics",
            "learningStyle": "Kinesthetic Learning",
            "learningMode": "Offline near ITS",
            "preferredDate": "2025-07-02",
            "preferredTime": "14:00",
            "flexibleSchedule": "Yes",  # Karena fleksibel, cocok walau beda
        },
        {
            "fullName": "Budi",
            "courseName": "Math",
            "topicSubtopic": "Algebra",
            "learningStyle": "Visual Learning",
            "learningMode": "Online",
            "preferredDate": "2025-07-05",
            "preferredTime": "15:00",
            "flexibleSchedule": "No",  # Ini cocok hanya kalau semua match
        }
    ])

    # 🔍 Hitung skor dan jalankan matching
    score_df = compute_score_matrix(tutors, students)
    assignment = match_tutors(score_df)
    matches, total_score = format_matches_unitest(score_df, assignment)

    # ✅ Validasi hasil
    assert len(matches) == 2

    # Cek pasangan dengan fleksibilitas: Bob – Ali (match karena fleksibel)
    assert ("Bob Wijaya", "Ali", score_df.loc["Bob Wijaya", "Ali"]) in matches

    # Cek pasangan lain
    assert ("Tutor B", "Budi", score_df.loc["Tutor B", "Budi"]) in matches

    # Cek skor total harus sesuai dengan penjumlahan 2 skor tertinggi
    expected_total = int(score_df.loc["Bob Wijaya", "Ali"]) + int(score_df.loc["Tutor B", "Budi"])
    assert total_score == expected_total


def test_matching_1on1_mismatch():
    # 🔹 Data dummy: 1 tutor vs 1 murid, semua atribut berbeda
    tutors = pd.DataFrame([{
        "fullName": "T1",
        "courseName": "Kalkulus",
        "topicSubtopic": "Integral",
        "learningStyle": "Visual",
        "learningMode": "Online",
        "preferredDate": "2025-07-02",
        "preferredTime": "09:00",
        "flexibleSchedule": "No",
    }])

    students = pd.DataFrame([{
        "fullName": "M1",
        "courseName": "Statistika",
        "topicSubtopic": "Distribusi",
        "learningStyle": "Diskusi",
        "learningMode": "Offline near ITS",
        "preferredDate": "2025-07-03",
        "preferredTime": "10:00",
        "flexibleSchedule": "No",
    }])

    # 🔍 Hitung skor dan jalankan matching
    score_df = compute_score_matrix(tutors, students)
    assignment = match_tutors(score_df)
    matches, total_score = format_matches_unitest(score_df, assignment)

    # ✅ Validasi: harus tetap match sekali, tapi skornya nol
    assert len(matches) == 1
    tutor, student, score = matches[0]
    assert (tutor, student, score) == ("T1", "M1", 0)
    assert total_score == 0


def test_matching_1on1_unbalanced_students_more():
    # 🔹 Kasus unbalanced: 2 tutor, 3 murid
    tutors = pd.DataFrame([
        {
            "fullName": "T1",
            "courseName": "CourseA",
            "topicSubtopic": "TopicX",
            "learningStyle": "Visual",
            "learningMode": "Online",
            "preferredDate": "2025-07-01",
            "preferredTime": "09:00",
            "flexibleSchedule": "No",
        },
        {
            "fullName": "T2",
            "courseName": "CourseB",
            "topicSubtopic": "TopicY",
            "learningStyle": "Kinesthetic",
            "learningMode": "Offline",
            "preferredDate": "2025-07-02",
            "preferredTime": "10:00",
            "flexibleSchedule": "No",
        },
    ])

    students = pd.DataFrame([
        {
            "fullName": "S1",
            "courseName": "CourseA",
            "topicSubtopic": "TopicX",
            "learningStyle": "Visual",
            "learningMode": "Online",
            "preferredDate": "2025-07-01",
            "preferredTime": "09:00",
            "flexibleSchedule": "No",
        },
        {
            "fullName": "S2",
            "courseName": "CourseB",
            "topicSubtopic": "TopicY",
            "learningStyle": "Kinesthetic",
            "learningMode": "Offline",
            "preferredDate": "2025-07-02",
            "preferredTime": "10:00",
            "flexibleSchedule": "No",
        },
        {
            "fullName": "S3",   # Murid tambahan tanpa kecocokan
            "courseName": "CourseC",
            "topicSubtopic": "TopicZ",
            "learningStyle": "Discussion",
            "learningMode": "Online",
            "preferredDate": "2025-07-03",
            "preferredTime": "11:00",
            "flexibleSchedule": "No",
        },
    ])

    # 🔍 Hitung skor dan jalankan Hungarian
    score_df = compute_score_matrix(tutors, students)
    assignment = match_tutors(score_df)
    matches, total_score = format_matches_unitest(score_df, assignment)

    # ✅ Validasi
    # Karena hanya 2 tutor, kita harus dapat tepat 2 match
    assert len(matches) == 2

    # Pastikan pasangan optimal untuk setiap tutor
    expected_1 = ("T1", "S1", int(score_df.loc["T1", "S1"]))
    expected_2 = ("T2", "S2", int(score_df.loc["T2", "S2"]))
    assert expected_1 in matches
    assert expected_2 in matches

    # Total skor harus jumlah dari kedua skor tersebut
    assert total_score == expected_1[2] + expected_2[2]


def test_matching_1on1_unbalanced_tutors_more():
    # 🔹 Data dummy: 3 tutor, 2 murid (unbalanced tutors > students)
    tutors = pd.DataFrame([
        {
            "fullName": "T1",
            "courseName": "CourseA",
            "topicSubtopic": "TopicX",
            "learningStyle": "Visual",
            "learningMode": "Online",
            "preferredDate": "2025-07-01",
            "preferredTime": "09:00",
            "flexibleSchedule": "No",
        },
        {
            "fullName": "T2",
            "courseName": "CourseB",
            "topicSubtopic": "TopicY",
            "learningStyle": "Kinesthetic",
            "learningMode": "Offline",
            "preferredDate": "2025-07-02",
            "preferredTime": "10:00",
            "flexibleSchedule": "No",
        },
        {
            # Tutor tanpa kecocokan, seharusnya di-skip oleh format_matches_unitest
            "fullName": "T3",
            "courseName": "CourseC",
            "topicSubtopic": "TopicZ",
            "learningStyle": "Discussion",
            "learningMode": "Online",
            "preferredDate": "2025-07-03",
            "preferredTime": "11:00",
            "flexibleSchedule": "No",
        },
    ])

    students = pd.DataFrame([
        {
            "fullName": "S1",
            "courseName": "CourseA",
            "topicSubtopic": "TopicX",
            "learningStyle": "Visual",
            "learningMode": "Online",
            "preferredDate": "2025-07-01",
            "preferredTime": "09:00",
            "flexibleSchedule": "No",
        },
        {
            "fullName": "S2",
            "courseName": "CourseB",
            "topicSubtopic": "TopicY",
            "learningStyle": "Kinesthetic",
            "learningMode": "Offline",
            "preferredDate": "2025-07-02",
            "preferredTime": "10:00",
            "flexibleSchedule": "No",
        },
    ])

    # 🔍 Hitung skor dan jalankan Hungarian
    score_df = compute_score_matrix(tutors, students)
    assignment = match_tutors(score_df)
    matches, total_score = format_matches_unitest(score_df, assignment)

    # ✅ Validasi: hanya 2 match yang valid, T3 harus di-skip
    assert len(matches) == 2

    # Pastikan tutor T1–S1 dan T2–S2 tercakup
    assert ("T1", "S1", int(score_df.loc["T1", "S1"])) in matches
    assert ("T2", "S2", int(score_df.loc["T2", "S2"])) in matches

    # Total skor harus sesuai jumlah kedua skor tersebut
    expected = int(score_df.loc["T1", "S1"]) + int(score_df.loc["T2", "S2"])
    assert total_score == expected


def test_matching_1on1_cross_topic_optimal():
    # 🔹 Data dummy: 2 tutor dengan same course tapi beda topic,
    #   dan 2 murid dengan swap topic agar only optimal cross-match
    common_kwargs = {
        "learningStyle": "Visual",
        "learningMode": "Online",
        "preferredDate": "2025-07-10",
        "preferredTime": "09:00",
        "flexibleSchedule": "No",
    }
    tutors = pd.DataFrame([
        {
            "fullName": "T1",
            "courseName": "CourseA",
            "topicSubtopic": "TopicX",
            **common_kwargs
        },
        {
            "fullName": "T2",
            "courseName": "CourseA",
            "topicSubtopic": "TopicY",
            **common_kwargs
        }
    ])

    students = pd.DataFrame([
        {
            "fullName": "S1",
            "courseName": "CourseA",
            "topicSubtopic": "TopicY",
            **common_kwargs
        },
        {
            "fullName": "S2",
            "courseName": "CourseA",
            "topicSubtopic": "TopicX",
            **common_kwargs
        }
    ])

    # 🔍 Hitung skor dan jalankan Hungarian
    score_df = compute_score_matrix(tutors, students)
    assignment = match_tutors(score_df)
    matches, total_score = format_matches_unitest(score_df, assignment)

    # ✅ Validasi:
    # Optimal pairing: T1-S2 (TopicX), T2-S1 (TopicY)
    expected_1 = ("T1", "S2", int(score_df.loc["T1", "S2"]))
    expected_2 = ("T2", "S1", int(score_df.loc["T2", "S1"]))

    assert len(matches) == 2
    assert expected_1 in matches
    assert expected_2 in matches

    # Total skor = sum skor kedua pasangan
    assert total_score == expected_1[2] + expected_2[2]


def test_matching_1on1_no_tutors():
    # Kasus: tidak ada tutor, ada murid
    tutors = pd.DataFrame([], columns=[
        "fullName","courseName","topicSubtopic",
        "learningStyle","learningMode",
        "preferredDate","preferredTime","flexibleSchedule"
    ])
    students = pd.DataFrame([{
        "fullName": "M1",
        "courseName": "Physics",
        "topicSubtopic": "Mechanics",
        "learningStyle": "Visual",
        "learningMode": "Online",
        "preferredDate": "2025-07-02",
        "preferredTime": "10:00",
        "flexibleSchedule": "No",
    }])

    score_df = compute_score_matrix(tutors, students)
    assignment = match_tutors(score_df)
    matches, total_score = format_matches_unitest(score_df, assignment)

    # Harus aman: tidak ada pasangan, total skor 0
    assert matches == []
    assert total_score == 0

def test_matching_1on1_no_students():
    # Kasus: tidak ada murid, ada tutor
    tutors = pd.DataFrame([{
        "fullName": "T1",
        "courseName": "Physics",
        "topicSubtopic": "Mechanics",
        "learningStyle": "Visual",
        "learningMode": "Online",
        "preferredDate": "2025-07-02",
        "preferredTime": "10:00",
        "flexibleSchedule": "No",
    }])
    students = pd.DataFrame([], columns=[
        "fullName","courseName","topicSubtopic",
        "learningStyle","learningMode",
        "preferredDate","preferredTime","flexibleSchedule"
    ])

    score_df = compute_score_matrix(tutors, students)
    assignment = match_tutors(score_df)
    matches, total_score = format_matches_unitest(score_df, assignment)

    # Harus aman: tidak ada pasangan, total skor 0
    assert matches == []
    assert total_score == 0


def test_compute_score_matrix_missing_preferredTime():
    # Kasus: students tidak punya kolom preferredTime
    tutors = pd.DataFrame([{
        "fullName": "T1",
        "courseName": "Physics",
        "topicSubtopic": "Mechanics",
        "learningStyle": "Visual",
        "learningMode": "Online",
        "preferredDate": "2025-07-02",
        "preferredTime": "10:00",
        "flexibleSchedule": "No",
    }])
    students = pd.DataFrame([{
        "fullName": "S1",
        "courseName": "Physics",
        "topicSubtopic": "Mechanics",
        "learningStyle": "Visual",
        "learningMode": "Online",
        "preferredDate": "2025-07-02",
        # "preferredTime" kolom sengaja dihilangkan
        "flexibleSchedule": "No",
    }])

    # Harus tetap jalan tanpa error
    score_df = compute_score_matrix(tutors, students)
    # Hasil harus DataFrame 1×1
    assert isinstance(score_df, pd.DataFrame)
    assert score_df.shape == (1, 1)

def test_compute_score_matrix_missing_learningMode():
    # Kasus: tutors tidak punya kolom learningMode
    tutors = pd.DataFrame([{
        "fullName": "T1",
        "courseName": "Math",
        "topicSubtopic": "Algebra",
        "learningStyle": "Kinesthetic",
        "preferredDate": "2025-07-03",
        "preferredTime": "09:00",
        "flexibleSchedule": "Yes",
        # "learningMode" kolom sengaja dihilangkan
    }])
    students = pd.DataFrame([{
        "fullName": "S1",
        "courseName": "Math",
        "topicSubtopic": "Algebra",
        "learningStyle": "Kinesthetic",
        "learningMode": "Offline",
        "preferredDate": "2025-07-03",
        "preferredTime": "09:00",
        "flexibleSchedule": "Yes",
    }])

    # Harus tetap jalan tanpa error
    score_df = compute_score_matrix(tutors, students)
    # Hasil harus DataFrame 1×1
    assert isinstance(score_df, pd.DataFrame)
    assert score_df.shape == (1, 1)
