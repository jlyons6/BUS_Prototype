import datetime
from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Task, Message, Group, GroupTaskStatus, Student, SupportService, AppointmentSlot


def reset_db():
    """Reset the database by dropping and recreating all tables."""
    db.drop_all()
    db.create_all()
    print("Database reset complete.")


def generate_users():
    """Generate and return a list of user objects."""
    users = [
        User(username='John Doe', student_id=1, email='john.doe@student.bham.ac.uk', role='Admin',
             password_hash=generate_password_hash('admin.pw'), registered=True),
        User(username='Alice Green', student_id=1111111, email='alicegreen@student.bham.ac.uk', role='Student',
             password_hash=generate_password_hash('AliceGreen1234!'), registered=True),
        User(username='Robert Brown', student_id=2222222, email='robertbrown@student.bham.ac.uk', role='Student',
             registered=False),
        User(username='Mia Clarke', student_id=3333333, email='miaclarke@student.bham.ac.uk', role='Admin',
             password_hash=generate_password_hash('MiaClarke1234!'), registered=True),
        User(username='Ethan James', student_id=4444444, email='ethanjames@student.bham.ac.uk', role='Student',
             registered=False),
        User(username='Sophia Taylor', student_id=5555555, email='sophiataylor@bstudent.bham.ac.uk', role='Mentor',
             password_hash=generate_password_hash('SophiaTaylor1234!'), registered=True),
        User(username='Liam Scott', student_id=6666666, email='liamscott@student.bham.ac.uk', role='Admin',
             password_hash=generate_password_hash('LiamScott1234!'), registered=True),
        User(username='Olivia White', student_id=7777777, email='oliviawhite@student.bham.ac.uk', role='Student',
             registered=False),
        User(username='James Black', student_id=8888888, email='jamesblack@student.bham.ac.uk', role='Admin',
             password_hash=generate_password_hash('JamesBlack1234!'), registered=True),
        User(username='Emma Gray', student_id=2000000, email='emmagray@b.com', role='Student',
             password_hash=generate_password_hash('EmmaGray1234!'), registered=True),
        User(username='Lucas King', student_id=3000000, email='lucasking@b.com', role='Mentor',
             password_hash=generate_password_hash('LucasKing1234!'), registered=True),
        User(username='Sophia Adams', student_id=9999999, email='sophiaadams@student.bham.ac.uk', role='Student',
             registered=False),
        User(username='Zoe Williams', student_id=1000000, email='zoewilliams@student.bham.ac.uk', role='Mentor',
             password_hash=generate_password_hash('ZoeWilliams1234!'), registered=True)
    ]
    return users


def generate_tasks():
    """Generate and return a list of task objects."""
    tasks = [
        Task(title="Study Group Meetup", description="Gather with fellow students for a study session", isUpload=True,
             start_datetime=datetime.datetime.now() + datetime.timedelta(minutes=10),
             end_datetime=datetime.datetime.now() + datetime.timedelta(minutes=30), location="Library Room 1"),
        Task(title="Campus Tour", description="Take a tour around the university campus", isUpload=True,
             start_datetime=datetime.datetime.now() + datetime.timedelta(days=1),
             end_datetime=datetime.datetime.now() + datetime.timedelta(days=1, hours=2), location="Main Entrance"),
        Task(title="Volunteer Event", description="Volunteer at a local community center", isUpload=False,
             start_datetime=datetime.datetime.now() + datetime.timedelta(weeks=1),
             end_datetime=datetime.datetime.now() + datetime.timedelta(weeks=1, hours=4), location="Community Center"),
    ]
    return tasks


def generate_support_services():
    """Generate and return a list of support service objects."""
    services = [
        SupportService("Counselling Service", "counselling"),
        SupportService("Academic Support", "academic"),
        SupportService("Wellbeing Workshop", "workshop"),
        SupportService("Mental Health Support", "mental_health"),
        SupportService("Career Guidance", "career")
    ]
    return services


def generate_students(users):
    """Generate student profiles for users with student role."""
    students = []
    for user in users:
        if user.role == 'Student':
            student = Student(user_id=user.id, name=user.username)
            students.append(student)
    return students


def generate_appointment_slots(services):
    """Generate appointment slots for each service."""
    slots = []
    for service in services:
        current_date = datetime.datetime.now()
        for _ in range(14):  # Generate slots for next 14 days
            current_date += datetime.timedelta(days=1)
            if current_date.weekday() < 5:  # Only weekdays
                for hour in range(9, 17):  # 9 AM to 5 PM
                    slot = AppointmentSlot(
                        service=service,
                        date=current_date.replace(hour=hour, minute=0)
                    )
                    slots.append(slot)
    return slots


def generate_group_task_status():
    """Generate and assign GroupTaskStatus to each group and task."""
    for group in db.session.scalars(db.select(Group)):
        for task in db.session.scalars(db.select(Task)):
            group_status = GroupTaskStatus(group_id=group.id, task_id=task.id)
            db.session.add(group_status)
    db.session.commit()


def populate_db():
    """Reset the DB and populate it with new data for testing."""
    reset_db()

    # Add users
    users = generate_users()
    db.session.add_all(users)
    db.session.commit()

    # Add tasks
    tasks = generate_tasks()
    db.session.add_all(tasks)
    db.session.commit()

    # Add support services
    services = generate_support_services()
    db.session.add_all(services)
    db.session.commit()

    # Add students
    students = generate_students(users)
    db.session.add_all(students)
    db.session.commit()

    # Add appointment slots
    slots = generate_appointment_slots(services)
    db.session.add_all(slots)
    db.session.commit()

    # Generate group task status mappings
    generate_group_task_status()

    print("Database populated with test data.")


