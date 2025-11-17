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

app = Flask(__name__)

# ====== CONFIG ======
app.config["SECRET_KEY"] = "ganti_ini_secret_keymu"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Dummy data
DASHBOARD_STATS = {
    "total_sessions": 12,
    "avg_score": 80.7,
    "best_score": 91,
    "streak_days": 5,
    "progress_scores": [67, 75, 84, 78, 89, 82, 91],
}

# List pertanyaan wawancara
QUESTIONS = [
    "Ceritakan tentang diri Anda.",
    "Apa kelebihan utama yang Anda miliki?",
    "Ceritakan pengalaman ketika Anda memecahkan masalah sulit.",
    "Apa alasan kami harus menerima Anda di Jobify.ai?",
]

# Roles yang muncul di dropdown
ROLES = [
    "Data Scientist",
    "Data Engineer",
    "Web Developer",
    "Backend Developer",
    "Frontend Developer",
    "Machine Learning Engineer",
    "Mobile Developer",
]


# ======= CONTEXT PROCESSOR =======
@app.context_processor
def inject_user():
    return dict(
        user_name=session.get("user_name"),
        user_role=session.get("user_role"),
        cv_filename=session.get("cv_filename"),
    )


# ======= LOGIN PAGE =======
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


# ======= LOGOUT =======
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ======= DASHBOARD =======
@app.route("/")
def dashboard():
    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        stats=DASHBOARD_STATS,
        scores=DASHBOARD_STATS["progress_scores"],
        title="Dashboard - Jobify.ai",
    )


# ======= INTERVIEW =======
@app.route("/interview")
def interview():
    if "user_name" not in session:
        return redirect(url_for("login"))

    first_question = QUESTIONS[0]

    return render_template(
        "interview.html",
        question=first_question,
        total_questions=len(QUESTIONS),
        title="Wawancara - Jobify.ai",
    )


# ======= API EVALUATE =======
@app.route("/api/evaluate", methods=["POST"])
def evaluate_answer():
    data = request.get_json()
    answer_text = data.get("answer", "").strip()
    q_index = data.get("question_index", 0)

    if not answer_text:
        return jsonify({"success": False, "message": "Jawaban masih kosong."})

    # Dummy model scoring
    length = len(answer_text.split())
    if length < 10:
        score = 55
        feedback = "Jawaban terlalu singkat. Tambah detail & contoh."
    elif length < 40:
        score = 75
        feedback = "Cukup baik, tapi masih bisa dibuat lebih terstruktur."
    else:
        score = 90
        feedback = "Sangat lengkap & jelas. Pertahankan!"

    # Next question
    next_index = q_index + 1
    if next_index < len(QUESTIONS):
        next_question = QUESTIONS[next_index]
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
            "next_question_index": next_index,
        }
    )


if __name__ == "__main__":
    app.run(port=7070, host='0.0.0.0', debug=True)
