# Re-import library setelah reset
import pandas as pd
import random

# Buat dummy data user (15-20 user)
names = [f"user{str(i).zfill(2)}" for i in range(1, 21)]
no_wa = [f"08{random.randint(1000000000, 9999999999)}" for _ in names]
statuses = ["Tutor"] * 4 + ["Murid"] * 16
random.shuffle(statuses)

topik_list = ["Integral Parsial", "Pointer di C++", "Distribusi Binomial"]
waktu_list = ["Senin malam", "Selasa sore", "Jumat pagi", "Rabu malam"]
mode_list = ["Online – Video Call", "Offline (sekitar ITS)", "Chat Diskusi (WA/Telegram)"]
gaya_list = ["Visual & konsep", "Diskusi dua arah", "Langsung latihan soal"]

# Buat DataFrame dummy
data = {
    "Nama": names,
    "No WA": no_wa,
    "Status": statuses,
    "Topik": [random.choice(topik_list) for _ in names],
    "Waktu": [random.choice(waktu_list) for _ in names],
    "Mode": [random.choice(mode_list) for _ in names],
    "Gaya": [random.choice(gaya_list) for _ in names],
}

df_dummy = pd.DataFrame(data)

# Simpan sebagai dummy input CSV
dummy_path = "data/dummy_circle_input.csv"
df_dummy.to_csv(dummy_path, index=False)

dummy_path
