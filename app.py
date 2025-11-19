import os
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
)

from questions import get_questions_for_role, ROLES
from answer_keys import get_ideal_answers
from text_scoring import tfidf_cosine_score, similarity_to_score

app = Flask(__name__)

# ========== CONFIG ==========
app.config["SECRET_KEY"] = "ganti_ini_dengan_secret_keymu"
BASE_DIR = os.path.dirname(__file__)

# ========== PENYIMPAN HASIL SESI (IN-MEMORY) ==========
# Struktur: {"role": "...", "average_score": 87.5, "user_name": "...", "timestamp": "..."}
SESSION_RESULTS = []


def compute_dashboard_stats():
    """Hitung statistik untuk dashboard berdasarkan SESSION_RESULTS."""
    scores = [s["average_score"] for s in SESSION_RESULTS]
    if scores:
        total_sessions = len(scores)
        avg_score = round(sum(scores) / len(scores), 1)
        best_score = max(scores)
        # untuk sederhana, anggap streak_days = total_sessions
        streak_days = total_sessions
    else:
        total_sessions = 0
        avg_score = 0.0
        best_score = 0
        streak_days = 0

    return {
        "total_sessions": total_sessions,
        "avg_score": avg_score,
        "best_score": best_score,
        "streak_days": streak_days,
        "progress_scores": scores,
    }


# ========== CONTEXT PROCESSOR ==========
@app.context_processor
def inject_user():
    return dict(
        user_name=session.get("user_name"),
        user_role=session.get("user_role"),
    )


# ========== LOGIN ==========
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "").strip()

        if not name or not role:
            error = "Nama dan Role wajib diisi."
        else:
            # simpan ke session
            session["user_name"] = name
            session["user_role"] = role

            # reset skor wawancara kalau ada sesi lama
            session.pop("scores", None)
            session.pop("total_questions", None)

            return redirect(url_for("dashboard"))

    return render_template("login.html", roles=ROLES, error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ========== DASHBOARD ==========
@app.route("/")
def dashboard():
    if "user_name" not in session or "user_role" not in session:
        return redirect(url_for("login"))

    stats = compute_dashboard_stats()

    return render_template(
        "dashboard.html",
        stats=stats,
        scores=stats["progress_scores"],
        title="Dashboard - Jobify.ai",
    )


# ========== RIWAYAT WAWANCARA ==========
@app.route("/history")
def history():
    if "user_name" not in session or "user_role" not in session:
        return redirect(url_for("login"))

    # kita tampilkan sesi terbaru di atas (dibalik)
    sessions = list(reversed(SESSION_RESULTS))

    return render_template(
        "history.html",
        sessions=sessions,
        title="Riwayat Wawancara - Jobify.ai",
    )


# ========== INTERVIEW ==========
@app.route("/interview")
def interview():
    if "user_name" not in session or "user_role" not in session:
        return redirect(url_for("login"))

    role = session.get("user_role", "")
    question_list = get_questions_for_role(role)
    if not question_list:
        question_list = get_questions_for_role("default")

    total_questions = len(question_list)
    session["total_questions"] = total_questions
    session["scores"] = []  # reset skor setiap mulai sesi baru

    first_question = question_list[0]

    return render_template(
        "interview.html",
        question=first_question,
        total_questions=total_questions,
        title="Wawancara - Jobify.ai",
    )


# ========== API EVALUATE (TF-IDF + COSINE + AVERAGE + HISTORY) ==========
@app.route("/api/evaluate", methods=["POST"])
def evaluate_answer():
    if "user_role" not in session:
        return jsonify(
            {"success": False, "message": "Session sudah habis, silakan login ulang."}
        )

    data = request.get_json()
    answer_text = data.get("answer", "").strip()
    question_index = int(data.get("question_index", 0))

    if not answer_text:
        return jsonify({"success": False, "message": "Jawaban masih kosong."})

    role = session.get("user_role", "")
    user_name = session.get("user_name", "Unknown")

    question_list = get_questions_for_role(role)
    if not question_list:
        question_list = get_questions_for_role("default")

    total_questions = len(question_list)
    if total_questions == 0:
        return jsonify(
            {"success": False, "message": "Daftar pertanyaan belum dikonfigurasi."}
        )

    # jaga index di dalam range
    if question_index < 0:
        question_index = 0
    if question_index >= total_questions:
        question_index = total_questions - 1

    # ----- Ambil jawaban ideal & hitung similarity -----
    ideal_answers = get_ideal_answers(role, question_index)
    similarity = tfidf_cosine_score(answer_text, ideal_answers)
    score = similarity_to_score(similarity)  # 0–100 (dibatasi min 40 max 95)

    # simpan skor ke session (skor per-pertanyaan)
    scores = session.get("scores", [])
    scores.append(score)
    session["scores"] = scores

    # ----- Feedback per-pertanyaan -----
    word_count = len(answer_text.split())
    if word_count < 10:
        extra_feedback = (
            "Jawaban masih terlalu singkat. Tambahkan detail dan contoh konkret."
        )
    elif word_count < 30:
        extra_feedback = (
            "Jawaban sudah cukup, tapi masih bisa diperdalam dengan struktur yang lebih jelas."
        )
    else:
        extra_feedback = (
            "Panjang jawaban sudah baik. Pertahankan struktur dan kejelasan seperti ini."
        )

    if score < 60:
        level_feedback = "Relevansi jawaban terhadap pertanyaan masih rendah."
    elif score < 80:
        level_feedback = "Jawaban sudah cukup relevan tetapi masih bisa ditingkatkan."
    else:
        level_feedback = "Jawaban sangat relevan dengan poin-poin penting pertanyaan."

    feedback = f"{level_feedback} {extra_feedback}"

    # ----- Pertanyaan berikutnya -----
    next_question_index = question_index + 1
    if next_question_index < total_questions:
        next_question = question_list[next_question_index]
        has_next = True
    else:
        next_question = None
        has_next = False

    # ----- Hitung rata-rata kalau semua pertanyaan sudah dijawab -----
    is_finished = False
    final_avg_score = None
    overall_feedback = None

    if not has_next:
        is_finished = True
        if scores:
            final_avg_score = sum(scores) / len(scores)

            # simpan hasil sesi ke SESSION_RESULTS sebagai "rata-rata per sesi"
            SESSION_RESULTS.append(
                {
                    "role": role,
                    "average_score": round(final_avg_score, 2),
                    "user_name": user_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

            # feedback keseluruhan berdasarkan rata-rata
            if final_avg_score < 60:
                overall_feedback = (
                    "Secara keseluruhan, jawaban Anda masih kurang relevan dan kurang mendalam. "
                    "Perlu banyak latihan untuk memperjelas pengalaman, menambahkan detail teknis, "
                    "dan mengaitkan jawaban dengan kebutuhan role yang dilamar."
                )
            elif final_avg_score < 80:
                overall_feedback = (
                    "Secara keseluruhan, jawaban Anda sudah cukup baik dan relevan, "
                    "namun masih ada beberapa pertanyaan yang bisa dijawab lebih terstruktur dan spesifik. "
                    "Fokuslah pada pemberian contoh konkret dan metrik keberhasilan."
                )
            else:
                overall_feedback = (
                    "Secara keseluruhan, jawaban Anda sudah sangat baik, relevan, dan meyakinkan. "
                    "Anda berhasil menjelaskan pengalaman, teknik, dan hasil dengan jelas. "
                    "Pertahankan kualitas ini dan latih lagi penyampaian lisan saat interview sebenarnya."
                )

    return jsonify(
        {
            "success": True,
            "score": score,
            "feedback": feedback,
            "has_next": has_next,
            "next_question": next_question,
            "next_question_index": next_question_index,
            "is_finished": is_finished,
            "final_avg_score": final_avg_score,
            "overall_feedback": overall_feedback,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070, debug=True)
