from Classes.Course import Course
from Classes.Teachers import Teacher
from Classes.University import UniversityData
from Scheduler import Scheduler


def main():
    data = UniversityData(
        modules_count=4,
        max_courses_per_module=2
    )

    # -----------------
    # Teachers
    # -----------------
    data.add_teacher(
        Teacher(
            name="Ivan",
            country="Ukraine",
            spesialization={"Math"},
            available_modules={0, 1}
        )
    )

    data.add_teacher(
        Teacher(
            name="Petro",
            country="Ukraine",
            spesialization={"AI", "Algorithms"},
            available_modules={1, 2, 3}
        )
    )

    # -----------------
    # Courses
    # -----------------
    data.add_course(
        Course(
            name="Math",
            spesialization="Math",
            level=1,
            teacher="Ivan",
            is_core=True
        )
    )

    data.add_course(
        Course(
            name="Algorithms",
            spesialization="Algorithms",
            level=2,
            teacher="Petro",
            is_core=True,
            prerequisites={"Math"}
        )
    )

    data.add_course(
        Course(
            name="AI",
            spesialization="AI",
            level=3,
            teacher="Petro",
            is_core=False,
            prerequisites={"Algorithms"}
        )
    )

    # -----------------
    # Solve
    # -----------------
    scheduler = Scheduler(data)
    schedule = scheduler.solve()

    print("\n📅 Schedule:")
    for m, courses in schedule.items():
        print(f"Module {m}: {courses}")


if __name__ == "__main__":
    main()
