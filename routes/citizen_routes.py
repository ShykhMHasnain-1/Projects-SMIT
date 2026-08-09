"""
Citizen-facing web routes (Dashboard, Submit Complaint, View History, Notifications, Profile).
"""
import os
import uuid
from flask import (Blueprint, render_template, request, redirect, url_for,
                    session, flash, current_app, jsonify, abort)
from werkzeug.utils import secure_filename
from backend.complaint_manager import ComplaintValidationError
from backend.database import DatabaseError
from backend.models import Complaint
from backend.decorators import login_required

citizen_bp = Blueprint("citizen", __name__)


def _allowed_image(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def _save_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None
    filename = secure_filename(file_storage.filename)
    if not _allowed_image(filename):
        raise ValueError("Invalid image file type. Allowed: png, jpg, jpeg, gif, webp.")
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    try:
        file_storage.save(save_path)
    except OSError as e:
        raise ValueError(f"Could not save image: {e}")
    return f"/static/uploads/{unique_name}"


@citizen_bp.route("/citizen")
@citizen_bp.route("/citizen/dashboard")
@login_required
def dashboard():
    if session.get("role") == "admin":
        return redirect(url_for("admin.dashboard"))
    complaints = current_app.complaint_mgr.get_citizen_complaints(session["user_id"])
    recent = complaints[:5]
    stats = {
        "total": len(complaints),
        "open": sum(1 for c in complaints if c["status"] in ["Pending", "In Progress"]),
        "resolved": sum(1 for c in complaints if c["status"] == "Resolved"),
        "critical": sum(1 for c in complaints if c["priority"] == "Critical"),
    }
    return render_template("citizen_dashboard.html", complaints=recent, stats=stats)


@citizen_bp.route("/submit", methods=["GET", "POST"])
@citizen_bp.route("/complaints/submit", methods=["GET", "POST"])
@login_required
def submit_complaint():
    if session.get("role") == "admin":
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "Auto-Detect")
        location = request.form.get("location", "").strip()
        latitude = request.form.get("latitude") or None
        longitude = request.form.get("longitude") or None
        contact_phone = request.form.get("contact_phone", "").strip()

        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except ValueError:
            latitude = longitude = None

        image_path = None
        if "photos" in request.files:
            try:
                image_path = _save_image(request.files["photos"])
            except ValueError as e:
                flash(str(e), "danger")
                return render_template("submit_complaint.html", form=request.form)

        try:
            result = current_app.complaint_mgr.submit_complaint(
                citizen_id=session["user_id"],
                title=title,
                description=description,
                category=category,
                location=location,
                latitude=latitude,
                longitude=longitude,
                image_path=image_path,
                contact_phone=contact_phone,
            )
        except ComplaintValidationError as e:
            for err in e.errors:
                flash(err, "danger")
            return render_template("submit_complaint.html", form=request.form)
        except DatabaseError as e:
            flash(f"We could not save your complaint: {e}", "danger")
            return render_template("submit_complaint.html", form=request.form)

        flash(f"Ticket #{result['id']} submitted! Category: '{result['category']}' ({result['priority']} Priority).", "success")
        return redirect(url_for("citizen.complaint_detail", complaint_id=result["id"]))

    return render_template("submit_complaint.html", form={})


@citizen_bp.route("/my-complaints")
@citizen_bp.route("/complaints")
@login_required
def my_complaints():
    if session.get("role") == "admin":
        return redirect(url_for("admin.complaints_list"))
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    complaints = current_app.complaint_mgr.get_citizen_complaints(session["user_id"])
    if q:
        ql = q.lower()
        complaints = [c for c in complaints if ql in c["description"].lower()
                      or ql in c["location"].lower() or ql in c["title"].lower()]
    if status:
        complaints = [c for c in complaints if c["status"] == status]
    return render_template("my_complaints.html", complaints=complaints, q=q, status=status,
                            statuses=Complaint.VALID_STATUSES)


@citizen_bp.route("/complaints/<int:complaint_id>")
@login_required
def complaint_detail(complaint_id):
    complaint = current_app.complaint_mgr.get_complaint(complaint_id)
    if not complaint:
        abort(404)
    if session.get("role") == "citizen" and complaint["citizen_id"] != session["user_id"]:
        abort(403)
    return render_template("complaint_detail.html", c=complaint, is_admin=(session.get("role") == "admin"))


@citizen_bp.route("/notifications")
@login_required
def notifications():
    notes = current_app.notifier.get_notifications(session["user_id"])
    current_app.notifier.mark_read(session["user_id"])
    return render_template("notifications.html", notifications=notes)


@citizen_bp.route("/api/notifications/unread-count")
@login_required
def unread_count():
    notes = current_app.notifier.get_notifications(session["user_id"], unread_only=True)
    return jsonify({"count": len(notes)})


@citizen_bp.route("/profile")
@login_required
def profile():
    user = current_app.db.get_user_by_id(session["user_id"])
    if not user:
        abort(404)
    return render_template("profile.html", user=user)
