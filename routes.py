from datetime import datetime
import csv
import random
from flask import abort, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from extensions import db, send_reset_link, send_verification_email
from forms import BloodPressureForm, LoginForm, RegisterForm, NewNoteForm
from medication import MedsJSON
from models import User, BloodPressure, Medication, Note, MedicationEntry, Category
from app import create_app
from sqlalchemy import inspect, select
import pandas as pd
from dateutil import parser, tz
from dateutil.tz import gettz
tz_mapping = {
        # --- NORTH AMERICA (US & CANADA) ---
        "EST": gettz("America/New_York"),  # Eastern Standard Time (UTC-5)
        "EDT": gettz("America/New_York"),  # Eastern Daylight Time (UTC-4)
        "CST": gettz("America/Chicago"),  # Central Standard Time (UTC-6)
        "CDT": gettz("America/Chicago"),  # Central Daylight Time (UTC-5)
        "MST": gettz("America/Denver"),  # Mountain Standard Time (UTC-7)
        "MDT": gettz("America/Denver"),  # Mountain Daylight Time (UTC-6)
        "PST": gettz("America/Los_Angeles"),  # Pacific Standard Time (UTC-8)
        "PDT": gettz("America/Los_Angeles"),  # Pacific Daylight Time (UTC-7)
        "AKST": gettz("America/Anchorage"),  # Alaska Standard Time (UTC-9)
        "AKDT": gettz("America/Anchorage"),  # Alaska Daylight Time (UTC-8)
        "HST": gettz("Pacific/Honolulu"),  # Hawaii Standard Time (UTC-10)

        # --- EUROPE ---
        "GMT": gettz("Europe/London"),  # Greenwich Mean Time (UTC+0)
        "BST": gettz("Europe/London"),  # British Summer Time (UTC+1)
        "WET": gettz("Europe/Lisbon"),  # Western European Time (UTC+0)
        "WEST": gettz("Europe/Lisbon"),  # Western European Summer Time (UTC+1)
        "CET": gettz("Europe/Paris"),  # Central European Time (UTC+1)
        "CEST": gettz("Europe/Paris"),  # Central European Summer Time (UTC+2)
        "EET": gettz("Europe/Bucharest"),  # Eastern European Time (UTC+2)
        "EEST": gettz("Europe/Bucharest"),  # Eastern European Summer Time (UTC+3)
        "MSK": gettz("Europe/Moscow"),  # Moscow Time (UTC+3)

        # --- ASIA ---
        "IST": gettz("Asia/Kolkata"),  # India Standard Time (UTC+5:30) *AMBIGUOUS*
        "PKT": gettz("Asia/Karachi"),  # Pakistan Standard Time (UTC+5)
        "BTT": gettz("Asia/Thimphu"),  # Bhutan Time (UTC+6)
        "WIB": gettz("Asia/Jakarta"),  # Western Indonesian Time (UTC+7)
        "ICT": gettz("Asia/Bangkok"),  # Indochina Time (UTC+7)
        "SGT": gettz("Asia/Singapore"),  # Singapore Standard Time (UTC+8)
        "CST_CHINA": gettz("Asia/Shanghai"),  # China Standard Time (UTC+8) *Conflicts with US CST*
        "JST": gettz("Asia/Tokyo"),  # Japan Standard Time (UTC+9)
        "KST": gettz("Asia/Seoul"),  # Korea Standard Time (UTC+9)

        # --- AUSTRALIA ---
        "AWST": gettz("Australia/Perth"),  # Australian Western Standard Time (UTC+8)
        "ACST": gettz("Australia/Adelaide"),  # Australian Central Standard Time (UTC+9:30)
        "ACDT": gettz("Australia/Adelaide"),  # Australian Central Daylight Time (UTC+10:30)
        "AEST": gettz("Australia/Sydney"),  # Australian Eastern Standard Time (UTC+10)
        "AEDT": gettz("Australia/Sydney"),  # Australian Eastern Daylight Time (UTC+11)

        # --- SOUTH AMERICA & ATLANTIC ---
        "BRT": gettz("America/Sao_Paulo"),  # Brasilia Time (UTC-3)
        "BRST": gettz("America/Sao_Paulo"),  # Brasilia Summer Time (UTC-2)
        "ART": gettz("America/Argentina/Buenos_Aires"),  # Argentina Time (UTC-3)
        "CLT": gettz("America/Santiago"),  # Chile Standard Time (UTC-4)
        "CLST": gettz("America/Santiago"),  # Chile Summer Time (UTC-3)

        # --- AFRICA ---
        "WAT": gettz("Africa/Lagos"),  # West Africa Time (UTC+1)
        "CAT": gettz("Africa/Maputo"),  # Central Africa Time (UTC+2)
        "EAT": gettz("Africa/Nairobi"),  # East Africa Time (UTC+3)
        "SAST": gettz("Africa/Johannesburg"),  # South Africa Standard Time (UTC+2)
    }
meds_json = MedsJSON(f"instance/medication.json")
app = create_app()

def db_to_excel():
    df = pd.read_sql(sql="blood_pressure", con=db.engine)
    df.to_excel(f'static/database.xlsx', index=False)




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
    return render_template('index.html')

@app.route('/admin_panel')
@admin_only
def admin_panel():
    return render_template('admin/panel.html')

@app.route('/admin/users')
@admin_only
def admin_users():
    return render_template('admin/users.html')

@app.route('/admin/login_as/<int:user_id>')
@admin_only
def login_as(user_id):
    user_to_login = db.session.execute(select(User).where(User.id == user_id)).scalar()
    login_user(user_to_login)
    return redirect(url_for('index'))

@app.route('/table')
@login_required
def table():
    page = 1
    per_page = 25
    return render_template('table.html')

@app.route('/graph_table')
def graph_table():
    table_data = BloodPressure.query.order_by(BloodPressure.created.desc()).all()
    labels = [entry.created for entry in table_data]
    systolic = [entry.systolic for entry in table_data]
    diastolic = [entry.diastolic for entry in table_data]
    pulse = [entry.pulse for entry in table_data]
    return render_template('graph_table.html', labes=labels, systolic=systolic, diastolic=diastolic, pulse=pulse)

@app.route('/admin/fetch_users/<int:page>')
@admin_only
def admin_fetch_users(page):
    per_page = 25
    table_data = User.query.order_by(User.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    results = [{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'verification_code': user.verification_code,
        'verified': user.verified,
        'is_admin': user.is_admin
    } for user in table_data]
    return jsonify({"data": results})


@app.route('/fetch_table_data/<int:page>')
def fetch_table_data(page):
    per_page = 25
    table_data = BloodPressure.query.filter_by(user_id=current_user.id).order_by(BloodPressure.created.desc()).paginate(page=page, per_page=per_page, error_out=False)
    results = [{'id': entry.id,
               'created': entry.created,
               'systolic': entry.systolic,
               'diastolic': entry.diastolic,
               'pulse': entry.pulse,
               'notes': entry.notes} for entry in table_data]
    return jsonify({"data": results})

@app.route('/fetch_medication_table_data/<int:page>')
def fetch_medication_table_data(page):
    per_page = 25
    table_data = Medication.query.filter_by(user_id=current_user.id).order_by(Medication.created.desc()).paginate(page=page, per_page=per_page, error_out=False)
    results = [{'id': entry.id,
                'created': entry.created,
                'medication': entry.medication} for entry in table_data]
    return jsonify({"data": results})
@app.route('/fetch_medication_entries/')
def fetch_medication_entries():
    medications = db.session.execute(select(MedicationEntry).where(MedicationEntry.user_id == current_user.id)).scalars()
    medications = [{'id': med.id,
                   'category': med.category.name,
                   'name': med.name,
                   'dose_mg': med.dose_mg} for med in medications]
    categories = db.session.execute(select(Category).where(Category.user_id == current_user.id)).scalars()
    categories = [{"id": cat.id,
                   'user_id': cat.user_id,
                   'name': cat.name} for cat in categories]
    data = {'medications': medications,
            'categories': categories}
    return jsonify(data)

@app.route('/fetch_graph_data')
def fetch_graph_data():
    window = 30
    table_data = BloodPressure.query.order_by(BloodPressure.created.asc()).all()
    return jsonify([bloodpressure.to_dict() for bloodpressure in table_data])

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
        now = parser.parse(request.form.get('time'), tzinfos=tz_mapping).astimezone(tz.tzutc())
        new_entry = Medication(user=current_user,
                               user_id=current_user.id,
                               created=now,
                               medication=str(request.form.getlist('medication')))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('medication_table'))
    return render_template('medication.html', medications=db.session.execute(select(MedicationEntry).where(MedicationEntry.user_id==current_user.id)).scalars())

@app.route("/medication_table")
@login_required
def medication_table():
    table_data = db.session.query(Medication).all()
    return render_template('medication_table.html', table_data=table_data)

@app.route("/add_new_medication/<category_id>", methods=['GET', 'POST'])
@login_required
def add_new_medication(category_id):
    if request.method == "POST":
        med = request.form.get('medication')
        dose = request.form.get('dose')
        new_med_entry = MedicationEntry(user_id=current_user.id, category_id=category_id, name=med, dose_mg=dose)
        db.session.add(new_med_entry)
        db.session.commit()
        return redirect(url_for('medication'))
    return render_template('/add_new_medication.html')

@app.route('/add_new_category', methods=['GET', 'POST'])
@login_required
def add_new_category():
    if request.method == 'POST':
        category_name = request.form.get('category')
        new_category = Category(name=category_name, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('medication'))
    return render_template('add_new_category.html')

@app.route('/delete_medication_entry/<int:medication_entry_id>')
@login_required
def delete_medication_entry(medication_entry_id):
    medication_entry_to_delete = db.session.execute(select(Medication).where(Medication.id == medication_entry_id)).scalar()
    db.session.delete(medication_entry_to_delete)
    db.session.commit()
    return redirect(url_for('medication_table'))
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
    systolic = request.form.get('systolic')
    diastolic = request.form.get('diastolic')
    pulse = request.form.get('pulse')
    notes = request.form.get('notes')
    now = parser.parse(request.form.get('time'), tzinfos=tz_mapping).astimezone(tz.tzutc())
    new_entry = BloodPressure(user=current_user,
                              user_id=current_user.id,
                              systolic=systolic,
                              diastolic=diastolic,
                              pulse=pulse,
                              created=now,
                              notes=notes)
    db.session.add(new_entry)
    db.session.commit()
    return render_template('success.html')

@app.route('/delete_bloodpressure/<int:id>')
def delete_bloodpressure(id):
    entry = db.session.execute(select(BloodPressure).where(BloodPressure.id == id)).scalar()
    db.session.delete(entry)
    db.session.commit()
    return redirect(request.referrer)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        if not User.exists(username=request.form.get('username')):
            return render_template('login.html', error='Incorrect username or password')
        password_matches = User.check_password(username=request.form.get('username'), password=request.form.get('password'))
        if not password_matches:
            return render_template('login.html', error='Incorrect username or password')
        user = db.session.execute(db.select(User).where(User.name == request.form.get('username'))).scalar()
        login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', current_user=current_user, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = str(request.form.get('username'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        verification_code = f"{random.randint(0, 99999):05}"
        if User.exists_by_email(email):
            return render_template('account/register.html', error="Account already exists with that email")
        if User.exists(username):
            return render_template('account/register.html', error="Username taken")
        new_user = User(name=username,
                        email=email,
                        password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8),
                        is_admin=False,
                        verified=False,
                        verification_code=verification_code
                        )
        db.session.add(new_user)
        db.session.commit()
        send_verification_email(verification_code, email)
        login_user(new_user, remember=True)
        return redirect(url_for('index'))
    return render_template('register.html', current_user=current_user)

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