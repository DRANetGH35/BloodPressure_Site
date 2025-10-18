from datetime import datetime

from flask import render_template, request

from extensions import db
from forms import BloodPressureForm
from models import User, BloodPressure
from app import create_app

app = create_app()

@app.route('/')
def index():
    form = BloodPressureForm()
    return render_template('index.html', form=form)

@app.route('/submit', methods=['POST'])
def submit():
    form = BloodPressureForm()
    if form.validate_on_submit():
        systolic = request.form.get('systolic')
        diastolic = request.form.get('diastolic')
        pulse = request.form.get('pulse')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(systolic, diastolic, pulse, now)
        print(type(now))
        new_entry = BloodPressure(systolic=systolic,
                                  diastolic=diastolic,
                                  pulse=pulse,
                                  time=now)
        db.session.add(new_entry)
        db.session.commit()
        return render_template('success.html')
    return render_template('index.html', form=form, errors=form.errors)