from collections import defaultdict

def make_subgroups(df, partition, max_size):
    df = df.copy()
    df["Circle ID"] = df["Nama"].map(partition)

    circle_groups = df.groupby("Circle ID")
    circle_result = []
    new_circle_id = 0

    for cid, group in circle_groups:
        # Pisahkan tutor & murid
        tutors = group[group["Status"].str.lower() == "tutor"].to_dict("records")
        students = group[group["Status"].str.lower().isin(["murid","student"])].to_dict("records")

        for t in tutors:
            assigned_students = students[:4]     # ambil 4 murid pertama
            students = students[4:]             # sisa murid
            sub = [t] + assigned_students
            circle_result.append((new_circle_id, sub))
            new_circle_id += 1

        while len(students) > 0:
            sub_students = students[:4]
            students = students[4:]
            circle_result.append((new_circle_id, sub_students))
            new_circle_id += 1

        for t in tutors[len(tutors):]:
            circle_result.append((new_circle_id, [t]))
            new_circle_id += 1

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
