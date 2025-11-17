import os
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
)
from werkzeug.utils import secure_filename

from questions import get_questions_for_role, ROLES
from answer_keys import get_ideal_answers
from text_scoring import tfidf_cosine_score, similarity_to_score

app = Flask(__name__)

# ========== CONFIG ==========
app.config["SECRET_KEY"] = "ganti_ini_dengan_secret_keymu"
BASE_DIR = os.path.dirname(__file__)
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Dummy data dashboard
DASHBOARD_STATS = {
    "total_sessions": 12,
    "avg_score": 80.7,
    "best_score": 91,
    "streak_days": 5,
    "progress_scores": [67, 75, 84, 78, 89, 82, 91],
}


# ========== CONTEXT PROCESSOR ==========
@app.context_processor
def inject_user():
    return dict(
        user_name=session.get("user_name"),
        user_role=session.get("user_role"),
        cv_filename=session.get("cv_filename"),
    )


# ========== LOGIN ==========
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "").strip()
        cv_file = request.files.get("cv")

        if not name or not role:
            error = "Nama dan Role wajib diisi."
        else:
            filename = None
            if cv_file and cv_file.filename:
                filename = secure_filename(cv_file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                cv_file.save(save_path)

            session["user_name"] = name
            session["user_role"] = role
            session["cv_filename"] = filename

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

    return render_template(
        "dashboard.html",
        stats=DASHBOARD_STATS,
        scores=DASHBOARD_STATS["progress_scores"],
        title="Dashboard - Jobify.ai",
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

    session["total_questions"] = len(question_list)

    first_question = question_list[0]

    return render_template(
        "interview.html",
        question=first_question,
        total_questions=len(question_list),
        title="Wawancara - Jobify.ai",
    )


# ========== API EVALUATE (TF-IDF + COSINE) ==========
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
    question_list = get_questions_for_role(role)
    if not question_list:
        question_list = get_questions_for_role("default")

    total_questions = len(question_list)

    # jaga index tetap di range
    if question_index < 0:
        question_index = 0
    if question_index >= total_questions:
        question_index = total_questions - 1

    # ====== Ambil jawaban ideal & hitung similarity ======
    ideal_answers = get_ideal_answers(role, question_index)
    similarity = tfidf_cosine_score(answer_text, ideal_answers)
    score = similarity_to_score(similarity)

    # Buat feedback sederhana berdasarkan skor + panjang jawaban
    word_count = len(answer_text.split())
    if word_count < 10:
        extra_feedback = "Jawaban masih terlalu singkat. Coba tambahkan detail dan contoh konkret."
    elif word_count < 30:
        extra_feedback = "Jawaban sudah cukup, tapi masih bisa diperdalam dengan struktur yang lebih jelas."
    else:
        extra_feedback = "Panjang jawaban sudah baik. Pertahankan struktur dan kejelasan seperti ini."

    if score < 60:
        level_feedback = "Relevansi jawaban terhadap pertanyaan masih rendah."
    elif score < 80:
        level_feedback = "Jawaban sudah cukup relevan tetapi masih bisa ditingkatkan."
    else:
        level_feedback = "Jawaban sangat relevan dengan poin-poin penting pertanyaan."

    feedback = f"{level_feedback} {extra_feedback}"

    # ====== Pertanyaan berikutnya ======
    next_question_index = question_index + 1
    if next_question_index < total_questions:
        next_question = question_list[next_question_index]
        has_next = True
    else:
        next_question = None
        has_next = False

    return jsonify(
        {
            "success": True,
            "score": score,
            "feedback": feedback,
            "has_next": has_next,
            "next_question": next_question,
            "next_question_index": next_question_index,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070, debug=True)
