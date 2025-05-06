from typing import Optional
from datetime import datetime, timedelta
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


# -----------------------------
# User Model
# -----------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[Optional[int]] = so.mapped_column(unique=True, nullable=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10))
    registered: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    group_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('groups.id'), index=True)
    group: so.Mapped[Optional['Group']] = so.relationship(back_populates='users')

    my_message: so.Mapped[list['Message']] = so.relationship(back_populates='user', cascade='all, delete-orphan')
    student_profile: so.Mapped[Optional['Student']] = so.relationship(back_populates='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'group_id': self.group_id
        }

    def __repr__(self):
        pwh = 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# -----------------------------
# Group Model
# -----------------------------
class Group(db.Model):
    __tablename__ = 'groups'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    users: so.Mapped[list['User']] = so.relationship(back_populates='group', cascade='all, delete-orphan')
    taskstatus: so.Mapped[list['GroupTaskStatus']] = so.relationship(back_populates='group', cascade='all, delete-orphan')
    message: so.Mapped[list['Message']] = so.relationship(back_populates='group', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'users': [user.to_dict() for user in self.users],
            'taskstatus': [status.to_dict() for status in self.taskstatus]
        }


# -----------------------------
# Task Model
# -----------------------------
class Task(db.Model):
    __tablename__ = 'tasks'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[str] = so.mapped_column(sa.String(1024))
    isUpload: so.Mapped[bool] = so.mapped_column(default=False)
    start_datetime: so.Mapped[datetime] = so.mapped_column(sa.DateTime())
    end_datetime: so.Mapped[datetime] = so.mapped_column(sa.DateTime())
    location: so.Mapped[str] = so.mapped_column(sa.String(128))

    groupstatus: so.Mapped[list['GroupTaskStatus']] = so.relationship(back_populates='task', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'isUpload': self.isUpload,
            'groupstatus': [status.to_dict() for status in self.groupstatus],
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'location': self.location
        }


# -----------------------------
# GroupTaskStatus Model
# -----------------------------
class GroupTaskStatus(db.Model):
    __tablename__ = 'groupTaskStatuses'

    status: so.Mapped[str] = so.mapped_column(sa.String(32), default="Inactive")

    group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('groups.id'), primary_key=True)
    group: so.Mapped['Group'] = so.relationship(back_populates='taskstatus')

    task_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('tasks.id'), primary_key=True)
    task: so.Mapped['Task'] = so.relationship(back_populates='groupstatus')

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'task_id': self.task_id,
            'status': self.status,
            'task': self.task.to_dict() if self.task else None
        }


# -----------------------------
# Message Model
# -----------------------------
class Message(db.Model):
    __tablename__ = 'messages'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sent_time: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), index=True, default=datetime.utcnow)
    content: so.Mapped[str] = so.mapped_column(sa.String(1024))

    group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('groups.id'), index=True)
    group: so.Mapped['Group'] = so.relationship(back_populates='message')

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    user: so.Mapped['User'] = so.relationship(back_populates='my_message')

    def to_dict(self):
        return {
            'id': self.id,
            'sent_time': self.sent_time,
            'content': self.content,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'username': self.user.username
        }


# -----------------------------
# UniSupport Models
# -----------------------------

class Student(db.Model):
    __tablename__ = 'students'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    
    user: so.Mapped['User'] = so.relationship(back_populates='student_profile')
    mood_history: so.Mapped[list['MoodEntry']] = so.relationship(back_populates='student', cascade='all, delete-orphan')
    appointments: so.Mapped[list['Appointment']] = so.relationship(back_populates='student', cascade='all, delete-orphan')

    def log_mood(self, score):
        if not 1 <= score <= 5:
            raise ValueError("Mood score must be between 1 and 5")
        entry = MoodEntry(student=self, score=score)
        db.session.add(entry)
        return entry

    def get_mood_history(self):
        return self.mood_history

    def book_appointment(self, service_type, date):
        if date < datetime.now():
            raise ValueError("Cannot book appointment in the past")
        
        appointment = Appointment(
            student=self,
            service_type=service_type,
            date=date,
            status='scheduled'
        )
        db.session.add(appointment)
        return appointment

    def get_appointments(self):
        return self.appointments


class MoodEntry(db.Model):
    __tablename__ = 'mood_entries'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('students.id'))
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.utcnow)
    score: so.Mapped[int] = so.mapped_column(sa.Integer)

    student: so.Mapped['Student'] = so.relationship(back_populates='mood_history')


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('students.id'))
    service_type: so.Mapped[str] = so.mapped_column(sa.String(64))
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime())
    status: so.Mapped[str] = so.mapped_column(sa.String(32), default='scheduled')

    student: so.Mapped['Student'] = so.relationship(back_populates='appointments')


class SupportService(db.Model):
    __tablename__ = 'support_services'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    service_type: so.Mapped[str] = so.mapped_column(sa.String(64))
    available_slots: so.Mapped[list['AppointmentSlot']] = so.relationship(back_populates='service', cascade='all, delete-orphan')

    def generate_available_slots(self):
        slots = []
        current_date = datetime.now()
        for _ in range(14):  # Generate slots for next 14 days
            current_date += timedelta(days=1)
            if current_date.weekday() < 5:  # Only weekdays
                for hour in range(9, 17):  # 9 AM to 5 PM
                    slot = AppointmentSlot(
                        service=self,
                        date=current_date.replace(hour=hour, minute=0)
                    )
                    slots.append(slot)
        return slots


class AppointmentSlot(db.Model):
    __tablename__ = 'appointment_slots'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    service_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('support_services.id'))
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime())
    is_available: so.Mapped[bool] = so.mapped_column(default=True)

    service: so.Mapped['SupportService'] = so.relationship(back_populates='available_slots')
