from datetime import datetime
import csv
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import os
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from forms import BloodPressureForm, AddNewMedicationForm, LoginForm, RegisterForm
from models import User, BloodPressure, Medication
from app import create_app


app = create_app()

def user_exists(username):
    try:
        if db.session.execute(db.select(User).where(User.name == username)).scalar():
            return True
    except AttributeError:
        return False
    return False

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
    if not os.path.isfile('instance/medication.csv'):
        with open("instance/medication.csv", "w") as f:
            f.write('')
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

@app.route("/medication_table")
def medication_table():
    table_data = db.session.query(Medication).all()
    return render_template('medication_table.html', table_data=table_data)

@app.route("/add_new_medication", methods=['GET', 'POST'])
def add_new_medication():
    form = AddNewMedicationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            with open('instance/medication.csv', 'a') as fd:
                fd.write(f"{request.form.get('medication')}\n")
            return redirect(url_for('medication'))
    return render_template('/add_new_medication.html', form=form, errors=form.errors)

@app.route('/submit', methods=['POST'])
def submit():
    form = BloodPressureForm()
    if form.validate_on_submit():
        systolic = request.form.get('systolic')
        diastolic = request.form.get('diastolic')
        pulse = request.form.get('pulse')
        notes = request.form.get('notes')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = BloodPressure(systolic=systolic,
                                  diastolic=diastolic,
                                  pulse=pulse,
                                  time=now,
                                  notes=notes)
        db.session.add(new_entry)
        db.session.commit()
        return render_template('success.html')
    return render_template('index.html', form=form, errors=form.errors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form, errors=form.errors, current_user=current_user)
        user = db.session.execute(db.select(User).where(User.name == form.username.data)).scalar()
        # if user does not exist or password is incorrect
        if not user_exists(form.username.data) or not check_password_hash(user.password, form.password.data):
            flash('Incorrect username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', form=form, errors=form.errors, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('register.html', form=form, current_user=current_user, errors=form.errors)
        new_user = User(name=form.username.data,
                        password=generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8),
                        is_admin=form.is_admin.data)
        db.session.add(new_user)
        db.session.commit()
    return render_template('login.html', form=form, errors=form.errors, current_user=current_user)