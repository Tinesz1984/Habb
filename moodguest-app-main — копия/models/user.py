from db import get_connection
from config import LEVEL_BASE, LEVEL_INCREMENT

class User:
    def __init__(self, id, username, xp=0, **kwargs):
        self.id = id
        self.username = username
        self.xp = xp

    @staticmethod
    def get_by_id(user_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        conn.close()
        return User(**dict(row)) if row else None

    @staticmethod
    def create(username, password):
        conn = get_connection()
        try:
            conn.execute("INSERT INTO users (username,password,xp) VALUES (?,?,0)", (username, password))
            conn.commit()
            row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
            conn.close()
            return User(**dict(row))
        except Exception:
            conn.close()
            return None

    @staticmethod
    def verify(username, password):
        conn = get_connection()
        row = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()
        return User(**dict(row)) if row else None

    def add_xp(self, amount):
        self.xp += amount
        conn = get_connection()
        conn.execute("UPDATE users SET xp=? WHERE id=?", (self.xp, self.id))
        conn.commit()
        conn.close()

    def get_level(self):
        xp, level, needed = self.xp, 1, LEVEL_BASE
        while xp >= needed:
            xp -= needed; level += 1; needed = LEVEL_BASE + (level-1)*LEVEL_INCREMENT
        return level

    def get_xp_in_level(self):
        xp, level, needed = self.xp, 1, LEVEL_BASE
        while xp >= needed:
            xp -= needed; level += 1; needed = LEVEL_BASE + (level-1)*LEVEL_INCREMENT
        pct = int((xp/needed)*100) if needed else 0
        return xp, needed, pct
