from ortools.sat.python import cp_model

from .university_data import UniversityData


class Scheduler:
    def __init__(self, data: UniversityData):
        self.data = data

    def solve(self) -> dict[int, int]:
        """
        Return mapping: {course_id: module_number}.
        Raises ValueError if no feasible schedule exists.
        """
        if not self.data.courses:
            return {}

        modules = list(range(1, self.data.modules_count + 1))
        model = cp_model.CpModel()

        # x[(course_id, module)] == 1 if the course is scheduled in that module.
        x: dict[tuple[int, int], cp_model.IntVar] = {}
        for course in self.data.courses:
            for module in modules:
                x[(course.id, module)] = model.NewBoolVar(f'course_{course.id}_module_{module}')

        # 1) Each course is assigned to exactly one module.
        for course in self.data.courses:
            model.AddExactlyOne(x[(course.id, module)] for module in modules)

        # 2) Max courses per module.
        for module in modules:
            model.Add(
                sum(x[(course.id, module)] for course in self.data.courses)
                <= self.data.max_courses_per_module
            )

        # 3) Teacher availability constraint.
        teacher_by_id = {teacher.id: teacher for teacher in self.data.teachers}
        for course in self.data.courses:
            teacher = teacher_by_id.get(course.teacher_id)
            if teacher is None:
                raise ValueError(f'Teacher with id={course.teacher_id} not found for course {course.name}.')

            allowed = set(teacher.available_modules)
            for module in modules:
                if module not in allowed:
                    model.Add(x[(course.id, module)] == 0)

        # 4) Prerequisites constraint: module(course) > module(prerequisite).
        module_of: dict[int, cp_model.IntVar] = {}
        for course in self.data.courses:
            module_var = model.NewIntVar(1, self.data.modules_count, f'module_of_course_{course.id}')
            module_of[course.id] = module_var
            model.Add(module_var == sum(module * x[(course.id, module)] for module in modules))

        course_ids = {course.id for course in self.data.courses}
        for course in self.data.courses:
            for prerequisite_id in course.prerequisite_ids:
                if prerequisite_id not in course_ids:
                    raise ValueError(
                        f'Course {course.name} references missing prerequisite id={prerequisite_id}.'
                    )
                model.Add(module_of[course.id] > module_of[prerequisite_id])

        # 5) A teacher can teach only one course per module.
        for teacher in self.data.teachers:
            teacher_courses = [course for course in self.data.courses if course.teacher_id == teacher.id]
            for module in modules:
                model.Add(sum(x[(course.id, module)] for course in teacher_courses) <= 1)

        # Compact schedule by minimizing the latest used module index.
        max_module_used = model.NewIntVar(1, self.data.modules_count, 'max_module_used')
        for course in self.data.courses:
            model.Add(max_module_used >= module_of[course.id])
        model.Minimize(max_module_used)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise ValueError(
                'No feasible schedule found. Check teacher availability, prerequisites, '
                'module count, and module capacity.'
            )

        return {
            course.id: int(solver.Value(module_of[course.id]))
            for course in self.data.courses
        }
