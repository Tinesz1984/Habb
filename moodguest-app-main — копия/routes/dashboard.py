from flask import Blueprint, render_template, request, redirect, session
from models.user import User
from models.habit import Habit
from models.mood import Mood
from services.gamification import award_mood_log
from services.quote_api import get_quote

bp = Blueprint("dashboard", __name__)

def login_required():
    if "user_id" not in session:
        return redirect("/")

@bp.route("/dashboard")
def dashboard():
    if "user_id" not in session: return redirect("/")
    user = User.get_by_id(session["user_id"])
    habits = Habit.get_all(user.id)
    xp_in_level, xp_needed, pct = user.get_xp_in_level()
    return render_template("dashboard.html",
        user=user, habits=habits[:5],
        done_today=sum(1 for h in habits if h.is_done_today()),
        total_today=len(habits),
        summary_streak=Habit.get_max_streak(user.id),
        mood_logged=Mood.logged_today(user.id),
        last_mood=Mood.get_last(user.id),
        quote=get_quote(),
        level=user.get_level(),
        xp_in_level=xp_in_level, xp_needed=xp_needed, xp_pct=pct)

@bp.route("/log_mood", methods=["POST"])
def log_mood():
    if "user_id" not in session: return redirect("/")
    user = User.get_by_id(session["user_id"])
    if not Mood.logged_today(user.id):
        Mood.log(user.id, int(request.form.get("mood",3)), request.form.get("note",""))
        award_mood_log(user)
    return redirect("/dashboard")
