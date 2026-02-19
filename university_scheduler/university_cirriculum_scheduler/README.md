# External Curriculum Scheduler

## 1. Project description
This package is a standalone Python scheduler used by the Django app as the external algorithm.
It reads CSV inputs, builds domain objects (`Teacher`, `Course`, `Module`), runs 3 scheduling passes (celebrity, chain, solitary), and produces a final schedule.

Main files:
- `main.py`: entrypoint
- `data_loaders.py`: CSV loading/builders
- `classes/`: scheduling engine and domain classes
- `csvs/`: source data files

## ii. Dev setup instructions (step-by-step)
1. Open terminal in repo root.
2. Create and activate a virtual environment.

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Run the external scheduler:
```bash
python university_scheduler/university_cirriculum_scheduler/main.py
```

## iii. How to run tests
From repository root:
```bash
pytest -q
```

## iv. How to run linters
From repository root:
```bash
ruff check .
```

Optional autofix:
```bash
ruff check . --fix
```

## v. How deployment works
This package is deployed as part of the Django web app, not as a separate service.

Flow in production:
1. Koyeb builds and runs Django via `Procfile` (`gunicorn ...`).
2. User selects `External Algorithm` in web UI.
3. Django service (`apps/core/services/external_scheduler_service.py`) imports this package.
4. Scheduler runs using CSVs in `university_scheduler/university_cirriculum_scheduler/csvs/`.

## vi. Environment variables description
This standalone package does not require dedicated env vars.
It uses the Django app runtime settings when called from the web app.

Relevant app-level variables:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `KOYEB_PUBLIC_DOMAIN`
- `DATABASE_URL`
