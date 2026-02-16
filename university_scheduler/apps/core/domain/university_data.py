from dataclasses import dataclass

from .course import Course
from .teacher import Teacher


@dataclass(frozen=True)
class UniversityData:
    modules_count: int
    max_courses_per_module: int
    teachers: list[Teacher]
    courses: list[Course]
