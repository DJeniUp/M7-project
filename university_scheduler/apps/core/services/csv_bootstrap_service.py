from __future__ import annotations

import csv
from pathlib import Path

from django.db import transaction

from apps.core.models import Course, Module, Specialization, Teacher


class CsvBootstrapService:
    @staticmethod
    def load_from_external_csvs() -> dict[str, int]:
        csv_dir = Path(__file__).resolve().parents[3] / 'university_cirriculum_scheduler' / 'csvs'
        course_teacher_csv = csv_dir / 'course_teacher.csv'
        prereqs_csv = csv_dir / 'prereqs_CSDS.csv'
        teacher_availability_csv = csv_dir / 'teacher_availability.csv'

        required_files = [course_teacher_csv, prereqs_csv, teacher_availability_csv]
        missing = [str(path) for path in required_files if not path.exists()]
        if missing:
            raise ValueError(f'CSV files not found: {", ".join(missing)}')

        course_teachers: dict[str, list[str]] = {}
        all_courses: set[str] = set()
        all_teachers: set[str] = set()

        with course_teacher_csv.open('r', encoding='utf-8-sig', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue
                course_name = (row[0] or '').strip()
                if not course_name:
                    continue
                teacher_names = [name.strip() for name in row[1:] if (name or '').strip()]
                course_teachers[course_name] = teacher_names
                all_courses.add(course_name)
                all_teachers.update(teacher_names)

        prereq_map: dict[str, list[str]] = {}
        level_map: dict[str, int] = {}
        with prereqs_csv.open('r', encoding='utf-8-sig', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue
                course_name = (row[0] or '').strip()
                if not course_name:
                    continue

                raw_level = (row[1] if len(row) > 1 else '').strip()
                level = int(raw_level) + 1 if raw_level.isdigit() else 1
                level_map[course_name] = max(1, level)

                prereqs = [name.strip() for name in row[2:] if (name or '').strip()]
                prereq_map[course_name] = prereqs

                all_courses.add(course_name)
                all_courses.update(prereqs)

        availability_by_teacher: dict[str, set[int]] = {}
        with teacher_availability_csv.open('r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                teacher_name = (row.get('name') or '').strip()
                if not teacher_name:
                    continue

                allowed_modules = {
                    module_number
                    for module_number in range(1, 15)
                    if (row.get(f'M{module_number}') or '').strip() != '-1'
                }
                availability_by_teacher[teacher_name] = allowed_modules
                all_teachers.add(teacher_name)

        fallback_teacher = 'Unassigned Teacher'
        if not all_teachers:
            all_teachers.add(fallback_teacher)

        with transaction.atomic():
            Course.objects.all().delete()
            Teacher.objects.all().delete()
            Module.objects.all().delete()
            Specialization.objects.all().delete()

            modules = {
                number: Module.objects.create(number=number)
                for number in range(1, 15)
            }

            specialization = Specialization.objects.create(name='General')

            teacher_by_name: dict[str, Teacher] = {}
            for teacher_name in sorted(all_teachers):
                teacher = Teacher.objects.create(name=teacher_name, country='Unknown')
                allowed_modules = availability_by_teacher.get(teacher_name, set(range(1, 15)))
                teacher.available_modules.set(modules[number] for number in sorted(allowed_modules))
                teacher_by_name[teacher_name] = teacher

            course_by_name: dict[str, Course] = {}
            for course_name in sorted(all_courses):
                teachers = course_teachers.get(course_name) or [fallback_teacher]
                primary_teacher_name = teachers[0]
                primary_teacher = teacher_by_name.get(primary_teacher_name)
                if primary_teacher is None:
                    primary_teacher = teacher_by_name[fallback_teacher]

                course = Course.objects.create(
                    name=course_name,
                    specialization=specialization,
                    level=level_map.get(course_name, 1),
                    teacher=primary_teacher,
                    is_core=True,
                )
                course_by_name[course_name] = course

            for course_name, prereqs in prereq_map.items():
                course = course_by_name.get(course_name)
                if course is None:
                    continue
                prereq_objects = [course_by_name[name] for name in prereqs if name in course_by_name]
                course.prerequisites.set(prereq_objects)

        return {
            'teachers': len(teacher_by_name),
            'courses': len(course_by_name),
            'modules': 14,
            'max_courses_per_module': 9,
        }
