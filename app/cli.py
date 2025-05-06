from datetime import datetime
import sys
from models import Student, SupportService
from forms import MoodLogForm, AppointmentForm

class UniSupportCLI:
    def __init__(self):
        self.current_student = None
        self.support_services = [
            SupportService(1, "Counselling Service", "counselling"),
            SupportService(2, "Academic Support", "academic"),
            SupportService(3, "Wellbeing Workshop", "workshop")
        ]

    def start(self):
        print("Welcome to UniSupport - Student Wellbeing Platform")
        print("================================================")
        
        while True:
            if not self.current_student:
                self._handle_login()
            else:
                self._show_main_menu()

    def _handle_login(self):
        print("\nPlease log in:")
        student_id = input("Student ID: ")
        name = input("Name: ")
        self.current_student = Student(student_id, name)
        print(f"\nWelcome, {name}!")

    def _show_main_menu(self):
        print("\nMain Menu:")
        print("1. Log Mood")
        print("2. Book Appointment")
        print("3. View Mood History")
        print("4. View Appointments")
        print("5. Logout")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            self._handle_mood_log()
        elif choice == "2":
            self._handle_appointment_booking()
        elif choice == "3":
            self._show_mood_history()
        elif choice == "4":
            self._show_appointments()
        elif choice == "5":
            self.current_student = None
            print("\nLogged out successfully.")
        elif choice == "6":
            print("\nThank you for using UniSupport. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")

    def _handle_mood_log(self):
        print("\nLog Your Mood (1-5):")
        print("1 - Very Low")
        print("2 - Low")
        print("3 - Neutral")
        print("4 - Good")
        print("5 - Very Good")
        
        try:
            score = int(input("\nEnter your mood score (1-5): "))
            form = MoodLogForm(score)
            
            if form.validate():
                self.current_student.log_mood(score)
                print("\nMood logged successfully!")
            else:
                print("\nValidation errors:")
                for error in form.errors:
                    print(f"- {error}")
        except ValueError:
            print("\nPlease enter a valid number.")

    def _handle_appointment_booking(self):
        print("\nAvailable Services:")
        for i, service in enumerate(self.support_services, 1):
            print(f"{i}. {service.name}")

        try:
            service_choice = int(input("\nSelect a service (1-3): ")) - 1
            if not 0 <= service_choice < len(self.support_services):
                raise ValueError("Invalid service choice")

            service = self.support_services[service_choice]
            print("\nAvailable slots:")
            for i, slot in enumerate(service.get_available_slots(), 1):
                print(f"{i}. {slot.strftime('%Y-%m-%d %H:%M')}")

            slot_choice = int(input("\nSelect a slot (enter number): ")) - 1
            if not 0 <= slot_choice < len(service.get_available_slots()):
                raise ValueError("Invalid slot choice")

            selected_slot = service.get_available_slots()[slot_choice]
            form = AppointmentForm(service.service_type, selected_slot)

            if form.validate():
                appointment = self.current_student.book_appointment(
                    service.service_type,
                    selected_slot
                )
                service.book_slot(selected_slot)
                print("\nAppointment booked successfully!")
                print(f"Appointment ID: {appointment['id']}")
                print(f"Date: {appointment['date'].strftime('%Y-%m-%d %H:%M')}")
            else:
                print("\nValidation errors:")
                for error in form.errors:
                    print(f"- {error}")

        except ValueError as e:
            print(f"\nError: {str(e)}")

    def _show_mood_history(self):
        history = self.current_student.get_mood_history()
        if not history:
            print("\nNo mood history available.")
            return

        print("\nMood History:")
        print("Date\t\t\tScore")
        print("-" * 40)
        for entry in history:
            print(f"{entry['date'].strftime('%Y-%m-%d %H:%M')}\t{entry['score']}")

    def _show_appointments(self):
        appointments = self.current_student.get_appointments()
        if not appointments:
            print("\nNo appointments booked.")
            return

        print("\nYour Appointments:")
        print("ID\tDate\t\t\tService Type\tStatus")
        print("-" * 60)
        for apt in appointments:
            print(f"{apt['id']}\t{apt['date'].strftime('%Y-%m-%d %H:%M')}\t{apt['service_type']}\t\t{apt['status']}")

if __name__ == "__main__":
    cli = UniSupportCLI()
    cli.start() 