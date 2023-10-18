import json


def get_player(governor_id, json_file_path):
    # Load the data from the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    player_stats = []

    # Searching player stats
    for player in data['STATS']:
        if player["Governor ID"] == governor_id:
            player_stats.append(player)

    for player_kvk in data['KVK']:
        if player_kvk["Governor ID"] == governor_id:
            player_stats.append(player_kvk)

    return player_stats if player_stats else None

