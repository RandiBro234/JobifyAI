# Repository Guidelines

## Project Structure & Module Organization

JobifyAI is a Flask web application for role-based interview practice and Indonesian text scoring. Keep route, session, dashboard, and export behavior in `app.py`. Place TF-IDF preprocessing and scoring helpers in `text_scoring.py`; reference answers live in `answer_keys.py`. Role-specific question banks belong in `questions/<role>.py` and are exposed through `questions/__init__.py`.

Jinja templates are in `templates/` (`base.html` provides the shared layout); browser assets are in `static/css/main.css` and `static/js/interview.js`. Do not commit generated `__pycache__/` files or local virtual-environment changes.

## Build, Test, and Development Commands

Create and activate a local environment, then install the pinned dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

`python app.py` starts the Flask development server. Alternatively, use `flask --app app run --debug` while developing. Verify that login, interview submission, history pagination, and Excel export work in a browser after UI or route changes.

## Coding Style & Naming Conventions

Use Python with four-space indentation, `snake_case` for functions, variables, and modules, and uppercase names for constants such as `ROLES`. Keep imports grouped as standard library, third-party, then project imports. Add type hints to new reusable scoring helpers and concise docstrings where behavior is non-obvious. Use meaningful Indonesian user-facing copy consistent with the existing templates. Keep template names lowercase (for example, `interview.html`) and match static asset paths referenced from templates.

No automated formatter or linter is configured; preserve the surrounding style and avoid unrelated reformatting.

## Testing Guidelines

There is currently no committed automated test suite or coverage threshold. Add focused `unittest` tests in a new `tests/` directory for changes to scoring, question selection, or Flask routes; name files `test_<feature>.py`. Run them with:

```powershell
python -m unittest discover -s tests
```

Test empty answers, invalid request values, and expected score bounds (0-100), in addition to successful flows.

## Commit & Pull Request Guidelines

History uses short Indonesian, imperative summaries, e.g. `Menambahkan fitur history`. Use the same style and keep each commit narrowly scoped. Pull requests should explain the behavior change, list test/manual verification performed, link any relevant issue, and include screenshots for template or CSS changes.

## Security & Configuration

Replace the placeholder Flask `SECRET_KEY` with an environment-provided secret before deployment. Never commit real secrets, user data, or generated Excel exports.
