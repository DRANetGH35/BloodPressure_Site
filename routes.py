from datetime import datetime
import csv
from flask import render_template, request

from extensions import db
from forms import BloodPressureForm
from models import User, BloodPressure, Medication
from app import create_app


app = create_app()

@app.route('/')
def index():
    form = BloodPressureForm()
    return render_template('index.html', form=form)

@app.route('/table')
def table():
    table_data = db.session.query(BloodPressure).all()
    for entry in table_data:
        print(entry.systolic, entry.diastolic)
    return render_template('table.html', table=table_data)

@app.route('/medication', methods=['GET', 'POST'])
def medication():
    medications = []
    with open('instance/medication.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            medications.append(row[0])
    if request.method == "POST":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        med_list = [med for med in medications if request.form.get(med)]  #appends med to medlists as long as it has been selected in the form
        new_entry = Medication(time=now, medication=str(med_list))
        db.session.add(new_entry)
        db.session.commit()
    return render_template('medication.html', medications=medications)

@app.route('/submit', methods=['POST'])
def submit():
    form = BloodPressureForm()
    if form.validate_on_submit():
        systolic = request.form.get('systolic')
        diastolic = request.form.get('diastolic')
        pulse = request.form.get('pulse')
        notes = request.form.get('notes')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(systolic, diastolic, pulse, now)
        print(type(now))
        new_entry = BloodPressure(systolic=systolic,
                                  diastolic=diastolic,
                                  pulse=pulse,
                                  time=now,
                                  notes=notes)
        db.session.add(new_entry)
        db.session.commit()
        return render_template('success.html')
    return render_template('index.html', form=form, errors=form.errors)

