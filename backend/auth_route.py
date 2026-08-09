from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from backend.models import Citizen
from backend.database import DatabaseError

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if password != confirm:
            errors.append("Passwords do not match.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")

        citizen = Citizen(name=name, email=email, password=password, phone=phone)
        errors.extend(citizen.validate())

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("register.html", form=request.form)

        try:
            user_id = current_app.db.create_user(citizen)
        except DatabaseError as e:
            flash(str(e), "danger")
            return render_template("register.html", form=request.form)

        session.clear()
        session["user_id"] = user_id
        session["role"] = "citizen"
        session["name"] = citizen.name
        flash("Account created successfully. Welcome!", "success")
        return redirect(url_for("citizen.dashboard"))

    return render_template("register.html", form={})


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")

        try:
            user = current_app.db.get_user_by_email(email)
        except DatabaseError:
            flash("A database error occurred. Please try again.", "danger")
            return render_template("login.html")

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role
        session["name"] = user.name
        flash(f"Welcome back, {user.name}!", "success")
        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("citizen.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))