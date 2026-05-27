from db import get_connection
from datetime import date, timedelta

def get_last_7_days():
    return [(date.today()-timedelta(days=i)).isoformat() for i in range(6,-1,-1)]

def get_habit_chart_data(user_id):
    days = get_last_7_days()
    conn = get_connection()
    rows = conn.execute("""SELECT DATE(completed_at) as day, COUNT(*) as count
        FROM habit_logs WHERE user_id=? AND DATE(completed_at)>=? GROUP BY day""",
        (user_id, days[0])).fetchall()
    conn.close()
    m = {r["day"]: r["count"] for r in rows}
    return {"labels":[d[5:] for d in days], "data":[m.get(d,0) for d in days]}

def get_mood_chart_data(user_id):
    days = get_last_7_days()
    conn = get_connection()
    rows = conn.execute("""SELECT DATE(created_at) as day, ROUND(AVG(mood),1) as avg_mood
        FROM mood_logs WHERE user_id=? AND DATE(created_at)>=? GROUP BY day""",
        (user_id, days[0])).fetchall()
    conn.close()
    m = {r["day"]: r["avg_mood"] for r in rows}
    return {"labels":[d[5:] for d in days], "data":[m.get(d,None) for d in days]}

def get_summary(user_id):
    from models.habit import Habit
    from models.mood import Mood
    from models.achievement import Achievement
    return {
        "total_habits": Habit.get_total_completed(user_id),
        "max_streak": Habit.get_max_streak(user_id),
        "total_mood_logs": Mood.get_total_logs(user_id),
        "total_achievements": len(Achievement.get_unlocked(user_id)),
    }
