from db import get_connection
from config import ACHIEVEMENTS as ACH_DEFS

class Achievement:
    def __init__(self, id, user_id, key, title, description, icon, unlocked_at, **kwargs):
        self.id = id; self.user_id = user_id; self.key = key
        self.title = title; self.description = description
        self.icon = icon; self.unlocked_at = unlocked_at

    @staticmethod
    def get_unlocked(user_id):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM achievements WHERE user_id=? ORDER BY unlocked_at DESC", (user_id,)).fetchall()
        conn.close()
        return [Achievement(**dict(r)) for r in rows]

    @staticmethod
    def get_unlocked_keys(user_id):
        conn = get_connection()
        rows = conn.execute("SELECT key FROM achievements WHERE user_id=?", (user_id,)).fetchall()
        conn.close()
        return {r["key"] for r in rows}

    @staticmethod
    def unlock(user_id, key):
        meta = ACH_DEFS.get(key)
        if not meta:
            return False
        conn = get_connection()
        ex = conn.execute("SELECT id FROM achievements WHERE user_id=? AND key=?", (user_id, key)).fetchone()
        if ex:
            conn.close()
            return False
        conn.execute("INSERT INTO achievements (user_id,key,title,description,icon) VALUES (?,?,?,?,?)",
                     (user_id, key, meta["title"], meta["description"], meta["icon"]))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all_with_status(user_id):
        unlocked = Achievement.get_unlocked_keys(user_id)
        return [{"key":k,"title":v["title"],"description":v["description"],"icon":v["icon"],"unlocked":k in unlocked}
                for k,v in ACH_DEFS.items()]
