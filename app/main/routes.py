from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

from app import db
from app.models import User, Student, SupportService
from app.forms import LoginForm, RegisterForm, MoodLogForm, AppointmentForm
from app.main import bp

# Temporary storage (will be replaced with database)
support_services = [
    SupportService("Counselling Service", "counselling"),
    SupportService("Academic Support", "academic"),
    SupportService("Wellbeing Workshop", "workshop")
]

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html', title='Dashboard', user=current_user)
    return render_template('index.html', title='Welcome to UniSupport')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            role='student'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard', user=current_user)

@bp.route('/mood/log', methods=['GET', 'POST'])
@login_required
def log_mood():
    if request.method == 'POST':
        try:
            score = int(request.form.get('score'))
            form = MoodLogForm(score)
            
            if form.validate():
                # Create or get student record
                student = Student.query.filter_by(user_id=current_user.id).first()
                if not student:
                    student = Student(user_id=current_user.id, name=current_user.username)
                    db.session.add(student)
                
                student.log_mood(score)
                db.session.commit()
                flash('Mood logged successfully!', 'success')
            else:
                for error in form.errors:
                    flash(error, 'error')
        except ValueError:
            flash('Please enter a valid number', 'error')
        
        return redirect(url_for('main.dashboard'))
    
    return render_template('log_mood.html', title='Log Mood')

@bp.route('/appointments/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == 'POST':
        try:
            service_type = request.form.get('service_type')
            date_str = request.form.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            
            form = AppointmentForm(service_type, date)
            
            if form.validate():
                student = Student.query.filter_by(user_id=current_user.id).first()
                if not student:
                    student = Student(user_id=current_user.id, name=current_user.username)
                    db.session.add(student)
                
                appointment = student.book_appointment(service_type, date)
                db.session.commit()
                flash('Appointment booked successfully!', 'success')
            else:
                for error in form.errors:
                    flash(error, 'error')
        except ValueError:
            flash('Invalid date format', 'error')
        
        return redirect(url_for('main.dashboard'))
    
    return render_template('book_appointment.html', title='Book Appointment', services=support_services)

@bp.route('/mood/history')
@login_required
def mood_history():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if student:
        history = student.get_mood_history()
        return render_template('mood_history.html', title='Mood History', history=history)
    flash('No mood history available', 'info')
    return redirect(url_for('main.dashboard'))

@bp.route('/appointments')
@login_required
def appointments():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if student:
        appointments = student.get_appointments()
        return render_template('appointments.html', title='Appointments', appointments=appointments)
    flash('No appointments found', 'info')
    return redirect(url_for('main.dashboard'))

@bp.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='404'), 404

@bp.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='500'), 500 