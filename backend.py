import requests

# Default header to imitate browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Referer": "https://www.foxsports.com.au/",
}


# Function to get data from the API based on year and round returning summary, stats and positions as JSON
def get_players_data(year, rnd):
    url = f"https://www.supercoach.com.au/{year}/api/nrl/classic/v1/players-cf?embed=notes%2Codds%2Cplayer_stats%2Cpositions&round={rnd}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        try:
            summary = response.json()
        except ValueError:
            print("Error: Failed to decode JSON response.")
            return [], [], []

    # Return empty lists on request failure
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return [], [], []

    # Lists for storing stats and positions
    stats = []
    positions = []

    # Remove stats and position objects from players and store it in stats and positions list
    for player in summary:
        player_stats = player.pop("player_stats", None)
        player_position = player.pop("positions", None)

        # Beautify the data
        first_name = player.get("first_name", "")
        last_name = player.get("last_name", "")
        player_full_name = f"{first_name} {last_name}".strip()


        # Check if stats and positions exist and are in the expected format
        if player_stats and isinstance(player_stats, list) and len(player_stats) > 0:
            player_stats[0].pop("player_id", None)
            stats.append({"id": player.get("id"), "player_full_name": player_full_name, **player_stats[0]})

        if player_position and isinstance(player_position, list) and len(player_position) > 0:
            positions.append(
                {"id": player.get("id"), "player_full_name": player_full_name, **player_position[0]})

    if len(stats)>0 and "round" in stats[0]:
        if stats[0]["round"] != rnd:
            return [], [], []

    return summary, stats, positions

# Function to make the Json data flat - Return the json data as just list of dictionaries no nests
def make_data_flat(json_data):
    flat_data = []
    for player in json_data:
        player_details = {}
        for key, value in player.items():
            if isinstance(value, dict):
                handle_dictionary(key, value, player_details)
            elif isinstance(value, list):
                handle_list(key, value, player_details)
            else:
                player_details[key] = value

        flat_data.append(player_details)

    return flat_data

# Assists the make_data_flat function by handling dictionary values
def handle_dictionary(dict_key, dict_value, player_details):
    for name, detail in dict_value.items():
        new_name = f"{dict_key}_{name}"
        if isinstance(detail, dict):
            handle_dictionary(new_name, detail, player_details)
        else:
            player_details[new_name] = detail

# Assists the make_data_flat function by handling list values
def handle_list(list_key, list_value, player_details):
    try:
        new_dict = list_value[0]
        handle_dictionary(list_key, new_dict, player_details)
    except IndexError:
        player_details[list_key] = list_value

def filter_json_by_search_term(player_term, players_json):
    result = []

    if isinstance(player_term, int):  # Check if player_term is an int
        player_id = player_term
        for player in players_json:
            if player["id"] == player_id:
                result.append(player)
        return result

    elif isinstance(player_term, str):  # Check if player_term is a string
        player_name = player_term
        for player in players_json:
            if "first_name" in player and "last_name" in player:
                full_name = f"{player['first_name']} {player['last_name']}"
            elif "player_full_name" in player:
                full_name = player["player_full_name"]
            else:
                full_name = ""

            if player_name.lower() in full_name.lower():
                result.append(player)
        return result

    else:
        return []



if __name__ == "__main__":
    players_summary, players_stats, players_position = get_players_data(year=2025, rnd=10)


