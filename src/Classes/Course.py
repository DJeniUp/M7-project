from dataclasses import dataclass, field
from typing import list, set

@dataclass
class Course:
    name: str
    prerequisites: set[str] = field(default_factory=set)
    teacher: str 
        
