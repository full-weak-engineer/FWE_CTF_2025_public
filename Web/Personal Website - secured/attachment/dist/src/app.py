import sys
from typing import TypeVar, Callable
from flask import (
    Flask,
    flash,
    redirect,
    session,
    request,
    url_for,
    jsonify,
    send_from_directory,
    g
)
from functools import wraps
import os
import logging

from user import User

app = Flask(__name__, template_folder="./")
app.secret_key = os.urandom(32)
# log_handler = logging.FileHandler("flask.log")
# app.logger.addHandler(log_handler)

REGISTER_TEMPLATE = "register.html"
LOGIN_TEMPLATE = "login.html"
INDEX_TEMPLATE = "index.html"
CONFIG_TEMPLATE = "config.html"

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

            return redirect("/login?success=Registration+successful")
        except Exception as e:
            return redirect("/register?error=" + str(e))

    return send_from_directory('templates', REGISTER_TEMPLATE)


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
            return redirect(url_for("index"))
        except Exception as e:
            return redirect("/login?error=" + str(e))

    return send_from_directory('templates', LOGIN_TEMPLATE)

@app.route("/config")
@login_required
def config():
    return send_from_directory('templates', CONFIG_TEMPLATE)

@app.route("/")
@login_required
def index():
    return send_from_directory('templates', INDEX_TEMPLATE)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.get("/api/user")
@login_required
def user_api_get():
    return jsonify({
        "username": g.user.username,
        "config": g.user.config
    })


@app.post("/api/config")
@login_required
def config_api_post():
    try:
        if not request.json:
            raise Exception("Input is empty")
        User.merge_info(request.json, g.get("user"))
        return jsonify({"success": "Config updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

def audit_hook(event, args):
    if event == "import":
        print(args, flush=True)


did_init = False
@app.before_request
def before():
    global did_init
    if did_init:
        return
    did_init = True
    User.create('test', os.urandom(32).hex())
    def audit_hook(event, _args):
        if event == "import":
            raise Exception("import shouldn't happen... someone must be trying to hack!")
    sys.addaudithook(audit_hook)