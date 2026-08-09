"""
REST API endpoints (AI text classification, Chatbot integration, Analytics JSON).
"""
from flask import Blueprint, request, jsonify, current_app

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/ai/predict", methods=["POST"])
def predict_ai():
    data = request.get_json(silent=True) or {}
    description = data.get("description", "").strip()
    title = data.get("title", "").strip()

    if not description:
        return jsonify({"error": "Description field is required for AI prediction."}), 400

    result = current_app.ai.analyze_complaint(description, title)
    return jsonify(result)


@api_bp.route("/chatbot/query", methods=["POST"])
def chatbot_query():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please type a message.", "action": "empty"}), 400

    result = current_app.ai.generate_chatbot_reply(message)
    return jsonify(result)


@api_bp.route("/analytics/overview", methods=["GET"])
def analytics_overview():
    stats = current_app.analytics_mgr.get_overview_stats()
    return jsonify(stats)


@api_bp.route("/complaints", methods=["GET"])
def list_complaints_json():
    limit = request.args.get("limit", 50, type=int)
    complaints = current_app.complaint_mgr.get_all_complaints(limit=limit)
    return jsonify({"count": len(complaints), "items": complaints})
