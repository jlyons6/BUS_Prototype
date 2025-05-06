from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from datetime import datetime

from app import app, db
from app.models import User, SupportRequest, Message, Student, SupportService
from app.forms import LoginForm, RegisterForm, SupportRequestForm, MoodLogForm, AppointmentForm
import sqlalchemy as sa

# Create a Blueprint for our views
main = Blueprint('main', __name__)

# Temporary storage (will be replaced with database)
students = {}
support_services = [
    SupportService(1, "Counselling Service", "counselling"),
    SupportService(2, "Academic Support", "academic"),
    SupportService(3, "Wellbeing Workshop", "workshop")
]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        
        if not student_id or not name:
            flash('Please provide both student ID and name', 'error')
            return redirect(url_for('main.login'))
        
        # Create or retrieve student
        if student_id not in students:
            students[student_id] = Student(student_id, name)
        
        # In a real app, we'd use session management here
        return redirect(url_for('main.dashboard'))
    
    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    # In a real app, we'd get the current user from the session
    return render_template('dashboard.html')

@main.route('/mood/log', methods=['GET', 'POST'])
def log_mood():
    if request.method == 'POST':
        try:
            score = int(request.form.get('score'))
            form = MoodLogForm(score)
            
            if form.validate():
                # In a real app, we'd get the current user from the session
                student_id = request.form.get('student_id')
                if student_id in students:
                    students[student_id].log_mood(score)
                    flash('Mood logged successfully!', 'success')
                else:
                    flash('Student not found', 'error')
            else:
                for error in form.errors:
                    flash(error, 'error')
        except ValueError:
            flash('Please enter a valid number', 'error')
        
        return redirect(url_for('main.dashboard'))
    
    return render_template('log_mood.html')

@main.route('/appointments/book', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        try:
            service_type = request.form.get('service_type')
            date_str = request.form.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            
            form = AppointmentForm(service_type, date)
            
            if form.validate():
                # In a real app, we'd get the current user from the session
                student_id = request.form.get('student_id')
                if student_id in students:
                    appointment = students[student_id].book_appointment(service_type, date)
                    flash('Appointment booked successfully!', 'success')
                else:
                    flash('Student not found', 'error')
            else:
                for error in form.errors:
                    flash(error, 'error')
        except ValueError:
            flash('Invalid date format', 'error')
        
        return redirect(url_for('main.dashboard'))
    
    return render_template('book_appointment.html', services=support_services)

@main.route('/mood/history')
def mood_history():
    # In a real app, we'd get the current user from the session
    student_id = request.args.get('student_id')
    if student_id in students:
        history = students[student_id].get_mood_history()
        return render_template('mood_history.html', history=history)
    flash('Student not found', 'error')
    return redirect(url_for('main.dashboard'))

@main.route('/appointments')
def appointments():
    # In a real app, we'd get the current user from the session
    student_id = request.args.get('student_id')
    if student_id in students:
        appointments = students[student_id].get_appointments()
        return render_template('appointments.html', appointments=appointments)
    flash('Student not found', 'error')
    return redirect(url_for('main.dashboard'))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('dashboard.html', title='Dashboard', user=current_user)
    return render_template('home.html', title='Welcome to UniSupport')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
        user = User(
            email=form.email.data,
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/request_support', methods=['GET', 'POST'])
@login_required
def request_support():
    form = SupportRequestForm()
    if form.validate_on_submit():
        support_request = SupportRequest(
            user_id=current_user.id,
            subject=form.subject.data,
            description=form.description.data,
            status='Pending'
        )
        db.session.add(support_request)
        db.session.commit()
        flash('Support request submitted.', 'success')
        return redirect(url_for('home'))
    return render_template('support_request.html', title='Request Support', form=form)


@app.route('/messages', methods=['GET'])
@login_required
def messages():
    messages = db.session.scalars(
        sa.select(Message).where(Message.user_id == current_user.id).order_by(Message.sent_time.desc())
    ).all()
    return render_template('messages.html', title='Messages', messages=messages)


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='404'), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='500'), 500
