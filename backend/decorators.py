"""
Authentication & Authorization Decorators for Flask Routes.
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request, abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        if session.get("role") != "admin":
            flash("Admin privilege required to view that page.", "danger")
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
