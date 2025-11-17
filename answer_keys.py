from typing import List, Dict

from questions import (
    ROLES,
    DS_QUESTIONS,
    DE_QUESTIONS,
    WEB_QUESTIONS,
    BE_QUESTIONS,
    FE_QUESTIONS,
    ML_QUESTIONS,
    MOB_QUESTIONS,
)

# Biar lebih eksplisit, kita import list pertanyaan dari masing-masing role:
ROLE_QUESTION_TEXTS: Dict[str, List[str]] = {
    "data scientist": DS_QUESTIONS,
    "data engineer": DE_QUESTIONS,
    "web developer": WEB_QUESTIONS,
    "backend developer": BE_QUESTIONS,
    "frontend developer": FE_QUESTIONS,
    "machine learning engineer": ML_QUESTIONS,
    "mobile developer": MOB_QUESTIONS,
}

# ====== JAWABAN IDEAL PER ROLE & PER PERTANYAAN ======
# NOTE:
# - Ini contoh singkat. Kamu bisa ganti / perpanjang jadi lebih detail.
# - Panjang list di setiap role harus sama dengan jumlah pertanyaan (7).

DATA_SCIENTIST_ANSWERS: List[List[str]] = [
    [
        "Saya pernah mengerjakan proyek analisis churn pelanggan. Saya mulai dari pengumpulan data dari database transaksi, melakukan pembersihan dan exploratory data analysis, lalu membangun model klasifikasi seperti Random Forest dan XGBoost untuk memprediksi pelanggan yang berpotensi churn, serta mengevaluasi dengan metrik AUC dan F1 score.",
    ],
    [
        "Saat membangun model machine learning, biasanya saya mulai dari understanding problem, mengumpulkan dan membersihkan data, melakukan feature engineering, memilih beberapa algoritma kandidat, melakukan training dan hyperparameter tuning menggunakan cross validation, lalu memilih model terbaik dan mengevaluasi dengan metrik yang sesuai seperti accuracy, F1, atau RMSE.",
    ],
    [
        "Untuk missing value, saya biasa menggunakan imputasi seperti mean atau median untuk fitur numerik, dan modus untuk fitur kategorikal, atau bahkan model based imputation jika kasusnya kompleks. Untuk outlier, saya melakukan deteksi menggunakan IQR atau z-score, lalu memutuskan apakah outlier tersebut hasil kesalahan atau justru informasi penting.",
    ],
    [
        "Saya memilih fitur dengan menggabungkan domain knowledge dan metode statistik. Saya melihat korelasi antar fitur, menggunakan teknik seperti mutual information atau feature importance dari model tree based. Selain itu saya juga mencoba teknik regularization seperti L1 untuk melakukan feature selection.",
    ],
    [
        "Proyek yang paling berkesan adalah membangun sistem rekomendasi produk. Saya menggabungkan collaborative filtering dengan content based filtering, melakukan evaluasi offline menggunakan precision@k, dan akhirnya menguji performa secara online melalui A/B testing sehingga terbukti meningkatkan konversi penjualan.",
    ],
    [
        "Untuk menjelaskan model yang kompleks, saya menggunakan visualisasi sederhana dan analogi yang mudah dipahami. Selain itu saya memakai teknik model interpretability seperti SHAP atau feature importance untuk menunjukkan fitur mana yang paling berpengaruh terhadap prediksi, dan menjelaskan implikasinya terhadap bisnis.",
    ],
    [
        "Supervised learning digunakan ketika kita memiliki label dan ingin memprediksi output tertentu seperti klasifikasi atau regresi. Sedangkan unsupervised learning digunakan ketika tidak ada label dan kita ingin menemukan struktur data, misalnya clustering dengan KMeans atau dimensionality reduction dengan PCA.",
    ],
]

DATA_ENGINEER_ANSWERS: List[List[str]] = [
    [
        "Saya pernah membangun data pipeline harian menggunakan Airflow yang mengekstrak data dari beberapa sumber, melakukan transformasi dengan Spark, lalu memuatnya ke data warehouse BigQuery untuk kebutuhan analisis dan dashboarding.",
    ],
    [
        "Untuk proses ETL saya sering menggunakan kombinasi Airflow, Python, dan SQL. Di sisi penyimpanan, saya biasa bekerja dengan PostgreSQL, BigQuery, dan kadang-kadang NoSQL seperti MongoDB tergantung kebutuhan.",
    ],
    [
        "Dalam merancang data warehouse, saya menggunakan pendekatan star schema atau snowflake schema dengan memisahkan fact table dan dimension table agar query analitik menjadi lebih cepat dan mudah dipahami.",
    ],
    [
        "Saya memasang monitoring di setiap task pipeline, mencatat log error dengan jelas, dan menambahkan notifikasi apabila ada job yang gagal. Selain itu saya mendesain pipeline supaya idempotent sehingga bila terjadi kegagalan bisa di rerun tanpa merusak data.",
    ],
    [
        "Saya pernah mengoptimasi query SQL dengan menambahkan indeks pada kolom yang sering difilter, meminimalkan penggunaan subquery kompleks, dan memanfaatkan partitioning serta clustering pada tabel besar.",
    ],
    [
        "Untuk menjamin kualitas data, saya menambahkan data validation di pipeline menggunakan aturan sederhana seperti cek range nilai, cek null, dan konsistensi referensial antar tabel. Jika ada anomali, pipeline akan menandai atau menghentikan proses.",
    ],
    [
        "Batch processing cocok digunakan untuk job terjadwal seperti laporan harian, sedangkan stream processing digunakan untuk memproses data real time misalnya log clickstream atau event aplikasi yang memerlukan respon cepat.",
    ],
]

WEB_DEVELOPER_ANSWERS: List[List[str]] = [
    [
        "Saya pernah membangun aplikasi web full stack menggunakan React di frontend dan Node.js Express di backend dengan database PostgreSQL. Aplikasinya memiliki fitur autentikasi, manajemen pengguna, dan dashboard analitik.",
    ],
    [
        "Saya sering menggunakan HTML, CSS, JavaScript, React untuk frontend dan Node.js atau Laravel untuk backend. Untuk styling saya menggunakan Tailwind CSS atau Bootstrap.",
    ],
    [
        "Untuk membuat layout responsif, saya menggunakan flexbox dan grid, media query, serta mengecek tampilan di berbagai ukuran layar. Saya juga memanfaatkan komponen yang sudah responsif dari framework CSS.",
    ],
    [
        "RESTful API adalah cara mendesain endpoint HTTP yang merepresentasikan resource. Saya biasa membuat endpoint dengan metode GET, POST, PUT, DELETE yang mengembalikan JSON sehingga dapat diakses oleh frontend atau klien lain.",
    ],
    [
        "Salah satu fitur kompleks yang pernah saya buat adalah sistem pencarian dengan filter dinamis dan pagination di sisi server untuk menangani data dalam jumlah besar.",
    ],
    [
        "Untuk keamanan, saya menerapkan autentikasi JWT, validasi input, proteksi CSRF, menggunakan HTTPS, serta menghindari SQL injection dengan prepared statement atau ORM.",
    ],
    [
        "Saya bekerja dekat dengan tim frontend dan backend dengan menyepakati kontrak API terlebih dahulu, membuat dokumentasi endpoint, dan melakukan testing bersama menggunakan Postman atau Swagger.",
    ],
]

BACKEND_DEVELOPER_ANSWERS: List[List[str]] = [
    [
        "Saya pernah mengembangkan REST API menggunakan Node.js dan Express yang melayani aplikasi mobile dan web, dengan autentikasi JWT dan integrasi ke payment gateway.",
    ],
    [
        "Saya paling sering menggunakan Node.js dengan Express atau NestJS, dan kadang-kadang Python dengan Flask atau Django tergantung kebutuhan proyek.",
    ],
    [
        "Saya mulai dari menganalisis kebutuhan fitur, lalu memetakan entitas menjadi tabel dengan relasi yang jelas. Setelah itu saya mendesain skema database normalized namun tetap mempertimbangkan performa query.",
    ],
    [
        "Untuk autentikasi dan otorisasi, saya menggunakan JWT atau session based auth, menambahkan role dan permission, serta memastikan password disimpan dengan hashing seperti bcrypt.",
    ],
    [
        "Saya pernah mengoptimasi API dengan menambah indeks database, mengurangi query berulang melalui caching, dan memindahkan operasi berat ke background job.",
    ],
    [
        "Sebelum rilis, saya menulis unit test dan integration test untuk endpoint utama, serta menggunakan environment staging untuk mencoba alur bisnis end-to-end.",
    ],
    [
        "Untuk desain yang scalable, saya memecah layanan menjadi beberapa service yang lebih kecil, menggunakan message queue bila perlu, dan memastikan tidak ada single point of failure.",
    ],
]

FRONTEND_DEVELOPER_ANSWERS: List[List[str]] = [
    [
        "Saya pernah mengerjakan dashboard interaktif menggunakan React dan Chart.js, dengan fitur filtering real time dan tampilan yang responsif di desktop maupun mobile.",
    ],
    [
        "Framework yang paling sering saya gunakan adalah React karena ekosistemnya luas dan fleksibel. Saya juga familiar dengan Vue untuk proyek tertentu.",
    ],
    [
        "Untuk mengelola state kompleks, saya menggunakan Redux atau React Context, dan memisahkan state global dengan state lokal komponen agar lebih terstruktur.",
    ],
    [
        "Saya mengoptimasi performa dengan meminimalkan re-render menggunakan memoization, lazy loading, serta memecah bundle menjadi chunk yang lebih kecil.",
    ],
    [
        "Saya menyesuaikan desain dengan design system yang disediakan tim UI/UX, menggunakan komponen reusable, dan menjaga konsistensi warna, tipografi, dan spacing.",
    ],
    [
        "Saya biasa menulis unit test untuk komponen penting menggunakan Jest dan React Testing Library, terutama untuk logic yang rumit.",
    ],
    [
        "Kolaborasi dengan designer dan backend dilakukan melalui handoff di Figma, pembuatan kontrak API yang jelas, dan komunikasi intensif saat ada perubahan requirement.",
    ],
]

ML_ENGINEER_ANSWERS: List[List[str]] = [
    [
        "Saya pernah melakukan deployment model machine learning ke produksi menggunakan Docker dan Kubernetes, dengan model yang di-expose sebagai REST API dan diakses oleh microservice lain.",
    ],
    [
        "Untuk training saya menggunakan PyTorch atau TensorFlow, sedangkan untuk serving saya menggunakan FastAPI atau TorchServe tergantung jenis modelnya.",
    ],
    [
        "Saya memonitor performa model dengan mencatat prediksi dan label aktual, lalu menghitung metrik berkala. Jika performa turun, saya analisis penyebab dan melakukan retraining.",
    ],
    [
        "Concept drift saya tangani dengan memantau distribusi fitur dan label, serta membuat jadwal retraining berkala apabila ditemukan pergeseran distribusi yang signifikan.",
    ],
    [
        "Saya pernah membangun pipeline ML end-to-end mulai dari data ingestion, feature store, training, evaluasi, hingga deployment otomatis dengan CI/CD.",
    ],
    [
        "Saya menggunakan tool seperti MLflow atau DVC untuk menyimpan eksperimen model, parameter, dan metrik sehingga mudah direproduksi dan dibandingkan.",
    ],
    [
        "Tantangan terbesar adalah sinkronisasi antara tim data dan engineering. Saya mengatasinya dengan menyusun pipeline yang jelas, dokumentasi yang baik, dan automasi proses deployment.",
    ],
]

MOBILE_DEVELOPER_ANSWERS: List[List[str]] = [
    [
        "Saya pernah membuat aplikasi mobile untuk pemesanan makanan menggunakan Flutter, dengan fitur login, keranjang belanja, dan notifikasi pesanan.",
    ],
    [
        "Saya sering menggunakan Flutter karena bisa menyusun aplikasi untuk Android dan iOS sekaligus, dan saya juga pernah menggunakan native Android dengan Kotlin.",
    ],
    [
        "Saya mengoptimasi performa dengan menghindari rebuild widget yang tidak perlu, menggunakan lazy list, dan meminimalkan operasi berat di main thread.",
    ],
    [
        "Untuk penyimpanan lokal, saya menggunakan SQLite atau Hive tergantung kompleksitas data, dan SharedPreferences untuk konfigurasi sederhana.",
    ],
    [
        "Salah satu fitur kompleks yang saya buat adalah integrasi map dan tracking lokasi real time untuk kurir pengiriman.",
    ],
    [
        "Saya mengelola proses release dengan membuat keystore, mengatur versioning, dan mengikuti prosedur upload aplikasi ke Play Store dan App Store.",
    ],
    [
        "Saya mengumpulkan feedback user melalui rating di store dan in-app feedback, lalu memprioritaskan perbaikan bug dan penambahan fitur yang paling banyak diminta.",
    ],
]

ROLE_ANSWER_MAP: Dict[str, List[List[str]]] = {
    "data scientist": DATA_SCIENTIST_ANSWERS,
    "data engineer": DATA_ENGINEER_ANSWERS,
    "web developer": WEB_DEVELOPER_ANSWERS,
    "backend developer": BACKEND_DEVELOPER_ANSWERS,
    "frontend developer": FRONTEND_DEVELOPER_ANSWERS,
    "machine learning engineer": ML_ENGINEER_ANSWERS,
    "mobile developer": MOBILE_DEVELOPER_ANSWERS,
}

DEFAULT_ROLE_KEY = "data scientist"


def get_ideal_answers(role_name: str, question_index: int) -> List[str]:
    """
    Ambil list jawaban ideal untuk role & index pertanyaan tertentu.
    """
    if not role_name:
        role_key = DEFAULT_ROLE_KEY
    else:
        role_key = role_name.strip().lower()

    answers_per_question = ROLE_ANSWER_MAP.get(role_key, ROLE_ANSWER_MAP[DEFAULT_ROLE_KEY])

    if question_index < 0 or question_index >= len(answers_per_question):
        question_index = 0

    return answers_per_question[question_index]
