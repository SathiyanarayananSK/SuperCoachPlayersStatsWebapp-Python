import pytest
from unittest.mock import patch
import backend
import frontend
import copy

# Sample mock API responses for different years and rounds (simplified for testing)
mock_api_responses = {
    (2025, 0): [
        {
            "id": 1,
            "first_name": "Jesse",
            "last_name": "Arthars",
            "player_stats": [{"round": 10, "points": 0, "position": 159}],
            "positions": [{"position": "CTW", "position_long": "Wing/Centre"}]
        }
    ],
    (2024, 5): [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "player_stats": [{"round": 5, "points": 3, "position": 160}],
            "positions": [{"position": "FL", "position_long": "Fullback"}]
        }
    ],
    (2023, 10): [
        {
            "id": 1,
            "first_name": "Alice",
            "last_name": "Smith",
            "player_stats": [{"round": 10, "points": 5, "position": 161}],
            "positions": [{"position": "HB", "position_long": "Halfback"}]
        }
    ],
    (2022, 15): [
        {
            "id": 1,
            "first_name": "Bob",
            "last_name": "Johnson",
            "player_stats": [{"round": 15, "points": 2, "position": 162}],
            "positions": [{"position": "FL", "position_long": "Fullback"}]
        }
    ],
}

mock_api_responses_copy = copy.deepcopy(mock_api_responses)


# Step 1: Mock the API response and test the data flow
@pytest.mark.parametrize("entered_year, entered_round", [
    (2025, 0),
    (2024, 5),
    (2023, 10),
    (2022, 15),
])
def test_integration(entered_year, entered_round):
    # Mocking the API call based on entered year and round using patch
    with patch("backend.requests.get") as mock_get:
        # Set the mock API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_api_responses[(entered_year, entered_round)]

        # Fetch data using the frontend function (which calls the backend)
        summary, stats, positions = frontend.fetch_data(entered_year, entered_round)


        # Validate the data at the integration level

        # Check that the summary data is correct
        assert len(summary) == 1
        assert summary[0]["first_name"] == mock_api_responses_copy[(entered_year, entered_round)][0]["first_name"]
        assert summary[0]["last_name"] == mock_api_responses_copy[(entered_year, entered_round)][0]["last_name"]

        # Check that the stats data is correctly processed
        assert len(stats) == 1
        assert stats[0]["player_full_name"] == f"{mock_api_responses_copy[(entered_year, entered_round)][0]['first_name']} {mock_api_responses_copy[(entered_year, entered_round)][0]['last_name']}"
        assert stats[0]["points"] == mock_api_responses_copy[(entered_year, entered_round)][0]["player_stats"][0]["points"]
        assert stats[0]["position"] == mock_api_responses_copy[(entered_year, entered_round)][0]["player_stats"][0]["position"]

        # Check that the positions data is correctly processed
        assert len(positions) == 1
        assert positions[0]["player_full_name"] == f"{mock_api_responses_copy[(entered_year, entered_round)][0]['first_name']} {mock_api_responses[(entered_year, entered_round)][0]['last_name']}"
        assert positions[0]["position"] == mock_api_responses_copy[(entered_year, entered_round)][0]["positions"][0]["position"]

        # Check that the data is passed correctly to the frontend for display

        stats_flat = backend.make_data_flat(stats)
        assert "player_stats" not in stats_flat[0]
        assert "position" in stats_flat[0]
        assert stats_flat[0]["round"] == mock_api_responses_copy[(entered_year, entered_round)][0]["player_stats"][0]["round"]

        positions_flat = backend.make_data_flat(positions)
        assert "positions" not in positions_flat[0]
        assert "position_long" in positions_flat[0]
        assert positions_flat[0]["position"] == mock_api_responses_copy[(entered_year, entered_round)][0]["positions"][0]["position"]

