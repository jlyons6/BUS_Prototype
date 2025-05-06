from datetime import datetime, timedelta
import random

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.mood_history = []
        self.appointments = []

    def log_mood(self, score):
        if not 1 <= score <= 5:
            raise ValueError("Mood score must be between 1 and 5")
        self.mood_history.append({
            'date': datetime.now(),
            'score': score
        })

    def get_mood_history(self):
        return self.mood_history

    def book_appointment(self, service_type, date):
        if date < datetime.now():
            raise ValueError("Cannot book appointment in the past")
        
        appointment = {
            'id': len(self.appointments) + 1,
            'service_type': service_type,
            'date': date,
            'status': 'scheduled'
        }
        self.appointments.append(appointment)
        return appointment

    def get_appointments(self):
        return self.appointments

class SupportService:
    def __init__(self, service_id, name, service_type):
        self.service_id = service_id
        self.name = name
        self.service_type = service_type
        self.available_slots = self._generate_available_slots()

    def _generate_available_slots(self):
        slots = []
        current_date = datetime.now()
        for _ in range(14):  # Generate slots for next 14 days
            current_date += timedelta(days=1)
            if current_date.weekday() < 5:  # Only weekdays
                for hour in range(9, 17):  # 9 AM to 5 PM
                    slots.append(current_date.replace(hour=hour, minute=0))
        return slots

    def get_available_slots(self):
        return self.available_slots

    def book_slot(self, slot):
        if slot in self.available_slots:
            self.available_slots.remove(slot)
            return True
        return False
