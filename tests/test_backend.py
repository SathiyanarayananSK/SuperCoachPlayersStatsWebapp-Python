import pytest
import backend
import requests
from unittest.mock import patch

# Sample API response (mocked)
mock_api_response = [
    {
        "id": 1,
        "first_name": "Jesse",
        "last_name": "Arthars",
        "player_stats": [{"round": 10, "points": 0, "position": 159}],
        "positions": [{"position": "CTW", "position_long": "Wing/Centre"}]
    }
]


# Mock the API request
@patch("backend.requests.get")
def test_get_players_data_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_api_response

    summary, stats, positions = backend.get_players_data(2025, 0)

    assert len(summary) == 1
    assert stats[0]["player_full_name"] == "Jesse Arthars"
    assert stats[0]["points"] == 0
    assert positions[0]["position"] == "CTW"


@patch("backend.requests.get")
def test_get_players_data_api_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("API Error")

    summary, stats, positions = backend.get_players_data(2025, 0)

    assert summary == []
    assert stats == []
    assert positions == []


def test_make_data_flat():
    json_data = [
        {
            "id": 1,
            "first_name": "Jesse",
            "team": {"name": "Broncos"},
            "player_stats": [{"round": 10, "points": 0}]
        }
    ]

    flat_data = backend.make_data_flat(json_data)

    assert flat_data[0]["id"] == 1
    assert flat_data[0]["first_name"] == "Jesse"
    assert flat_data[0]["team_name"] == "Broncos"
    assert flat_data[0]["player_stats_round"] == 10
    assert "player_stats" not in flat_data[0]
