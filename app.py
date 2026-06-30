import os
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database.database import (
    create_user,
    get_history,
    init_db,
    save_search_history,
    verify_user,
)
from src.pipeline.prediction_pipeline import PredictionPipeline

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")

    init_db()

    try:
        app.recommender = PredictionPipeline(artifacts_dir=str(ARTIFACTS_DIR))
    except Exception as exc:
        app.recommender = None
        print(f"Recommendation pipeline load failed: {exc}")

    return app


app = create_app()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("home"))
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        user = verify_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful.", "success")
            return redirect(url_for("home"))

        flash("Invalid username or password.", "danger")

    return render_template(
        "login.html",
        title="Login",
        form_action=url_for("login"),
        button_text="Login",
        alternate_text="Don’t have an account?",
        alternate_label="Register now",
        alternate_url=url_for("register"),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not password:
            flash("Both username and password are required.", "danger")
        elif password != confirm_password:
            flash("Passwords do not match.", "danger")
        elif create_user(username, password):
            flash("Account created successfully. Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username is already taken.", "danger")

    return render_template(
        "login.html",
        title="Register",
        form_action=url_for("register"),
        button_text="Create account",
        alternate_text="Already have an account?",
        alternate_label="Login here",
        alternate_url=url_for("login"),
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/home", methods=["GET"])
@login_required
def home():
    return render_template(
        "home.html",
        username=session.get("username", "Guest"),
    )


@app.route("/recommend", methods=["POST"])
@login_required
def recommend():
    if app.recommender is None:
        flash("Recommendation engine is unavailable. Please check artifacts.", "danger")
        return redirect(url_for("home"))

    query = request.form.get("book_name", "").strip()
    top_n = int(request.form.get("top_n", 5))

    if not query:
        flash("Please enter a book title to get recommendations.", "warning")
        return redirect(url_for("home"))

    try:
        recommendations = app.recommender.recommend_books(query, top_n=top_n)
        results = [row for row in recommendations.to_dict(orient="records")]
        save_search_history(session["user_id"], query, results)

        return render_template(
            "recommendation.html",
            query=query,
            recommendations=results,
        )

    except Exception as exc:
        flash(str(exc), "danger")
        return redirect(url_for("home"))


@app.route("/history")
@login_required
def history():
    history_items = get_history(session["user_id"])
    return render_template(
        "history.html",
        username=session.get("username", "Guest"),
        history_items=history_items,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
