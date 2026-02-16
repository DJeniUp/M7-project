from dataclasses import dataclass, field


@dataclass(frozen=True)
class Course:
    id: int
    name: str
    specialization: str
    level: int
    teacher_id: int
    is_core: bool
    prerequisite_ids: set[int] = field(default_factory=set)
