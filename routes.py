from datetime import datetime

from flask import render_template, request

from extensions import db
from forms import BloodPressureForm, NoteForm
from models import User, BloodPressure, Notes
from app import create_app

app = create_app()

@app.route('/')
def index():
    form = BloodPressureForm()
    return render_template('index.html', form=form)

@app.route('/notes', methods=['GET', 'POST'])
def notes_route():
    form = NoteForm()
    table_data = db.session.query(Notes).all()
    if request.method == "GET":
        return render_template('notes.html', table=table_data, form=form)
    else:   #POST
        if form.validate_on_submit():
            type = request.form.get('type')
            note = request.form.get('note')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = Notes(time=now,
                              type=type,
                              note=note)
            print(new_entry)
            db.session.add(new_entry)
            db.session.commit()
        else:
            print(form.errors)
            print("Failed to validate")
        return render_template('notes.html', table=table_data, form=form)

@app.route('/table')
def table():
    table_data = db.session.query(BloodPressure).all()
    for entry in table_data:
        print(entry.systolic, entry.diastolic)
    return render_template('table.html', table=table_data)

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

