from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from Classes.University import UniversityData


def test_university_data_defaults_match_expected_constraints():
    data = UniversityData()
    assert data.modules_count == 14
    assert data.max_courses_per_module == 9


def test_university_data_accepts_custom_constraints():
    data = UniversityData(modules_count=10, max_courses_per_module=5)
    assert data.modules_count == 10
    assert data.max_courses_per_module == 5
