import re


def normalize_city(city: str) -> str:
    if not city or not city.strip():
        raise ValueError("City cannot be empty")

    city = city.strip()
    city = re.sub(r"\s+", " ", city)
    return city


def build_wttr_url(city: str, *, json: bool = True) -> str:
    city = normalize_city(city)
    fmt = "j1" if json else "3"
    return f"https://wttr.in/{city}?format={fmt}"
