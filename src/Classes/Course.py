from dataclasses import dataclass, field

@dataclass
class Course:
    name: str
    spesialization:str
    level:int
    teacher: str
    is_core:bool
    prerequisites: set[str] = field(default_factory=set)
