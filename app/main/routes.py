import sqlalchemy as sa
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from datetime import datetime

from app import db
from app.models import User, Session
from app.forms import LoginForm, RegistrationForm
from app.main import bp

def can_manage_session(session_obj):
    return (session_obj.created_by_id == current_user.id) or getattr(current_user, "is_admin", False)

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))

        if user is None:
            form.email.errors.append("Email not recognized.")
            return render_template("login.html", form=form)

        if getattr(user, "disabled", False):
            form.email.errors.append("This account has been disabled by an admin.")
            return render_template("login.html", form=form)

        if not user.check_password(form.password.data):
            form.password.errors.append("Incorrect password.")
            return render_template("login.html", form=form)

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main.home"))

    return render_template("login.html", form=form)



@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            gender=form.gender.data,
            study=form.study.data,
            faculty=form.faculty.data,
            grad_year=form.grad_year.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("main.dashboard"))

    return render_template("register.html", form=form)

@bp.route("/dashboard")
@login_required
def dashboard():
    sessions = db.session.scalars(sa.select(Session)).all()
    return render_template("dashboard.html", study_requests=sessions)

@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@bp.route("/profile/<int:user_id>")
@login_required
def user_profile(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    return render_template("profile.html", user=user)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_request():
    if request.method == "POST":
        subject = request.form["subject"]
        description = request.form["description"]
        location = request.form["location"]

        date_str = request.form["date"]
        time_str = request.form["time"]
        starts_at = datetime.fromisoformat(f"{date_str}T{time_str}")

        s = Session(
            subject=subject,
            description=description,
            location=location,
            starts_at=starts_at,
            created_by_id=current_user.id,
        )
        db.session.add(s)
        db.session.commit()
        flash("Study session created!")
        return redirect(url_for("main.dashboard"))

    return render_template("create_session.html")

@bp.route("/sessions/<int:request_id>/join", methods=["POST"])
@login_required
def join_request(request_id):
    session_obj = db.session.get(Session, request_id)
    if session_obj is None:
        abort(404)

    if session_obj.created_by_id == current_user.id:
        flash("You can’t join your own session.")
        return redirect(url_for("main.dashboard"))

    # optional: block disabled users
    if getattr(current_user, "disabled", False):
        flash("Your account is disabled.")
        return redirect(url_for("main.dashboard"))

    # avoid duplicate join
    if current_user in session_obj.participants:
        flash("You already joined this session.")
        return redirect(url_for("main.dashboard"))

    session_obj.participants.append(current_user)
    db.session.commit()
    flash("You joined the session!")
    return redirect(url_for("main.dashboard"))

@bp.route("/sessions/<int:session_id>/delete", methods=["POST"])
@login_required
def delete_session(session_id):
    session_obj = db.session.get(Session, session_id)
    if session_obj is None:
        abort(404)

    if not can_manage_session(session_obj):
        abort(403)

    db.session.delete(session_obj)
    db.session.commit()
    flash("Session deleted.")
    return redirect(url_for("main.dashboard"))

@bp.route("/sessions/<int:session_id>/edit", methods=["GET", "POST"])
@login_required
def edit_session(session_id):
    session_obj = db.session.get(Session, session_id)
    if session_obj is None:
        abort(404)

    if not can_manage_session(session_obj):
        abort(403)

    if request.method == "POST":
        session_obj.subject = request.form["subject"]
        session_obj.description = request.form["description"]
        session_obj.location = request.form["location"]

        date_str = request.form["date"]   # YYYY-MM-DD
        time_str = request.form["time"]   # HH:MM
        session_obj.starts_at = datetime.fromisoformat(f"{date_str}T{time_str}")

        db.session.commit()
        flash("Session updated.")
        return redirect(url_for("main.dashboard"))

    # prefill date/time in the form
    date_value = session_obj.starts_at.strftime("%Y-%m-%d")
    time_value = session_obj.starts_at.strftime("%H:%M")
    return render_template(
        "edit_session.html",
        s=session_obj,
        date_value=date_value,
        time_value=time_value
    )


@bp.route("/admin")
@login_required
def admin_panel():
    if not getattr(current_user, "is_admin", False):
        abort(403)

    all_users = db.session.scalars(sa.select(User)).all()
    all_sessions = db.session.scalars(sa.select(Session)).all()

    return render_template("admindashboard.html", users=all_users, sessions=all_sessions)


@bp.route("/admin/user/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    if not getattr(current_user, "is_admin", False):
        abort(403)

    user_obj = db.session.get(User, user_id)
    if user_obj:
        if user_obj.id == current_user.id:
            flash("You cannot delete your own admin account!")
        else:
            db.session.delete(user_obj)
            db.session.commit()
            flash(f"User {user_obj.name} deleted.")

    return redirect(url_for("main.admin_panel"))

@bp.route("/sessions/<int:request_id>/leave", methods=["POST"])
@login_required
def leave_request(request_id):
    session_obj = db.session.get(Session, request_id)
    if session_obj is None:
        abort(404)

    if session_obj.created_by_id == current_user.id:
        flash("You can’t leave your own session.")
        return redirect(url_for("main.dashboard"))

    if current_user not in session_obj.participants:
        flash("You are not a participant of this session.")
        return redirect(url_for("main.dashboard"))

    session_obj.participants.remove(current_user)
    db.session.commit()
    flash("Left session successfully!")
    return redirect(url_for("main.dashboard"))

