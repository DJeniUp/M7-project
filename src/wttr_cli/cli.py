import argparse
import sys
import requests

from .core import build_wttr_url, normalize_city


def fetch_weather(city: str, *, json_mode: bool = True):
    url = build_wttr_url(city, json=json_mode)

    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)

    return r.json() if json_mode else r.text


def format_weather(data: dict, city: str) -> str:
    current = data["current_condition"][0]
    today = data["weather"][0]

    temp = current["temp_C"]
    desc = current["weatherDesc"][0]["value"]
    max_t = today["maxtempC"]
    min_t = today["mintempC"]

    return (
        f"Weather for {city}\n"
        f"Now: {temp}°C, {desc}\n"
        f"Today: max {max_t}°C / min {min_t}°C"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("city", nargs="?", help="City name")
    parser.add_argument("--simple", action="store_true")

    args = parser.parse_args()

    if not args.city:
        print("City is required", file=sys.stderr)
        sys.exit(1)

    city = normalize_city(args.city)

    if args.simple:
        text = fetch_weather(city, json_mode=False)
        print(text.strip())
    else:
        data = fetch_weather(city, json_mode=True)
        print(format_weather(data, city))


if __name__ == "__main__":
    main()
