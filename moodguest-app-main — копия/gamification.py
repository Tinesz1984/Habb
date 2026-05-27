from models.achievement import Achievement
from models.habit import Habit
from models.mood import Mood
from config import ACHIEVEMENTS, XP_COMPLETE_HABIT, XP_LOG_MOOD, XP_STREAK_BONUS_7, XP_STREAK_BONUS_30, XP_FIRST_HABIT

def award_habit_completion(user, habit_id):
    habit = Habit.get_by_id(habit_id, user.id)
    if not habit:
        return [], 0
    completed, streak = habit.complete()
    if not completed:
        return [], 0
    xp = XP_COMPLETE_HABIT
    if streak == 7:  xp += XP_STREAK_BONUS_7
    if streak == 30: xp += XP_STREAK_BONUS_30
    if Habit.get_total_completed(user.id) == 1: xp += XP_FIRST_HABIT
    user.add_xp(xp)
    return _check_achievements(user), xp

def award_mood_log(user):
    user.add_xp(XP_LOG_MOOD)
    return _check_mood_achievements(user), XP_LOG_MOOD

def _check_achievements(user):
    unlocked = Achievement.get_unlocked_keys(user.id)
    new = []
    total = Habit.get_total_completed(user.id)
    max_s = Habit.get_max_streak(user.id)
    level = user.get_level()
    checks = {
        "first_habit": total>=1, "habits_10": total>=10, "habits_50": total>=50, "habits_100": total>=100,
        "streak_3": max_s>=3, "streak_7": max_s>=7, "streak_30": max_s>=30,
        "level_5": level>=5, "level_10": level>=10, "xp_500": user.xp>=500, "xp_1000": user.xp>=1000,
    }
    for key, cond in checks.items():
        if cond and key not in unlocked:
            if Achievement.unlock(user.id, key):
                new.append(ACHIEVEMENTS[key])
    return new

def _check_mood_achievements(user):
    unlocked = Achievement.get_unlocked_keys(user.id)
    new = []
    total = Mood.get_total_logs(user.id)
    for key, cond in {"mood_7": total>=7, "mood_30": total>=30}.items():
        if cond and key not in unlocked:
            if Achievement.unlock(user.id, key):
                new.append(ACHIEVEMENTS[key])
    return new
