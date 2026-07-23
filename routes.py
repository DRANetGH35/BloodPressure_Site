from datetime import datetime
import csv
from flask import abort, render_template, request, redirect, url_for, flash, send_file
from flask_login import current_user, login_user, logout_user, login_required
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from extensions import db
from forms import BloodPressureForm, AddNewMedicationForm, LoginForm, RegisterForm, NewNoteForm
from medication import MedsJSON
from models import User, BloodPressure, Medication, Note, MedicationEntry, Category
from app import create_app
from sqlalchemy import inspect, select
import pandas as pd


meds_json = MedsJSON(f"instance/medication.json")
app = create_app()

def db_to_excel():
    df = pd.read_sql(sql="blood_pressure", con=db.engine)
    df.to_excel(f'static/database.xlsx', index=False)


def user_exists(username):
    try:
        if db.session.execute(db.select(User).where(User.name == username)).scalar():
            return True
    except AttributeError:
        return False
    return False

def logged_in_as_admin():
    return current_user.is_authenticated and current_user.is_admin == True

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user is None:
            return abort(401)
        if not logged_in_as_admin():
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    form = BloodPressureForm()
    return render_template('index.html', form=form)

@app.route('/table')
@login_required
def table():
    table_data = db.session.query(BloodPressure).all()
    for entry in table_data:
        print(entry.systolic, entry.diastolic)
    return render_template('table.html', table=table_data)


@app.route('/download_table')
@login_required
def donwload_table():
    table_data = db.session.query(BloodPressure).all()
    path = "static/database.xlsx"
    db_to_excel()
    return send_file(path, as_attachment=True)
    

@app.route('/medication', methods=['GET', 'POST'])
@login_required
def medication():
    if request.method == "POST":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = Medication(time=now, medication=str(request.form.getlist('medication')))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('medication_table'))
    return render_template('medication.html', categories=db.session.execute(select(Category)).scalars().all(), medications=db.session.execute(select(MedicationEntry)).scalars().all())

@app.route("/medication_table")
@login_required
def medication_table():
    table_data = db.session.query(Medication).all()
    return render_template('medication_table.html', table_data=table_data)

@app.route("/add_new_medication/<category_id>", methods=['GET', 'POST'])
@login_required
def add_new_medication(category_id):
    form = AddNewMedicationForm()
    if request.method == "POST":
        med = request.form.get('medication')
        dose = request.form.get('dose')
        if form.validate_on_submit():
            new_med_entry = MedicationEntry(category_id=category_id, name=med, dose_mg=dose)
            db.session.add(new_med_entry)
            db.session.commit()
            return redirect(url_for('medication'))
    return render_template('/add_new_medication.html', form=form, errors=form.errors)

@app.route('/add_new_category', methods=['GET', 'POST'])
@login_required
def add_new_category():
    if request.method == 'POST':
        category_name = request.form.get('category')
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('medication'))
    return render_template('add_new_category.html')

@app.route('/delete_medication/<medication_id>', methods=['GET', 'POST'])
@login_required
def delete_medication(medication_id):
    medication_to_delete = db.session.execute(select(MedicationEntry).where(MedicationEntry.id == medication_id)).scalar()
    db.session.delete(medication_to_delete)
    db.session.commit()
    return redirect(url_for('medication'))

@app.route('/new_note', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template('new_note.html', errors=form.errors)
        subject = request.form.get('subject')
        content = request.form.get('content')
        new_note = Note(subject=subject, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('notes'))
    return render_template('new_note.html', form=form, errors=form.errors)

@app.route('/notes')
def notes():
    table_data = db.session.query(Note).all()
    return render_template('note_table.html', table_data=table_data)

@app.route("/delete_note/<note_id>")
def delete_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/submit', methods=['POST'])
@login_required
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
@admin_only
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

@app.route('/populate_created_values')
def populate_created_values():
    all_entries = db.session.query(BloodPressure).all()
    for entry in all_entries:
        entry.created = datetime.strptime(entry.time, '%Y-%m-%d %H:%M:%S')
        db.session.commit()
    return redirect(url_for('table'))

@app.route('/populate_created_meds')
def populate_created_meds():
    all_entries = db.session.query(Medication).all()
    for entry in all_entries:
        entry.created = datetime.strptime(entry.time, '%Y-%m-%d %H:%M:%S')
        db.session.commit()
    return redirect(url_for('medication_table'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(401)
def unauthorized(e):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403