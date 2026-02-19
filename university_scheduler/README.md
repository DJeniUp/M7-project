# University Scheduler

## 1. Project description
Django application for university course scheduling with two algorithms:
- Internal solver (`apps/core/services/scheduler_service.py`)
- External algorithm integration (`apps/core/services/external_scheduler_service.py`) backed by `university_cirriculum_scheduler/`

The app supports CSV bootstrap, schedule generation, and web UI output per module.

## ii. Dev setup instructions (step-by-step)
1. From repository root, create and activate a virtual environment.

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start server:
```bash
python manage.py runserver
```

5. Open `http://127.0.0.1:8000/`.

## iii. How to run tests
Run Django tests:
```bash
python manage.py test
```

Run repository pytest suite from repo root:
```bash
pytest -q
```

## iv. How to run linters
From repo root:
```bash
ruff check .
```

Optional autofix:
```bash
ruff check . --fix
```

## v. How deployment works
Deployment target is Koyeb with Python buildpack.

- Build dependencies come from root `requirements.txt` (which includes this folder's `requirements.txt`).
- Runtime command is defined in root `Procfile`:
```bash
gunicorn university_scheduler.wsgi:application --chdir university_scheduler --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```
- Production static files are served with WhiteNoise.

Typical build steps:
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

## vi. Environment variables description
- `DJANGO_SECRET_KEY`: required secret key.
- `DJANGO_DEBUG`: `True` or `False`.
- `DJANGO_ALLOWED_HOSTS`: comma-separated allowed hosts.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: comma-separated full origins.
- `KOYEB_PUBLIC_DOMAIN`: Koyeb domain, auto-added to host/csrf lists in production.
- `DATABASE_URL`: optional PostgreSQL URL (`postgres://...` or `postgresql://...`); SQLite is used when not set.
