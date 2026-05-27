from flask import Blueprint, render_template, request, redirect, session, flash
from models.user import User

bp = Blueprint("auth", __name__)

@bp.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("auth.html")

@bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username","").strip()
    password = request.form.get("password","")
    user = User.verify(username, password)
    if user:
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/dashboard")
    flash("Invalid username or password","error")
    return redirect("/")

@bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username","").strip()
    password = request.form.get("password","")
    if len(username) < 3:
        flash("Username must be at least 3 characters","error")
        return redirect("/")
    if len(password) < 4:
        flash("Password must be at least 4 characters","error")
        return redirect("/")
    user = User.create(username, password)
    if not user:
        flash("Username already taken","error")
        return redirect("/")
    session["user_id"] = user.id
    session["username"] = user.username
    return redirect("/dashboard")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
