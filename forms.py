from wtforms.fields import PasswordField, SubmitField, StringField, IntegerField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash

class BloodPressureForm(FlaskForm):
    systolic = IntegerField('Systolic', validators=[DataRequired()])
    diastolic =IntegerField('Diastolic', validators=[DataRequired()])
    pulse = IntegerField('Pulse', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ensure_integer(self, field):
        if field.data < 1 or field.data > 1000:
            raise ValidationError('Please enter a number between 0 and 1000')
