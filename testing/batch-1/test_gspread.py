import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Gunakan scope untuk Google Sheets dan Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credential JSON dari service account
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Membuat spreadsheet baru
spreadsheet = client.create("Data Belajar Mahasiswa")

# Share spreadsheet ke akun Google agar bisa diakses dari browser
spreadsheet.share('your-email@gmail.com', perm_type='user', role='writer')

# Membuka worksheet pertama
sheet = spreadsheet.sheet1
sheet.update_title("Matchmaking Belajar")

# Header
sheet.append_row(["Demand", "Supply"])

# Contoh data demand & supply
data = [
    ["Rina Lestari - Kalkulus - Senin 10:00", "Andi Pratama - Kalkulus - Senin 10:00"],
    ["Dimas Putra - Fisika - Selasa 13:00", "Sari Dewi - Fisika - Selasa 13:00"],
    ["Tiara Anjani - Algoritma - Rabu 14:00", "Budi Santoso - Algoritma - Rabu 14:00"]
]

# Menambahkan data ke sheet
for row in data:
    sheet.append_row(row)

# Membaca kembali data
rows = sheet.get_all_values()
for r in rows:
    print(r)