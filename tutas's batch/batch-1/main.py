import gspread
import networkx as nx
from oauth2client.service_account import ServiceAccountCredentials
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Ganti dengan token yang kamu dapat dari Notion
auth_notion = os.getenv("AUTH_NOTION")
notion = Client(auth=auth_notion)
DATABASE_ID = os.getenv("DATABASE_NOTION_ID")

# Query isi database
response = notion.databases.query(database_id=DATABASE_ID)

# 🔐 Autentikasi Google Sheets (tidak diubah)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("googleAuth/sapient-zodiac-456411-n7-92649cf546be.json", scope)
client = gspread.authorize(creds)

# 📄 Ambil data dari spreadsheet
sheet = client.open("spreadsheet-match").sheet1
data = sheet.get_all_values()

students = []
teachers = []

header = data[0]

for i, row in enumerate(data[1:], start=1):
    # 🧑‍🎓 Jika murid (kolom bantuan diisi)
    if row[6].strip() != "" and row[6].strip() != "Mata kuliah lain (tuliskan di catatan)":
        subjects = [s.strip().lower() for s in row[6].split(',')]
        for j, subject in enumerate(subjects):
            entry = {
                "id": f"M{i}_{j}",
                "name": row[1],
                "nrp": row[2],
                "jurusan": row[3],
                "wa": row[5],
                "subject": subject,
                "schedule": row[7].strip(),
                # "flex": row[8].strip().lower(),
                "role": "student"
            }
            students.append(entry)

    # 🧑‍🏫 Jika tutor (kolom ajar diisi)
    if row[9].strip() != "" and row[9].strip() != "Mata kuliah lain (tuliskan di catatan)":
        subjects = [s.strip().lower() for s in row[9].split(',')]
        for j, subject in enumerate(subjects):
            entry = {
                "id": f"T{i}_{j}",
                "name": row[1],
                "nrp": row[2],
                "jurusan": row[3],
                "wa": row[5],
                "subject": subject,
                "schedule": row[12].strip(),
                # "flex": row[13].strip().lower(),
                "role": "teacher"
            }
            teachers.append(entry)

# 📋 Tampilkan semua murid
print("🧑‍🎓 Daftar Murid:")
for s in students:
    print(f"- {s['name']} | NRP: {s['nrp']} | Jurusan: {s['jurusan']} | Mata Kuliah: {s['subject']}")

# 📋 Tampilkan semua tutor
print("\n🧑‍🏫 Daftar Tutor:")
for t in teachers:
    print(f"- {t['name']} | NRP: {t['nrp']} | Jurusan: {t['jurusan']} | Mata Kuliah: {t['subject']}")

# 🔀 Buat graf bipartit
G = nx.Graph()

for s in students:
    G.add_node(s['id'], bipartite=0, data=s)

for t in teachers:
    G.add_node(t['id'], bipartite=1, data=t)

# 🔗 Tambahkan edge berdasarkan subject dan fleksibilitas
for s in students:
    for t in teachers:
        if s['subject'] == t['subject']:
            if s['nrp'] == t['nrp']:
                continue  # ❌ Skip jika NRP sama (orang yang sama)
            else:
                G.add_edge(s['id'], t['id'], weight=1)

            # Matching bergantung fleksibilitas
            # if s['flex'] == "tidak" and t['flex'] == "tidak, saya hanya bisa di jadwal yang saya isi":
            #     if s['schedule'] == t['schedule']:
            #         G.add_edge(s['id'], t['id'], weight=2)  # Match full
            # else:
            #     G.add_edge(s['id'], t['id'], weight=1)  # Subject match saja

# ✅ Matching maksimal berbobot
matching = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True)

# 🖨️ Tampilkan hasil pencocokan
print("\n🔗 Matching Result:")
for u, v in matching:
    node_u = G.nodes[u]
    node_v = G.nodes[v]

    student = node_u['data'] if node_u['data']['role'] == "student" else node_v['data']
    teacher = node_v['data'] if node_v['data']['role'] == "teacher" else node_u['data']

    print(f"👨‍🎓 {student['name']} belajar dari 🧑‍🏫 {teacher['name']} "
          f"(Mata kuliah: {student['subject']}, Jadwal: {student['schedule']})")

    message = (f"Halo {student['name']}! 👋"
               f"\nSaya dari tim Tutas – Tutor Sebaya Mahasiswa ITS."
               f"\n"
               f"\nBerikut hasil pencocokan kamu dari Batch 1:"
               f"\n"
               f"\n📘 Mata kuliah: {student['subject']}"
               f"\n👤 Tutor kamu: {teacher['name']}"  
               f"\n📞 Kontak tutor: {teacher['wa']}"
               f"\n"
               f"\nSilakan langsung hubungi tutor kamu untuk diskusi jadwal belajar yang cocok."
               f"\nBelajar bisa dilakukan fleksibel sesuai kesepakatan kalian."
               f"\n"
               f"\nKalau ada kendala atau feedback, bisa balas langsung ke nomor ini ya."
               f"\nTerima kasih sudah jadi bagian dari Tutas 🙌")
    print(f"📩 Notifikasi: {message}\n")


    # Tambahkan data
    new_page = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Nama Murid": {
                "title": [
                    {"text": {"content": student['name']}}
                ]
            },
            "Nomer WA Murid": {
                "rich_text": [
                    {"text": {"content": student['wa']}}
                ]
            },
            "Tutor": {
                "rich_text": [
                    {"text": {"content": teacher['name']}}
                ]
            },
            "Nomer WA Tutor": {
                "rich_text": [
                    {"text": {"content": teacher['wa']}}
                ]
            },
            "Mata Kuliah": {
                "rich_text": [
                    {"text": {"content": student['subject']}}
                ]
            },
            "Status": {
                "select": {
                    "name": "Belum"
                }
            },
            "Template Chat": {
                "rich_text": [
                    {"text": {"content": message}}
                ]
            }
        }
    )

print("Data berhasil ditambahkan ke Notion 🎉")