from datetime import datetime
from typing import Optional

class MoodLogForm:
    def __init__(self, score: int):
        self.score = score
        self.errors = []

    def validate(self) -> bool:
        if not isinstance(self.score, int):
            self.errors.append("Score must be an integer")
            return False
        
        if not 1 <= self.score <= 5:
            self.errors.append("Score must be between 1 and 5")
            return False
        
        return True

class AppointmentForm:
    def __init__(self, service_type: str, date: datetime):
        self.service_type = service_type
        self.date = date
        self.errors = []

    def validate(self) -> bool:
        if not isinstance(self.service_type, str):
            self.errors.append("Service type must be a string")
            return False
        
        if not self.service_type:
            self.errors.append("Service type cannot be empty")
            return False
        
        if not isinstance(self.date, datetime):
            self.errors.append("Date must be a datetime object")
            return False
        
        if self.date < datetime.now():
            self.errors.append("Cannot book appointment in the past")
            return False
        
        if self.date.weekday() >= 5:  # Saturday or Sunday
            self.errors.append("Appointments are only available on weekdays")
            return False
        
        if not 9 <= self.date.hour < 17:
            self.errors.append("Appointments are only available between 9 AM and 5 PM")
            return False
        
        return True
