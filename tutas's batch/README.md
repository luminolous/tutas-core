# 📦 `tutas's batch/`

Repositori ini berisi kode operasional sistem **Tutas** selama pelaksanaan **Batch 1 dan Batch 2**.  
**Bukan** merupakan kode utama dari **Final Project Teori Graf**, melainkan kumpulan skrip eksperimen dan otomasi teknis internal program.

---

## 📁 `batch-1/`

Folder ini menyimpan skrip-skrip operasional Tutas Batch 1, antara lain:

- `generate_qrcode.py`  
  Membuat QR Code untuk absensi tutor selama sesi berlangsung.

- `test_gspread.py`  
  Uji koneksi dan pembacaan data dari Google Spreadsheet API.

- `main.py`  
  Skrip gabungan dari beberapa modul untuk keperluan testing internal.

- `testNotion.py`  
  Uji kirim data otomatis ke Notion API untuk dashboard tracking.

- `test.ipynb`  
  Notebook interaktif untuk eksperimen fitur dan data dummy.

---

## 📁 `batch-2/`

Folder ini menyimpan kode eksperimen dan simulasi untuk Tutas Batch 2, khususnya:

- `hungarian.py`  
  Implementasi dan pengujian algoritma Hungarian untuk matching 1-on-1.

- `manual_louvain.py`  
  Matching Circle berbasis Louvain modularity dan grouping komunitas belajar.

- `data_dummy.py`  
  Generator data simulasi murid-tutor.

- `test_matriks.py`  
  Uji coba pembuatan matriks skor antara murid dan tutor berdasarkan preferensi.

- `tutascircle/`  
  (Submodul untuk clustering dan similarity graph – sedang dalam pengembangan.)

---

## ⚠️ Catatan Penting

> **Folder ini bukan bagian dari kode Final Project mata kuliah Teori Graf.**  
> Struktur di dalamnya digunakan sebagai dokumentasi teknis dan eksperimen sistem **Tutas** selama batch berjalan.

---