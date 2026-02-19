from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from Classes.Course import Course
from Classes.Teachers import Teacher
from Classes.University import UniversityData


def test_course_prerequisites_default_to_empty_set():
    course = Course(
        name="Math",
        spesialization="Math",
        level=1,
        teacher="Ivan",
        is_core=True,
    )
    assert course.prerequisites == set()


def test_add_teacher_stores_teacher_by_name():
    data = UniversityData()
    teacher = Teacher(
        name="Ivan",
        country="Ukraine",
        spesialization={"Math"},
        available_modules={1, 2},
    )

    data.add_teacher(teacher)

    assert data.teachers["Ivan"] == teacher


def test_add_course_stores_course_by_name():
    data = UniversityData()
    course = Course(
        name="Algorithms",
        spesialization="Algorithms",
        level=2,
        teacher="Petro",
        is_core=True,
    )

    data.add_course(course)

    assert data.courses["Algorithms"] == course


def test_teacher_modules_for_returns_available_modules():
    data = UniversityData()
    teacher = Teacher(
        name="Petro",
        country="Ukraine",
        spesialization={"AI", "Algorithms"},
        available_modules={2, 3, 4},
    )
    course = Course(
        name="AI",
        spesialization="AI",
        level=3,
        teacher="Petro",
        is_core=False,
    )
    data.add_teacher(teacher)
    data.add_course(course)

    modules = data.teacher_modules_for("AI")

    assert modules == {2, 3, 4}


def test_teacher_modules_for_raises_for_missing_course():
    data = UniversityData()
    with pytest.raises(KeyError):
        data.teacher_modules_for("Missing course")
