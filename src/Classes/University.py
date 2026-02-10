from dataclasses import dataclass, field
from typing import dict

from Course import Course
from Teachers import Teacher


@dataclass
class UniversityData:
    courses: dict[str, Course] = field(default_factory=dict)
    teachers: dict[str, Teacher] = field(default_factory=dict)

    modules_count: int = 14
    max_courses_per_module: int = 9


    def add_course(self, course: Course):
        self.courses[course.name] = course

    def add_teacher(self, teacher: Teacher):
        self.teachers[teacher.name] = teacher

    def teacher_modules_for(self, course_name: str):
        teacher_name = self.courses[course_name].teacher
        return self.teachers[teacher_name].available_modules
