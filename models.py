from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import datetime

from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

class BloodPressure(db.Model):
    __tablename__ = 'blood_pressure'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    systolic: Mapped[int] = mapped_column(Integer, nullable=False)
    diastolic: Mapped[int] = mapped_column(Integer, nullable=False)
    pulse: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[String] = mapped_column(String, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "systolic": self.systolic,
            "diastolic": self.diastolic,
            "pulse": self.pulse,
            "notes": self.notes,
            "created": self.created
        }
class Medication(db.Model):
    __tablename__ = "medication"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    medication: Mapped[String] = mapped_column(String, nullable=False)

class Note(db.Model):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)

class Category(db.Model):
    __tablename__ = "medication_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    medication_entries: Mapped[List["MedicationEntry"]] = relationship(back_populates="category")

class MedicationEntry(db.Model):
    __tablename__ = "medication_entry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[Category] = relationship("Category", back_populates="medication_entries")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('medication_category.id'))
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    dose_mg: Mapped[float] = mapped_column(Float, nullable=False)
