from dataclasses import dataclass, field
from typing import list, set

@dataclass
class Course:
    name: str
    spesialization:str
    level:int
    prerequisites: set[str] = field(default_factory=set)
    teacher: str 
    is_core:bool
        
