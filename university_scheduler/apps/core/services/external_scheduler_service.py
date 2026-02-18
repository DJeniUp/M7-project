from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from apps.core.models import Course


class ExternalSchedulerService:
    @staticmethod
    def generate_schedule(modules_count: int, max_courses_per_module: int) -> dict[int, list[dict[str, str]]]:
        if modules_count < 14:
            raise ValueError('External Algorithm requires at least 14 modules due to its timeline model.')

        external_repo_path = Path(__file__).resolve().parents[3]
        external_repo_str = str(external_repo_path)
        if external_repo_str not in sys.path:
            sys.path.insert(0, external_repo_str)

        try:
            from university_cirriculum_scheduler.classes.scheduler import Scheduler as ExternalScheduler
            from university_cirriculum_scheduler.data_loaders import (
                build_courses,
                build_modules,
                build_teachers,
                load_celebrity_courses,
            )
        except ImportError as exc:
            raise ValueError('External Algorithm modules could not be imported.') from exc

        courses = list(
            Course.objects.select_related('specialization').all()
        )
        course_metadata = {
            course.name: {
                'specialization': course.specialization.name,
                'level': str(course.level),
            }
            for course in courses
        }

        external_teachers = build_teachers()
        external_courses = build_courses(external_teachers)
        external_modules = build_modules(total_modules=modules_count, max_capacity=max_courses_per_module)
        celebrity_courses = load_celebrity_courses()

        scheduler = ExternalScheduler(external_teachers, external_courses, external_modules)

        try:
            scheduler.pass1_celebrity(celebrity_courses)
            scheduler.pass2_chains()
            scheduler.pass3_solitary()
        except Exception as exc:
            raise ValueError(str(exc)) from exc

        schedule_by_module: dict[int, list[dict[str, str]]] = defaultdict(list)

        for ext_course in external_courses.values():
            if ext_course.module_assigned is None:
                continue

            module_number = int(ext_course.module_assigned)
            metadata = course_metadata.get(ext_course.name, {})
            schedule_by_module[module_number].append(
                {
                    'name': ext_course.name,
                    'teacher': ext_course.teacher_assigned or '',
                    'specialization': metadata.get('specialization', ''),
                    'level': metadata.get('level', ''),
                }
            )

        ordered_schedule: dict[int, list[dict[str, str]]] = {}
        for module_number in range(1, modules_count + 1):
            ordered_schedule[module_number] = sorted(
                schedule_by_module[module_number], key=lambda item: item['name']
            )

        return ordered_schedule

