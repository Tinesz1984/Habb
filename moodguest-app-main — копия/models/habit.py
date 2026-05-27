from db import get_connection
from datetime import date, timedelta

class Habit:
    def __init__(self, id, user_id, name, icon, streak, best_streak, last_completed, created_at, **kwargs):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.icon = icon
        self.streak = streak or 0
        self.best_streak = best_streak or 0
        self.last_completed = last_completed
        self.created_at = created_at

    def is_done_today(self):
        return self.last_completed == date.today().isoformat()

    def complete(self):
        today = date.today().isoformat()
        if self.is_done_today():
            return False, 0
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        new_streak = (self.streak + 1) if self.last_completed == yesterday else 1
        new_best = max(new_streak, self.best_streak or 0)
        conn = get_connection()
        conn.execute("UPDATE habits SET streak=?,best_streak=?,last_completed=? WHERE id=?",
                     (new_streak, new_best, today, self.id))
        conn.execute("INSERT INTO habit_logs (habit_id, user_id) VALUES (?,?)", (self.id, self.user_id))
        conn.commit()
        conn.close()
        self.streak = new_streak
        self.best_streak = new_best
        self.last_completed = today
        return True, new_streak

    @staticmethod
    def get_all(user_id):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM habits WHERE user_id=? ORDER BY created_at DESC", (user_id,)).fetchall()
        conn.close()
        return [Habit(**dict(r)) for r in rows]

    @staticmethod
    def get_by_id(habit_id, user_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM habits WHERE id=? AND user_id=?", (habit_id, user_id)).fetchone()
        conn.close()
        return Habit(**dict(row)) if row else None

    @staticmethod
    def create(user_id, name, icon="⭐"):
        conn = get_connection()
        conn.execute("INSERT INTO habits (user_id,name,icon) VALUES (?,?,?)", (user_id, name, icon))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(habit_id, user_id):
        conn = get_connection()
        conn.execute("DELETE FROM habit_logs WHERE habit_id=?", (habit_id,))
        conn.execute("DELETE FROM habits WHERE id=? AND user_id=?", (habit_id, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_total_completed(user_id):
        conn = get_connection()
        row = conn.execute("SELECT COUNT(*) as n FROM habit_logs WHERE user_id=?", (user_id,)).fetchone()
        conn.close()
        return row["n"] if row else 0

    @staticmethod
    def get_max_streak(user_id):
        conn = get_connection()
        row = conn.execute("SELECT MAX(best_streak) as m FROM habits WHERE user_id=?", (user_id,)).fetchone()
        conn.close()
        return row["m"] or 0
