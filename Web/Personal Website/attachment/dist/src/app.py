from typing import TypeVar, Callable
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    session,
    request,
    url_for,
    jsonify,
    g,
)
from functools import wraps
import os
import logging


from user import User

app = Flask(__name__, template_folder="./")
app.secret_key = os.urandom(32)
log_handler = logging.FileHandler("flask.log")
app.logger.addHandler(log_handler)

REGISTER_TEMPLATE = "templates/register.html"
LOGIN_TEMPLATE = "templates/login.html"
INDEX_TEMPLATE = "templates/index.html"
CONFIG_TEMPLATE = "templates/config.html"

F = TypeVar("F", bound=Callable)


def login_required(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("username", False):
            flash("User must be logged in to view this page", "danger")
            return redirect(url_for("login"))
        g.user = User.get(session.get("username"))
        return func(*args, **kwargs)

    return wrapper


def unauthorized(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            return redirect(url_for("index"))
        return func(*args, **kwargs)

    return wrapper


@app.route("/register", methods=["GET", "POST"])
@unauthorized
def register():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            if not username or not password:
                raise Exception("Missing username or password")

            User.create(username, password)

            flash("Registration successful", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(str(e), "danger")
            return render_template(REGISTER_TEMPLATE)

    return render_template(REGISTER_TEMPLATE)


@app.route("/login", methods=["GET", "POST"])
@unauthorized
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password", "")
            if not username or not password:
                raise Exception("Missing username or password")

            User.verify(username, password)

            session["username"] = username
            flash("Logged in successfully", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(str(e), "danger")
            return render_template(LOGIN_TEMPLATE)

    return render_template(LOGIN_TEMPLATE)


@app.post("/api/config")
@login_required
def config_api():
    try:
        if not request.json:
            raise Exception("Input is empty")
        User.merge_info(request.json, g.get("user"))
        return jsonify({"success": "Config updated"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.get("/config")
@login_required
def config():
    return render_template(CONFIG_TEMPLATE)


@app.route("/")
@login_required
def index():
    return render_template(INDEX_TEMPLATE)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))
