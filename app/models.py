from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

session_participants = db.Table(
    "session_participants",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("session_id", db.Integer, db.ForeignKey("session.id"), primary_key=True),
)

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    age = db.Column(db.Integer)
    gender = db.Column(db.String(30))
    study = db.Column(db.String(120))
    faculty = db.Column(db.String(120))
    grad_year = db.Column(db.Integer)

    disabled = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


    created_sessions = db.relationship("Session", back_populates="created_by", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subject = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    starts_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    location = db.Column(db.String(200), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_by = db.relationship("User", back_populates="created_sessions")

    participants = db.relationship("User", secondary=session_participants, backref="joined_sessions")
