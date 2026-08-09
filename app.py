"""
AI Smart Civic Services — application entry point.

Run locally:
    pip install -r requirements.txt
    python backend/train_model.py   # trains & saves the AI NLP model
    python app.py

Then open http://localhost:5000
Default admin login: admin@civic.gov / Admin@123
Default citizen login: citizen@civic.gov / Citizen@123
"""
import os
from flask import Flask, render_template
from config import config_map

from backend.database import DatabaseManager, DatabaseError
from backend.ai_analyzer import AIAnalyzer
from backend.notifications import NotificationManager
from backend.complaint_manager import ComplaintManager
from backend.analytics import AnalyticsManager

from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.citizen_routes import citizen_bp
from routes.admin_routes import admin_bp
from routes.api_routes import api_bp


def create_app(env: str | None = None) -> Flask:
    env = env or os.environ.get("FLASK_ENV", "default")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_folder = os.path.join(base_dir, "frontend", "templates")
    static_folder = os.path.join(base_dir, "frontend", "static")
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.config.from_object(config_map.get(env, config_map["default"]))
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ---- Wire up backend services (dependency composition root) ----
    app.db = DatabaseManager(app.config["DATABASE_PATH"])
    app.ai = AIAnalyzer(app.config["AI_MODEL_DIR"])
    app.notifier = NotificationManager(app.db)
    app.complaint_mgr = ComplaintManager(app.db, app.ai, app.notifier)
    app.analytics_mgr = AnalyticsManager(app.db)

    # ---- Blueprints ----
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # ---- Error handling ----
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404,
                                message="Page not found."), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403,
                                message="You don't have permission to view this page."), 403

    @app.errorhandler(DatabaseError)
    def db_error(e):
        return render_template("error.html", code=500,
                                message=f"A database error occurred: {e}"), 500

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", code=500,
                                message="Something went wrong on our end. Please try again."), 500

    @app.context_processor
    def inject_globals():
        from flask import session
        unread = 0
        if "user_id" in session:
            try:
                unread = len(app.notifier.get_notifications(session["user_id"], unread_only=True))
            except Exception:
                unread = 0
        return {"unread_notifications": unread}

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting AI Smart Civic Services Flask Server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))