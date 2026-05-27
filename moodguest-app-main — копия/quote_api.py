import requests
import random

FALLBACK = [
    "Small habits make big differences.",
    "Consistency is the key to achievement.",
    "Every day is a chance to be better.",
    "Discipline is freedom.",
    "Show up every day. That's the secret.",
    "You are what you repeatedly do.",
    "Success is the sum of small efforts repeated.",
    "Motivation is what gets you started. Habit keeps you going.",
    "Little by little, a little becomes a lot.",
    "Progress, not perfection.",
    "Don't count the days. Make the days count.",
    "Build the life you want, one habit at a time.",
]

def get_quote():
    try:
        response = requests.get(
            "https://zenquotes.io/api/random",
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                return {
                    "content": data[0].get("q", random.choice(FALLBACK)),
                    "author": data[0].get("a", "Unknown")
                }

    except Exception as e:
        print(f"Quote API error: {e}")

    return {
        "content": random.choice(FALLBACK),
        "author": "HabitQuest"
    }
