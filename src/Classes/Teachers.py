from dataclasses import dataclass, field
from typing import list, set

@dataclass
class Teacher:
    name: str
    available_modules: set[int] 
