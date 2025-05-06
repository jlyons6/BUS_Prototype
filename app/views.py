from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import User, SupportRequest, Message
from app.forms import LoginForm, RegisterForm, SupportRequestForm
import sqlalchemy as sa


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
