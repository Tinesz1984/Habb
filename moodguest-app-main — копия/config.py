import os
SECRET_KEY = os.environ.get("SECRET_KEY", "habitquest_super_secret_2024")
XP_COMPLETE_HABIT = 20
XP_LOG_MOOD = 10
XP_STREAK_BONUS_7 = 50
XP_STREAK_BONUS_30 = 200
XP_FIRST_HABIT = 30
LEVEL_BASE = 100
LEVEL_INCREMENT = 50
ICONS = ["⭐","💪","🏃","📚","🧘","💧","🥗","😴","🎯","✍️","🎵","🌿","🏋️","🚴","🧠","❤️","🌅","🎨","🍎","🤝"]
ACHIEVEMENTS = {
    "first_habit":  {"title":"First Step",       "description":"Complete your first habit",    "icon":"🌱"},
    "habits_10":    {"title":"Getting Warmed Up", "description":"Complete 10 habits total",     "icon":"🔥"},
    "habits_50":    {"title":"Habit Machine",     "description":"Complete 50 habits total",     "icon":"⚡"},
    "habits_100":   {"title":"Legend",            "description":"Complete 100 habits total",    "icon":"👑"},
    "streak_3":     {"title":"On a Roll",         "description":"3-day streak on any habit",    "icon":"🎯"},
    "streak_7":     {"title":"Week Warrior",      "description":"7-day streak on any habit",    "icon":"🦾"},
    "streak_30":    {"title":"Iron Will",         "description":"30-day streak on any habit",   "icon":"💎"},
    "mood_7":       {"title":"Mood Tracker",      "description":"Log your mood 7 days",         "icon":"😊"},
    "mood_30":      {"title":"Mood Master",       "description":"Log your mood 30 days",        "icon":"🧘"},
    "level_5":      {"title":"Rising Star",       "description":"Reach level 5",               "icon":"🌟"},
    "level_10":     {"title":"Veteran",           "description":"Reach level 10",              "icon":"🏆"},
    "xp_500":       {"title":"XP Hunter",         "description":"Earn 500 XP",                 "icon":"💰"},
    "xp_1000":      {"title":"XP Millionaire",    "description":"Earn 1000 XP",                "icon":"💎"},
}
