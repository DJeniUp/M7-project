# University Scheduler

Production-ready Django project for scheduling university courses with clean architecture separation:

- Django ORM layer (`apps/core/models.py`)
- Service/business layer (`apps/core/services/`)
- Pure domain layer with CP-SAT solver (`apps/core/domain/`)

## Tech Stack

- Django 5+
- PostgreSQL
- OR-Tools (CP-SAT)

## Project Structure

```text
university_scheduler/
├── manage.py
├── requirements.txt
├── README.md
├── university_scheduler/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── apps/
    └── core/
        ├── admin.py
        ├── forms.py
        ├── models.py
        ├── urls.py
        ├── views.py
        ├── services/
        │   └── scheduler_service.py
        ├── domain/
        │   ├── course.py
        │   ├── teacher.py
        │   ├── university_data.py
        │   └── scheduler.py
        └── templates/core/
            └── schedule.html
```

## Installation

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Set these before running:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`True` or `False`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated, e.g. `localhost,127.0.0.1`)
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Example (PowerShell):

```powershell
$env:DJANGO_SECRET_KEY = "replace-me"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
$env:DB_NAME = "university_scheduler"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "postgres"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
```

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

## Run the App

```bash
python manage.py runserver
```

Open:

- Scheduler page: `http://127.0.0.1:8000/`
- Admin page: `http://127.0.0.1:8000/admin/`

## Scheduling Constraints

The CP-SAT solver enforces:

1. Each course is assigned to exactly one module.
2. Max courses per module.
3. Teacher availability by module.
4. Prerequisite ordering (`module(course) > module(prerequisite)`).
5. A teacher teaches at most one course per module.

## Notes

- Business logic is intentionally kept out of views.
- Domain classes are pure Python dataclasses without Django imports.
- Scheduler errors are surfaced in the UI when no feasible schedule exists.
