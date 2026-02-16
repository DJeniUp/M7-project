from dataclasses import dataclass, field


@dataclass(frozen=True)
class Teacher:
    id: int
    name: str
    country: str
    available_modules: set[int] = field(default_factory=set)
