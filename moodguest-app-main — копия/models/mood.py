from db import get_connection

MOOD_LABELS = {1:"Terrible",2:"Bad",3:"Okay",4:"Good",5:"Amazing"}
MOOD_EMOJIS = {1:"😢",2:"😞",3:"😐",4:"😊",5:"😄"}

class Mood:
    def __init__(self, id, user_id, mood, note, created_at, **kwargs):
        self.id = id
        self.user_id = user_id
        self.mood = mood
        self.note = note
        self.created_at = created_at
        self.label = MOOD_LABELS.get(mood, "")
        self.emoji = MOOD_EMOJIS.get(mood, "")

    @staticmethod
    def log(user_id, mood, note=""):
        conn = get_connection()
        conn.execute("INSERT INTO mood_logs (user_id,mood,note) VALUES (?,?,?)", (user_id, mood, note))
        conn.commit()
        conn.close()

    @staticmethod
    def logged_today(user_id):
        conn = get_connection()
        row = conn.execute("SELECT id FROM mood_logs WHERE user_id=? AND DATE(created_at)=DATE('now') LIMIT 1", (user_id,)).fetchone()
        conn.close()
        return row is not None

    @staticmethod
    def get_total_logs(user_id):
        conn = get_connection()
        row = conn.execute("SELECT COUNT(*) as n FROM mood_logs WHERE user_id=?", (user_id,)).fetchone()
        conn.close()
        return row["n"] if row else 0

    @staticmethod
    def get_last(user_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM mood_logs WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,)).fetchone()
        conn.close()
        return Mood(**dict(row)) if row else None

    @staticmethod
    def get_recent(user_id, days=7):
        conn = get_connection()
        rows = conn.execute("""
            SELECT DATE(created_at) as day, ROUND(AVG(mood),1) as avg_mood
            FROM mood_logs WHERE user_id=? AND created_at>=DATE('now',? || ' days')
            GROUP BY day ORDER BY day
        """, (user_id, f"-{days-1}")).fetchall()
        conn.close()
        return [dict(r) for r in rows]
