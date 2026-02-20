#!/usr/bin/env python
"""Project root manage.py shim for platforms expecting /workspace/manage.py."""

import os
import sys
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parent / "university_scheduler"
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "university_scheduler.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
