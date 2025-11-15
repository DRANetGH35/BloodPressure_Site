from sqlalchemy import select
from wtforms import FloatField
from wtforms.fields import PasswordField, SubmitField, StringField, IntegerField, TextAreaField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models import User


class BloodPressureForm(FlaskForm):
    systolic = IntegerField('Systolic', validators=[DataRequired()])
    diastolic = IntegerField('Diastolic', validators=[DataRequired()])
    pulse = IntegerField('Pulse', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ensure_integer(self, field):
        if field.data < 1 or field.data > 1000:
            raise ValidationError('Please enter a number between 0 and 1000')

class AddNewMedicationForm(FlaskForm):
    medication = StringField('Medication', validators=[DataRequired()])
    dose = FloatField('Dose', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    change_password = BooleanField('Change Password')
    submit = SubmitField('Login', render_kw={'class': 'btn custom-btn'})

    def __init__(self, stored_password=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stored_password = stored_password

class NewNoteForm(FlaskForm):
    subject = SelectField('Choose an option',
                       choices=[('Symptom', 'Symptom'), ('Concern', 'Concern'), ('Question', 'Question'), ('Other', 'Other')],
                       validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    is_admin = BooleanField('Admin')
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_username(self, field):
        if db.session.execute(select(User).where(User.name == field.data)).scalar_one_or_none():
            raise ValidationError('Username already exists')

    def validate_confirm_password(self, field):
        if not self.password.data == self.confirm_password.data:
            raise ValidationError('Passwords do not match')
