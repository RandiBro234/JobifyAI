from .data_scientist import QUESTIONS as DS_QUESTIONS
from .data_engineer import QUESTIONS as DE_QUESTIONS
from .web_developer import QUESTIONS as WEB_QUESTIONS
from .backend_developer import QUESTIONS as BE_QUESTIONS
from .frontend_developer import QUESTIONS as FE_QUESTIONS
from .ml_engineer import QUESTIONS as ML_QUESTIONS
from .mobile_developer import QUESTIONS as MOB_QUESTIONS

# List role yang muncul di dropdown login
ROLES = [
    "Data Scientist",
    "Data Engineer",
    "Web Developer",
    "Backend Developer",
    "Frontend Developer",
    "Machine Learning Engineer",
    "Mobile Developer",
]

ROLE_QUESTION_MAP = {
    "data scientist": DS_QUESTIONS,
    "data engineer": DE_QUESTIONS,
    "web developer": WEB_QUESTIONS,
    "backend developer": BE_QUESTIONS,
    "frontend developer": FE_QUESTIONS,
    "machine learning engineer": ML_QUESTIONS,
    "mobile developer": MOB_QUESTIONS,
}

# default: pakai pertanyaan Data Scientist
DEFAULT_QUESTIONS = DS_QUESTIONS


def get_questions_for_role(role_name: str):
    if not role_name:
        return DEFAULT_QUESTIONS
    key = role_name.strip().lower()
    return ROLE_QUESTION_MAP.get(key, DEFAULT_QUESTIONS)
