# UniSupport - Student Wellbeing Platform

A command-line prototype for a student wellbeing support platform that helps students track their mood and book support sessions.

## Features

- **Mood Tracking**: Log daily mood scores (1-5)
- **Appointment Booking**: Book support sessions (counselling, academic support, wellbeing workshops)
- **Data Viewing**: View mood history and booked appointments

## Technical Details

- **Language**: Python 3
- **Architecture**: Object-Oriented Design
- **Current Version**: CLI Prototype
- **Future Plans**: Web-based implementation using Flask

## Project Structure

```
BUS_Prototype/
├── app/
│   ├── cli.py      # Command-line interface
│   ├── forms.py    # Form validation
│   ├── models.py   # Core data models
│   └── views.py    # (Future) Flask views
├── config.py       # Configuration
├── run.py         # Application entry point
└── README.md      # This file
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd BUS_Prototype
   ```

2. Run the application:
   ```bash
   python app/cli.py
   ```

## Usage

1. Log in with your student ID and name
2. Use the main menu to:
   - Log your mood (1-5 scale)
   - Book appointments
   - View mood history
   - View booked appointments

## Design Principles

- Single Responsibility Principle: Each class and method serves one clear purpose
- Encapsulation: Data is stored within objects and accessed via methods
- CLI-based Simulation: Mimics interaction without external systems or UIs

## Future Enhancements

- Convert to Flask-based web application
- Implement design patterns (Decorator for logging, Observer for notifications)
- Expand system relationships
- Add database integration
- Implement user authentication 