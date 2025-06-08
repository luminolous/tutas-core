from collections import defaultdict

def make_subgroups(df, partition, max_size):
    # df: DataFrame valid dengan kolom Nama, Status, No WA
    df = df.copy()
    df["Circle ID"] = df["Nama"].map(partition)

    circle_groups = df.groupby("Circle ID")
    circle_result = []
    new_circle_id = 0

    for cid, group in circle_groups:
        # Pisahkan tutor & murid
        tutors   = group[group["Status"]=="Tutor"].to_dict("records")
        students = group[group["Status"]=="Murid"].to_dict("records")

        # 1) Untuk setiap tutor, bikin sub-grup: [tutor + up to 4 murid]
        for t in tutors:
            assigned_students = students[:4]     # ambil 4 murid pertama
            students = students[4:]             # sisa murid
            sub = [t] + assigned_students
            circle_result.append((new_circle_id, sub))
            new_circle_id += 1

        # 2) Sisa murid → kelompok murid saja, 4 orang per sub-grup
        while len(students) > 0:
            sub_students = students[:4]
            students = students[4:]
            circle_result.append((new_circle_id, sub_students))
            new_circle_id += 1

        # 3) (Opsional) Jika ada tutor “tersisa” (jarang), masukkan sendiri
        #    — tapi biasanya tutors habis di langkah 1
        for t in tutors[len(tutors):]:
            circle_result.append((new_circle_id, [t]))
            new_circle_id += 1

    # Setelah ini, circle_result berisi list of (CircleID, list_of_rows)
    # Lanjutkan STEP 5: simpan ke CSV seperti biasa
    output_rows = []
    for cid, rows in circle_result:
        for row in rows:
            output_rows.append({
                "Nama"       : row["Nama"],
                "Circle ID"  : cid,
                "Tutor/Murid": row["Status"],
                "No WA"      : row["No WA"]
            })

    return output_rows
