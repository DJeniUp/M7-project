from dataclasses import dataclass, field

@dataclass
class Teacher:
    name: str
    country: str
    spesialization: set[str]
    available_modules: set[int]
