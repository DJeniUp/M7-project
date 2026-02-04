import pytest
from unittest.mock import patch
from wttr_cli.cli import format_weather


def test_format_weather():
    fake = {
        "current_condition": [
            {"temp_C": "10", "weatherDesc": [{"value": "Sunny"}]}
        ],
        "weather": [
            {"maxtempC": "12", "mintempC": "5"}
        ]
    }

    out = format_weather(fake, "Berlin")
    assert "Sunny" in out


@patch("wttr_cli.cli.requests.get")
def test_network_mock(mock_get):
    class R:
        def raise_for_status(self): pass
        def json(self): return {"current_condition":[{"temp_C":"1","weatherDesc":[{"value":"Clear"}]}],
                                "weather":[{"maxtempC":"2","mintempC":"0"}]}

    mock_get.return_value = R()

    from wttr_cli.cli import fetch_weather
    data = fetch_weather("Berlin")
    assert "current_condition" in data


def test_missing_city():
    import subprocess
    result = subprocess.run(["weather"], capture_output=True)
    assert result.returncode != 0
