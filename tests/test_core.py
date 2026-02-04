import pytest
from wttr_cli.core import normalize_city, build_wttr_url


def test_normalize_spaces():
    assert normalize_city("  New   York ") == "New York"


def test_empty_city():
    with pytest.raises(ValueError):
        normalize_city("   ")


def test_build_url_json():
    url = build_wttr_url("Berlin")
    assert url == "https://wttr.in/Berlin?format=j1"


def test_build_url_text():
    url = build_wttr_url("Berlin", json=False)
    assert url.endswith("format=3")
