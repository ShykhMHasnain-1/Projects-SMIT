"""
Admin-facing routes (Dashboard, Complaint Management, Status Updates, Analytics).
"""
from flask import (Blueprint, render_template, request, redirect, url_for,
                    session, flash, current_app, abort)
from backend.decorators import admin_required
from backend.models import Complaint

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@admin_bp.route("/admin/dashboard")
@admin_required
def dashboard():
    all_complaints = current_app.complaint_mgr.get_all_complaints(limit=50)
    overview = current_app.analytics_mgr.get_overview_stats()
    recent = all_complaints[:8]
    return render_template(
        "admin_dashboard.html",
        complaints=recent,
        stats=overview,
        categories=Complaint.VALID_CATEGORIES,
    )


@admin_bp.route("/admin/complaints")
@admin_required
def complaints_list():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    category = request.args.get("category", "")
    priority = request.args.get("priority", "")

    all_complaints = current_app.complaint_mgr.get_all_complaints(limit=200)

    if q:
        ql = q.lower()
        all_complaints = [
            c for c in all_complaints
            if ql in c["title"].lower() or ql in c["description"].lower()
            or ql in c["location"].lower() or ql in str(c["id"])
        ]
    if status:
        all_complaints = [c for c in all_complaints if c["status"] == status]
    if category:
        all_complaints = [c for c in all_complaints if c["category"] == category]
    if priority:
        all_complaints = [c for c in all_complaints if c["priority"] == priority]

    return render_template(
        "admin_complaints.html",
        complaints=all_complaints,
        q=q,
        status=status,
        category=category,
        priority=priority,
        statuses=Complaint.VALID_STATUSES,
        categories=Complaint.VALID_CATEGORIES,
        priorities=Complaint.VALID_PRIORITIES,
    )


@admin_bp.route("/admin/complaints/<int:complaint_id>/update", methods=["POST"])
@admin_required
def update_status(complaint_id):
    new_status = request.form.get("status", "").strip()
    comment = request.form.get("comment", "").strip() or f"Status changed to {new_status} by Admin."

    if new_status not in Complaint.VALID_STATUSES:
        flash("Invalid status selection.", "danger")
        return redirect(url_for("citizen.complaint_detail", complaint_id=complaint_id))

    success = current_app.complaint_mgr.update_status(
        complaint_id=complaint_id,
        new_status=new_status,
        comment=comment,
        admin_id=session["user_id"],
    )

    if success:
        flash(f"Ticket #{complaint_id} status updated to '{new_status}'. Notification dispatched.", "success")
    else:
        flash("Failed to update complaint status.", "danger")

    return redirect(url_for("citizen.complaint_detail", complaint_id=complaint_id))


@admin_bp.route("/admin/analytics")
@admin_required
def analytics():
    overview = current_app.analytics_mgr.get_overview_stats()
    return render_template("admin_analytics.html", stats=overview)
