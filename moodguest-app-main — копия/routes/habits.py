from flask import Blueprint, render_template, request, redirect, session, jsonify
from models.user import User
from models.habit import Habit
from services.gamification import award_habit_completion
from config import ICONS

bp = Blueprint("habits", __name__)

@bp.route("/habits")
def habits():
    if "user_id" not in session: return redirect("/")
    user = User.get_by_id(session["user_id"])
    xp_in_level, xp_needed, pct = user.get_xp_in_level()
    return render_template("habits.html",
        user=user, habits=Habit.get_all(user.id), icons=ICONS,
        level=user.get_level(), xp_in_level=xp_in_level, xp_needed=xp_needed, xp_pct=pct)

@bp.route("/habits/add", methods=["POST"])
def add_habit():
    if "user_id" not in session: return redirect("/")
    name = request.form.get("name","").strip()
    icon = request.form.get("icon","⭐")
    if name:
        Habit.create(session["user_id"], name, icon)
    return redirect("/habits")

@bp.route("/habits/complete/<int:habit_id>", methods=["POST"])
def complete_habit(habit_id):
    if "user_id" not in session: return redirect("/")
    user = User.get_by_id(session["user_id"])
    new_achievements, xp = award_habit_completion(user, habit_id)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        habit = Habit.get_by_id(habit_id, user.id)
        return jsonify({"success": True, "xp_gained": xp, "new_xp": user.xp,
                        "level": user.get_level(), "achievements": new_achievements,
                        "streak": habit.streak if habit else 0})
    return redirect(request.referrer or "/habits")

@bp.route("/habits/delete/<int:habit_id>", methods=["POST"])
def delete_habit(habit_id):
    if "user_id" not in session: return redirect("/")
    Habit.delete(habit_id, session["user_id"])
    return redirect("/habits")
