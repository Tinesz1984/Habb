from flask import Blueprint, render_template, redirect, session
from models.user import User
from services.analytics import get_mood_chart_data, get_habit_chart_data, get_summary

bp = Blueprint("stats", __name__)

@bp.route("/stats")
def stats():
    if "user_id" not in session: return redirect("/")
    user = User.get_by_id(session["user_id"])
    xp_in_level, xp_needed, pct = user.get_xp_in_level()
    return render_template("stats.html",
        user=user, mood_data=get_mood_chart_data(user.id),
        habit_data=get_habit_chart_data(user.id), summary=get_summary(user.id),
        level=user.get_level(), xp_in_level=xp_in_level, xp_needed=xp_needed, xp_pct=pct)
