from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    IntegerField, SelectField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length

import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    # Login via email (past bij jouw User model)
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])

    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=16, max=100)])
    gender = SelectField(
        "Gender",
        choices=[
            ("female", "Female"),
            ("male", "Male"),
            ("nonbinary", "Non-binary"),
            ("prefer_not_say", "Prefer not to say"),
        ],
        validators=[DataRequired()],
    )

    study = StringField("Program / Major", validators=[DataRequired(), Length(max=120)])
    faculty = SelectField(
        "Faculty",
        choices=[
            ("science", "Science"),
            ("engineering", "Engineering"),
            ("arts", "Arts & Humanities"),
            ("business", "Business"),
            ("health", "Health Sciences"),
            ("law", "Law"),
            ("education", "Education"),
        ],
        validators=[DataRequired()],
    )

    grad_year = IntegerField("Graduation Year", validators=[DataRequired(), NumberRange(min=2024, max=2035)])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Register")

    def validate_name(self, name):
        user = db.session.scalar(sa.select(User).where(User.name == name.data))
        if user is not None:
            raise ValidationError("Please use a different name.")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")