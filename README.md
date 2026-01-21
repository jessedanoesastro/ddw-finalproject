# 📚 Study Buddy 

A platform for students to organize, find, and join study sessions. This project was built for the final evaluation of **Database-driven Webtechnology (2025-2026)**.

---

Built by **Group 9**:

* **Iwan Hofstra - s5769450** - Project Manager & Model (Data & Logica)
* **Anko van Dijk - s4074661** - Controller (Functionality & Flow)
* **Jesse Danoesastro - S4932781** - Admin & Integration
* **Jerre Scheenaard - S5261139** - View & Frontend/Interface

---

# Motivation
The idea for the project was originated from the situation that students often struggle with focus and finding motivation when studying alone. While many benefit from the accountability of a group, organizing informal sessions often requires a social network that not everyone has. Study Buddy lowers this barrier by providing a platform for students to find and join peer-led study groups.

---

# Core Features
User Authentication: Secure registration and login with hashed passwords and session management.

Session CRUD: Complete lifecycle for study appointments (Create, Read, Update, Delete).

Joining Logic: Ability for students to sign up for or leave existing sessions.

Admin Dashboard: Tools for moderation, including banning users and deleting inappropriate sessions.

Statistics: Real-time tracking of platform usage (active users and sessions).

API Endpoints: Modular API for authentication and session data retrieval.

---

## Documentation

- Source code with clear module separation
- API routes located in `app/api/`
- Database migration scripts in `migrations/`
- Dependency lists in `requirements.txt`
- Report - handed in separately from repository

---

## Project Structure

.

├─ app/

│  ├─ __init__.py          # app factory + extensions

│  ├─ models.py            # User + Session models

│  ├─ forms.py             # Login + Registration forms

│  ├─ main/

│  │  └─ routes.py         # main routes (UI)

│  ├─ templates/           # html templates

│  └─ static/              # CSS/JS

├─ migrations/             # Alembic migration files

├─ config.py               # configuration (SECRET_KEY, DB URI)

├─ run.py                  # entry point (creates tables + runs server)

├─ requirements.txt        # requirements for macOS

├─ requirements_window.txt # minimal pip requirements for Windows

└─ studybuddy.db           # SQLite database (included for demo)

---

## Installation Requirements

Before running the project, make sure you have:

- **Python 3.10+**
- **pip** (Python package manager)
- **virtualenv** (recommended)

---

## Dependencies

All required Python packages are listed in:

- `requirements.txt` (macOS/Linux)
- `requirements_window.txt` (Windows)

Key dependencies include:

- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate
- Werkzeug

---


## How to Run the Project

### 1. Clone repository to desired location

### 2. Create and Activate a Virtual Environment

`$ python -m venv venv`

`$ source venv/bin/activate`   # macOS/Linux

`$ venv\Scripts\activate`      # Windows

### 3. install dependencies

`$ pip install -r requirements.txt` (macOS/Linux)

`$ pip install -r requirements_window.txt` (Windows)

### 4. Run the application

`$ python run.py`

The application will start locally at: http://127.0.0.1:5000