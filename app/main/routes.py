import sqlalchemy as sa
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from datetime import datetime

from app import db
from app.models import User, Session
from app.forms import LoginForm, RegistrationForm
from app.main import bp

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

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_request():
    if request.method == "POST":
        subject = request.form["subject"]
        description = request.form.get("description", "")
        location = request.form["location"]

        # verwacht input name="starts_at" type="datetime-local"
        starts_at_str = request.form["starts_at"]
        starts_at = datetime.fromisoformat(starts_at_str)

        s = Session(
            subject=subject,
            description=description,
            location=location,
            starts_at=starts_at,
            created_by_id=current_user.id,
        )
        db.session.add(s)
        db.session.commit()
        flash("Study session posted!")
        return redirect(url_for("main.dashboard"))

    return render_template("create_appointment.html")