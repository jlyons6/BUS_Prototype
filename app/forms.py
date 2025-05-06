from datetime import datetime
from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class MoodLogForm(FlaskForm):
    score = RadioField('Mood Score', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Length(max=500)])
    activities = SelectField('Activities', choices=[
        ('study', 'Studying'),
        ('social', 'Social Activities'),
        ('exercise', 'Exercise'),
        ('rest', 'Rest/Relaxation'),
        ('other', 'Other')
    ])
    submit = SubmitField('Save Mood Entry')

class AppointmentForm(FlaskForm):
    service_type = SelectField('Service Type', validators=[DataRequired()])
    date = StringField('Date and Time', validators=[DataRequired()])
    notes = TextAreaField('Additional Notes', validators=[Length(max=500)])
    submit = SubmitField('Book Appointment')
