import re
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# ====== STEMMER BAHASA INDONESIA ======
_factory = StemmerFactory()
_stemmer = _factory.create_stemmer()

# ====== STOPWORDS SEDERHANA (bisa kamu perluas sendiri) ======
INDO_STOPWORDS = {
    "dan", "yang", "di", "ke", "dari", "pada", "untuk", "dengan",
    "ini", "itu", "saya", "saya", "kami", "kita", "anda",
    "atau", "karena", "jadi", "sebagai", "jika", "bila", "agar",
    "adalah", "ialah", "dalam", "tidak", "ya", "tidak", "juga",
    "sebuah", "suatu", "para", "oleh", "serta", "saat", "ketika",
    "lebih", "kurang", "akan", "telah", "sudah", "masih",
}


def preprocess(text: str) -> str:
    """
    Preprocessing sederhana untuk teks bahasa Indonesia:
    - lowercase
    - hapus karakter non-huruf
    - tokenisasi
    - stopword removal
    - stemming dengan Sastrawi
    """
    if not text:
        return ""

    # lowercase
    text = text.lower()

    # hilangkan karakter non huruf
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # tokenisasi sederhana
    tokens = text.split()

    # buang stopword + kata sangat pendek
    filtered = []
    for tok in tokens:
        if tok in INDO_STOPWORDS:
            continue
        if len(tok) <= 2:
            continue
        # stemming
        stemmed = _stemmer.stem(tok)
        filtered.append(stemmed)

    return " ".join(filtered)


def tfidf_cosine_score(user_answer: str, ideal_answers: List[str]) -> float:
    """
    Hitung cosine similarity antara jawaban user dan 1..n jawaban ideal.
    Return nilai antara 0 - 1 (maksimum similarity terhadap ideal answers).
    """
    if not user_answer or not ideal_answers:
        return 0.0

    # Preprocess semua teks
    processed_user = preprocess(user_answer)
    processed_ideals = [preprocess(ans) for ans in ideal_answers]

    corpus = [processed_user] + processed_ideals

    # TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # vektor user = index 0, ideal = 1..N
    user_vec = tfidf_matrix[0:1]
    ideal_vecs = tfidf_matrix[1:]

    sim = cosine_similarity(user_vec, ideal_vecs)  # shape (1, n)
    max_sim = float(np.max(sim))  # ambil similarity tertinggi

    return max_sim


def similarity_to_score(similarity: float) -> int:
    """
    Konversi nilai cosine similarity (0-1) menjadi skor 0-100.
    Di sini kita pakai skala linear + sedikit offset.
    """
    # jaga range
    if similarity < 0:
        similarity = 0.0
    if similarity > 1:
        similarity = 1.0

    # misal: minimal 40, maksimal 95
    min_score = 40
    max_score = 95

    score = min_score + similarity * (max_score - min_score)
    return int(round(score))
