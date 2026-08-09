"""
Main public routes (Home, About, FAQ).
"""
from flask import Blueprint, render_template, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    stats = {
        "total": 1482,
        "ai_accuracy": "98.4%",
        "avg_sla": "4.2 hrs",
        "resolved": 1240,
    }
    if hasattr(current_app, "analytics_mgr"):
        try:
            overview = current_app.analytics_mgr.get_overview_stats()
            stats["total"] = overview["total_complaints"]
            stats["resolved"] = overview["resolved_complaints"]
        except Exception:
            pass
    return render_template("index.html", stats=stats)


@main_bp.route("/about")
def about():
    return render_template("index.html")
