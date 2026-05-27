from flask import Blueprint, render_template, redirect, session
from models.user import User
from models.achievement import Achievement

bp = Blueprint("achievements", __name__)

@bp.route("/achievements")
def achievements():
    if "user_id" not in session: return redirect("/")
    user = User.get_by_id(session["user_id"])
    all_ach = Achievement.get_all_with_status(user.id)
    unlocked_count = sum(1 for a in all_ach if a["unlocked"])
    xp_in_level, xp_needed, pct = user.get_xp_in_level()
    return render_template("achievements.html",
        user=user, achievements=all_ach,
        unlocked_count=unlocked_count, total_count=len(all_ach),
        level=user.get_level(), xp_in_level=xp_in_level, xp_needed=xp_needed, xp_pct=pct)
