from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

class BloodPressure(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    systolic: Mapped[int] = mapped_column(Integer, nullable=False)
    diastolic: Mapped[int] = mapped_column(Integer, nullable=False)
    pulse: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[str] = mapped_column(String, nullable=False)
