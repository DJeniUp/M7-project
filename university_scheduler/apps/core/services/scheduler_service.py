from collections import defaultdict

from apps.core.domain.course import Course as DomainCourse
from apps.core.domain.scheduler import Scheduler
from apps.core.domain.teacher import Teacher as DomainTeacher
from apps.core.domain.university_data import UniversityData
from apps.core.models import Course, Teacher


class SchedulerService:
    @staticmethod
    def generate_schedule(modules_count: int, max_courses_per_module: int) -> dict[int, list[dict[str, str]]]:
        teachers = list(Teacher.objects.prefetch_related('available_modules').all())
        courses = list(
            Course.objects.select_related('teacher', 'specialization').prefetch_related('prerequisites').all()
        )

        domain_teachers = {
            t.id: DomainTeacher(
                id=t.id,
                name=t.name,
                country=t.country,
                available_modules={module.number for module in t.available_modules.all()},
            )
            for t in teachers
        }

        domain_courses = [
            DomainCourse(
                id=c.id,
                name=c.name,
                specialization=c.specialization.name,
                level=c.level,
                teacher_id=c.teacher_id,
                is_core=c.is_core,
                prerequisite_ids={pre.id for pre in c.prerequisites.all()},
            )
            for c in courses
        ]

        university_data = UniversityData(
            modules_count=modules_count,
            max_courses_per_module=max_courses_per_module,
            teachers=list(domain_teachers.values()),
            courses=domain_courses,
        )

        solver = Scheduler(university_data)
        assignment = solver.solve()

        schedule_by_module: dict[int, list[dict[str, str]]] = defaultdict(list)
        course_by_id = {course.id: course for course in courses}

        for course_id, module_number in assignment.items():
            django_course = course_by_id[course_id]
            schedule_by_module[module_number].append(
                {
                    'name': django_course.name,
                    'teacher': django_course.teacher.name,
                    'specialization': django_course.specialization.name,
                    'level': str(django_course.level),
                }
            )

        ordered_schedule: dict[int, list[dict[str, str]]] = {}
        for module_number in range(1, modules_count + 1):
            ordered_schedule[module_number] = sorted(
                schedule_by_module[module_number], key=lambda item: item['name']
            )

        return ordered_schedule
