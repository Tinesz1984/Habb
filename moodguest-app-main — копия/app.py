from flask import Flask
from db import init_db
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
init_db()

from routes.auth import bp as auth_bp
from routes.dashboard import bp as dashboard_bp
from routes.habits import bp as habits_bp
from routes.achievements import bp as achievements_bp
from routes.stats import bp as stats_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(habits_bp)
app.register_blueprint(achievements_bp)
app.register_blueprint(stats_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
