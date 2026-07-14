# JobifyAI

JobifyAI adalah aplikasi web simulasi wawancara kerja berbasis Flask. Pengguna memilih bidang pekerjaan, menjawab pertanyaan interview melalui teks atau suara, lalu memperoleh skor relevansi dan umpan balik otomatis menggunakan text mining Bahasa Indonesia.

## Fitur

- Pilihan role: Data Scientist, Data Engineer, Web Developer, Backend Developer, Frontend Developer, Machine Learning Engineer, dan Mobile Developer.
- Pertanyaan dan jawaban referensi yang berbeda untuk setiap role.
- Jawaban melalui teks atau suara dengan Web Speech Recognition browser.
- Penilaian otomatis memakai TF-IDF dan cosine similarity.
- Feedback per pertanyaan berdasarkan relevansi dan panjang jawaban.
- Ringkasan nilai rata-rata saat interview selesai.
- Riwayat interview dengan pagination dan ekspor ke file Excel.

## Alur Penilaian

```text
Login + pilih role
  -> ambil daftar pertanyaan
  -> kirim jawaban ke /api/evaluate
  -> preprocessing teks
  -> TF-IDF + cosine similarity dengan jawaban referensi
  -> skor, feedback, dan pertanyaan berikutnya
  -> rata-rata skor + simpan riwayat sesi
```

Preprocessing di `text_scoring.py` mencakup lowercase, penghapusan karakter non-huruf, tokenisasi, stopword removal, dan stemming menggunakan Sastrawi. Similarity tertinggi terhadap jawaban ideal kemudian dikonversi menjadi skor 40-95.

## Teknologi

- Python 3
- Flask 3
- scikit-learn dan NumPy untuk TF-IDF serta cosine similarity
- Sastrawi untuk stemming Bahasa Indonesia
- Pandas dan openpyxl untuk ekspor Excel
- HTML, CSS, JavaScript, dan Web Speech API

## Instalasi dan Menjalankan Aplikasi

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Buka `http://localhost:7070` di browser. Untuk mode suara, gunakan browser yang mendukung Web Speech Recognition dan izinkan akses mikrofon.

## Struktur Proyek

```text
app.py                 # Route Flask, sesi, dashboard, history, dan API evaluasi
text_scoring.py        # Preprocessing, TF-IDF, cosine similarity, dan konversi skor
answer_keys.py         # Jawaban ideal tiap pertanyaan
questions/             # Bank pertanyaan berdasarkan role
templates/             # Halaman Jinja HTML
static/css/main.css    # Styling aplikasi
static/js/interview.js # Interaksi interview dan speech recognition
requirements.txt       # Dependensi Python
```

## Catatan Pengembangan

Hasil interview saat ini disimpan di memori melalui `SESSION_RESULTS`; data akan hilang saat server dimulai ulang dan belum dipisahkan antar pengguna. Untuk penggunaan produksi, gunakan database, pindahkan `SECRET_KEY` ke environment variable, dan jalankan Flask dengan konfigurasi produksi.
